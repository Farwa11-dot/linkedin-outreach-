"""
Voice AI Receptionist — FastAPI entry point.
"""
import os
import asyncio
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers import calls, leads, bookings
from services.stt import STTService
from services.tts import TTSService
from services.llm import LLMService

logger = structlog.get_logger()
settings = get_settings()


# ─── App Lifecycle ────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Voice AI Receptionist backend")

    # Ensure temp audio directory exists
    os.makedirs(settings.audio_temp_dir, exist_ok=True)

    # Pre-load Whisper model (heavy — do once at startup)
    logger.info("Loading Whisper STT model", model=settings.whisper_model)
    app.state.stt = STTService()
    await app.state.stt.load()

    # Pre-load Piper TTS
    logger.info("Loading Piper TTS")
    app.state.tts = TTSService()
    await app.state.tts.load()

    # Initialise LLM client
    app.state.llm = LLMService()
    logger.info("LLM service ready", model=settings.ollama_model)

    yield

    logger.info("Shutting down backend")


# ─── App Instance ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="Voice AI Receptionist",
    version="1.0.0",
    description="Open-source AI phone receptionist with Whisper + Ollama + Piper",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────

app.include_router(calls.router, prefix="/calls", tags=["calls"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])


@app.get("/health")
async def health():
    return {"status": "ok", "model": settings.ollama_model}


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=False,
        log_level="info",
    )
