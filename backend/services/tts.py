"""
Text-to-Speech service using Piper TTS (wyoming-piper sidecar).

Piper produces natural-sounding speech entirely offline.
The wyoming-piper Docker container exposes a simple TCP protocol.
We communicate with it over the network socket.

Alternatively, if you install piper-tts Python package directly,
uncomment the LOCAL_PIPER block and remove the socket client.
"""
import asyncio
import io
import os
import struct
import tempfile
import wave
from pathlib import Path

import structlog

from config import get_settings

logger = structlog.get_logger()
settings = get_settings()

PIPER_HOST = "piper"       # docker service name
PIPER_PORT = 10200
PIPER_SAMPLE_RATE = 22050


class TTSService:
    def __init__(self):
        self._ready = False

    async def load(self):
        """Verify connectivity to Piper sidecar."""
        try:
            reader, writer = await asyncio.open_connection(PIPER_HOST, PIPER_PORT)
            writer.close()
            await writer.wait_closed()
            self._ready = True
            logger.info("Piper TTS connected", host=PIPER_HOST, port=PIPER_PORT)
        except Exception as exc:
            logger.warning("Piper TTS not reachable at startup — will retry on first call", error=str(exc))

    async def synthesise(self, text: str, output_path: str | None = None) -> str:
        """
        Convert text to speech and save as a WAV file.

        Returns the path to the generated audio file.
        Asterisk can play WAV files directly via AGI STREAM FILE.
        """
        if not output_path:
            output_path = os.path.join(
                settings.audio_temp_dir,
                f"tts_{abs(hash(text))}.wav",
            )

        audio_bytes = await self._request_piper(text)

        # Write 8kHz mono WAV (Asterisk native format)
        # Piper outputs 22050 Hz — resample to 8kHz for Asterisk
        resampled = self._resample(audio_bytes, from_hz=PIPER_SAMPLE_RATE, to_hz=8000)

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)           # 16-bit
            wf.setframerate(8000)
            wf.writeframes(resampled)

        logger.info("TTS synthesis complete", chars=len(text), path=output_path)
        return output_path

    async def _request_piper(self, text: str) -> bytes:
        """
        Send text to wyoming-piper and receive raw PCM audio.

        Wyoming protocol (simplified):
          1. Send JSON header line: {"type": "synthesize", "data": {"text": "..."}}
          2. Receive JSON audio-start header
          3. Receive binary audio chunks
          4. Receive JSON audio-stop
        """
        reader, writer = await asyncio.open_connection(PIPER_HOST, PIPER_PORT)
        try:
            import json
            message = json.dumps({"type": "synthesize", "data": {"text": text}}) + "\n"
            writer.write(message.encode())
            await writer.drain()

            audio_chunks = []
            while True:
                line = await reader.readline()
                if not line:
                    break
                header = json.loads(line.decode())
                if header.get("type") == "audio-chunk":
                    payload_size = header.get("payload_length", 0)
                    if payload_size > 0:
                        chunk = await reader.readexactly(payload_size)
                        audio_chunks.append(chunk)
                elif header.get("type") == "audio-stop":
                    break

            return b"".join(audio_chunks)
        finally:
            writer.close()
            await writer.wait_closed()

    @staticmethod
    def _resample(pcm_bytes: bytes, from_hz: int, to_hz: int) -> bytes:
        """Simple linear decimation resample (integer ratios)."""
        import numpy as np
        audio = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32)
        ratio = from_hz / to_hz
        new_length = int(len(audio) / ratio)
        indices = np.linspace(0, len(audio) - 1, new_length)
        resampled = np.interp(indices, np.arange(len(audio)), audio).astype(np.int16)
        return resampled.tobytes()
