#!/usr/bin/env python3
"""
Asterisk AGI script — bridges the PBX with the FastAPI voice pipeline.

How it works:
  1. Asterisk dials in → executes this AGI script
  2. Script records caller audio (silence-detected chunk)
  3. POSTs audio to FastAPI /calls/speech
  4. Receives path to synthesised reply WAV
  5. Plays reply back to caller
  6. Loops until caller hangs up or AI signals end
  7. POSTs /calls/{session_id}/end for CRM finalisation

Requirements (installed in the Asterisk container):
    pip install requests

Set BACKEND_URL env var or edit BACKEND_URL below.
"""
import os
import sys
import time
import subprocess
import requests
from asterisk.agi import AGI

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
AUDIO_DIR = "/tmp/audio"
SILENCE_THRESHOLD = 1.5   # seconds of silence to stop recording
MAX_RECORDING_SECS = 30   # hard cap per turn
MAX_TURNS = 20            # prevent infinite loops

os.makedirs(AUDIO_DIR, exist_ok=True)


def main():
    agi = AGI()
    agi.answer()
    agi.verbose("Voice AI Receptionist AGI started")

    caller_number = agi.env.get("agi_callerid", "unknown")
    called_number = agi.env.get("agi_dnid", "unknown")
    call_id = agi.env.get("agi_uniqueid", "unknown")

    # ── Start session ──────────────────────────────────────────────────────────
    resp = requests.post(
        f"{BACKEND_URL}/calls/start",
        data={
            "call_id": call_id,
            "caller_number": caller_number,
            "called_number": called_number,
        },
        timeout=10,
    )
    resp.raise_for_status()
    session_id = resp.json()["session_id"]
    agi.verbose(f"Session started: {session_id}")

    # ── Play greeting ──────────────────────────────────────────────────────────
    greeting_path = synthesise_greeting(session_id, caller_number)
    if greeting_path:
        play_audio(agi, greeting_path)

    # ── Conversation loop ──────────────────────────────────────────────────────
    for turn in range(MAX_TURNS):
        # 1. Record caller audio chunk
        audio_path = os.path.join(AUDIO_DIR, f"{session_id}_caller_{turn}.wav")
        agi.record_file(
            audio_path.replace(".wav", ""),   # Asterisk appends .wav
            "wav",
            "#",                              # DTMF # to stop early
            int(MAX_RECORDING_SECS * 1000),   # timeout in ms
            0,                                # offset
            "s=1.5",                          # silence detection: 1.5s
        )
        audio_path_full = audio_path if os.path.exists(audio_path) else audio_path

        if not os.path.exists(audio_path_full):
            agi.verbose(f"No audio recorded on turn {turn} — hanging up")
            break

        # 2. Send to backend — STT → LLM → TTS
        try:
            with open(audio_path_full, "rb") as f:
                api_resp = requests.post(
                    f"{BACKEND_URL}/calls/speech",
                    data={"session_id": session_id, "caller_number": caller_number},
                    files={"audio": ("audio.wav", f, "audio/wav")},
                    timeout=30,
                )
            api_resp.raise_for_status()
            result = api_resp.json()
        except Exception as e:
            agi.verbose(f"Backend error: {e}")
            play_static(agi, "sorry_technical_issue")
            break

        os.unlink(audio_path_full)

        # 3. Play synthesised reply
        reply_path = result.get("audio_path", "")
        if reply_path and os.path.exists(reply_path):
            play_audio(agi, reply_path)
        else:
            agi.verbose("No reply audio — ending call")
            break

        # 4. Check for booking or call-end signal
        if result.get("call_outcome") in ("booked", "not_interested"):
            agi.verbose(f"Call outcome: {result['call_outcome']}")
            play_static(agi, "goodbye")
            break

    # ── End session ────────────────────────────────────────────────────────────
    try:
        requests.post(
            f"{BACKEND_URL}/calls/{session_id}/end",
            params={"outcome": "completed"},
            timeout=5,
        )
    except Exception:
        pass

    agi.hangup()
    agi.verbose("AGI complete")


def synthesise_greeting(session_id: str, caller_number: str) -> str | None:
    """
    Ask the backend to synthesise the opening greeting.
    We send a synthetic 'first turn' with empty audio and a special flag.
    The LLM is primed to open with the greeting from the system prompt.
    """
    try:
        resp = requests.post(
            f"{BACKEND_URL}/calls/speech",
            data={
                "session_id": session_id,
                "caller_number": caller_number,
            },
            # Send a 1-byte empty file — backend handles [silence] gracefully
            files={"audio": ("greeting.wav", b"\x00", "audio/wav")},
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json().get("audio_path")
    except Exception:
        return None


def play_audio(agi: AGI, path: str) -> None:
    """Strip .wav extension — Asterisk STREAM FILE does not want it."""
    base = path.replace(".wav", "")
    agi.stream_file(base, escape_digits="#")


def play_static(agi: AGI, sound_name: str) -> None:
    """Play a built-in Asterisk sound file."""
    agi.stream_file(f"custom/{sound_name}", escape_digits="#")


if __name__ == "__main__":
    main()
