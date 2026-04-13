"""
LLM service — Ollama backend (LLaMA 3, Mistral, Phi-3, etc.)

The system prompt is the full Voice AI Receptionist sales prompt.
Conversation history is maintained per call session so the LLM
has full context of the conversation at every turn.
"""
import asyncio
from pathlib import Path

import ollama
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from config import get_settings

logger = structlog.get_logger()
settings = get_settings()

SYSTEM_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"

# Intent keywords that signal the caller wants to book an appointment
BOOKING_INTENTS = [
    "book", "appointment", "schedule", "call back", "demo",
    "meeting", "available", "slot", "calendar", "time",
]


def _load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    # Minimal fallback if file is missing
    return (
        "You are a professional AI receptionist. "
        "Answer helpfully and concisely. "
        "If the caller wants to book an appointment, collect their name, email, "
        "preferred date and time, then confirm."
    )


SYSTEM_PROMPT = _load_system_prompt()


class LLMService:
    """Async wrapper around the Ollama Python client."""

    def __init__(self):
        self._client = ollama.AsyncClient(host=settings.ollama_base_url)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    async def chat(
        self,
        user_message: str,
        conversation_history: list[dict],
    ) -> tuple[str, bool]:
        """
        Send a message and receive the assistant reply.

        Args:
            user_message: The caller's transcribed speech.
            conversation_history: List of {role, content} dicts for this call.

        Returns:
            Tuple of (assistant_text, booking_requested).
            booking_requested is True when the LLM reply indicates the caller
            wants to schedule an appointment.
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history,
            {"role": "user", "content": user_message},
        ]

        response = await self._client.chat(
            model=settings.ollama_model,
            messages=messages,
            options={
                "temperature": settings.ollama_temperature,
                "num_predict": settings.ollama_max_tokens,
                "stop": ["<|eot_id|>", "<|end_of_text|>"],
            },
        )

        reply_text: str = response["message"]["content"].strip()
        booking_requested = self._detect_booking_intent(user_message, reply_text)

        logger.info(
            "LLM turn complete",
            model=settings.ollama_model,
            user_chars=len(user_message),
            reply_chars=len(reply_text),
            booking_requested=booking_requested,
        )
        return reply_text, booking_requested

    async def stream_chat(
        self,
        user_message: str,
        conversation_history: list[dict],
    ):
        """
        Streaming variant — yields text chunks as they arrive.
        Useful for reducing time-to-first-audio in the voice pipeline.
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history,
            {"role": "user", "content": user_message},
        ]

        full_reply = []
        async for chunk in await self._client.chat(
            model=settings.ollama_model,
            messages=messages,
            stream=True,
            options={
                "temperature": settings.ollama_temperature,
                "num_predict": settings.ollama_max_tokens,
            },
        ):
            delta = chunk["message"]["content"]
            full_reply.append(delta)
            yield delta

        reply_text = "".join(full_reply)
        logger.info("LLM stream complete", reply_chars=len(reply_text))

    async def summarise_call(self, transcript: list[dict]) -> str:
        """
        Produce a short summary of the call for CRM logging and n8n triggers.
        """
        conversation = "\n".join(
            f"{t['role'].upper()}: {t['content']}" for t in transcript
        )
        prompt = (
            f"Summarise this call transcript in 2–3 sentences. "
            f"Include: caller intent, outcome, and any follow-up needed.\n\n{conversation}"
        )
        response = await self._client.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "system", "content": "You are a concise call summariser. Output plain text only."},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.1, "num_predict": 200},
        )
        return response["message"]["content"].strip()

    @staticmethod
    def _detect_booking_intent(user_text: str, assistant_text: str) -> bool:
        combined = (user_text + " " + assistant_text).lower()
        return any(kw in combined for kw in BOOKING_INTENTS)
