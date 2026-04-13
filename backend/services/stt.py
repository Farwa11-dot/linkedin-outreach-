"""
Speech-to-Text service using OpenAI Whisper (local, no API key).

Whisper runs entirely on-device. The base model works well on CPU.
For faster inference on a GPU server, switch to WHISPER_MODEL=small or medium.
"""
import asyncio
import os
import tempfile
from pathlib import Path

import structlog
import numpy as np
import soundfile as sf
import whisper

from config import get_settings

logger = structlog.get_logger()
settings = get_settings()


class STTService:
    def __init__(self):
        self._model = None

    async def load(self):
        """Load Whisper model into memory (done once at startup)."""
        loop = asyncio.get_event_loop()
        self._model = await loop.run_in_executor(
            None,
            lambda: whisper.load_model(
                settings.whisper_model,
                device=settings.whisper_device,
            ),
        )
        logger.info("Whisper model loaded", model=settings.whisper_model)

    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribe a WAV/PCM file to text.

        Asterisk writes audio as 8kHz 16-bit mono PCM (.sln or .wav).
        Whisper expects 16kHz mono float32. This method resamples automatically.
        """
        if self._model is None:
            raise RuntimeError("STT model not loaded — call load() first")

        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._run_whisper, str(path))
        text = result["text"].strip()
        logger.info("Transcription complete", chars=len(text), preview=text[:80])
        return text

    def _run_whisper(self, audio_path: str) -> dict:
        """Blocking Whisper call — runs in thread executor."""
        audio = whisper.load_audio(audio_path)   # auto-resamples to 16kHz
        audio = whisper.pad_or_trim(audio)
        result = self._model.transcribe(
            audio,
            language="en",
            fp16=False,                           # CPU inference — keep fp32
            temperature=0.0,
        )
        return result

    async def transcribe_raw_pcm(self, pcm_bytes: bytes, sample_rate: int = 8000) -> str:
        """
        Transcribe raw PCM bytes (e.g. piped directly from Asterisk).
        Converts to a temp file then calls transcribe().
        """
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            dir=settings.audio_temp_dir,
            delete=False,
        ) as tmp:
            audio_array = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            sf.write(tmp.name, audio_array, sample_rate, subtype="PCM_16")
            tmp_path = tmp.name

        try:
            return await self.transcribe(tmp_path)
        finally:
            os.unlink(tmp_path)
