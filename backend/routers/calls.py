"""
/calls router — core voice pipeline endpoints consumed by the Asterisk AGI script.

Flow per turn:
  1. AGI posts audio file → POST /calls/speech  (STT + LLM + TTS)
  2. AGI polls status     → GET  /calls/{session_id}
  3. Call ends            → POST /calls/{session_id}/end
"""
import os
import uuid
from datetime import datetime
from typing import Optional

import structlog
from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, Request, UploadFile

from config import get_settings
from models import (
    CallCompletedEvent,
    CallOutcome,
    CallSession,
    LeadCreate,
    SpeechResponse,
    TurnRequest,
    TurnResponse,
)
from services import crm
from services.booking import BookingService
from services.llm import LLMService
from services.stt import STTService
from services.tts import TTSService

router = APIRouter()
logger = structlog.get_logger()
settings = get_settings()

# In-memory conversation store (per call session).
# In production swap this for Redis or Supabase.
_sessions: dict[str, dict] = {}

booking_svc = BookingService()


def _get_services(request: Request) -> tuple[STTService, TTSService, LLMService]:
    return request.app.state.stt, request.app.state.tts, request.app.state.llm


# ─── Start a Call Session ─────────────────────────────────────────────────────

@router.post("/start", response_model=dict)
async def start_call(
    call_id: str = Form(...),
    caller_number: str = Form(...),
    called_number: str = Form(...),
):
    """
    Called by Asterisk AGI at the start of every inbound call.
    Creates a session and returns the greeting audio path.
    """
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "call_id": call_id,
        "caller_number": caller_number,
        "called_number": called_number,
        "history": [],
        "started_at": datetime.utcnow(),
        "booking_data": {},
    }

    session = CallSession(
        session_id=session_id,
        call_id=call_id,
        caller_number=caller_number,
        called_number=called_number,
    )
    await crm.create_call_session(session)

    logger.info("Call session started", session_id=session_id, caller=caller_number)
    return {"session_id": session_id, "status": "started"}


# ─── Process a Speech Turn ────────────────────────────────────────────────────

@router.post("/speech", response_model=TurnResponse)
async def process_speech(
    request: Request,
    session_id: str = Form(...),
    caller_number: str = Form(...),
    audio: UploadFile = File(...),
):
    """
    Receives a WAV audio chunk from Asterisk, runs the full pipeline:
    Whisper STT → Ollama LLM → Piper TTS
    Returns the path to the synthesised reply audio.
    """
    stt, tts, llm = _get_services(request)

    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    sess = _sessions[session_id]

    # 1. Save uploaded audio to temp file
    audio_path = os.path.join(settings.audio_temp_dir, f"{session_id}_in.wav")
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    # 2. STT — Whisper transcribes caller speech
    user_text = await stt.transcribe(audio_path)
    os.unlink(audio_path)

    if not user_text.strip():
        # Silence or noise — ask the caller to repeat
        user_text = "[silence]"

    logger.info("Caller said", session_id=session_id, text=user_text[:120])

    # 3. LLM — generate response
    reply_text, booking_requested = await llm.chat(user_text, sess["history"])

    # 4. Update conversation history
    sess["history"].append({"role": "user", "content": user_text})
    sess["history"].append({"role": "assistant", "content": reply_text})

    # 5. Detect booking data collection completion
    call_outcome = None
    booking_data = sess.get("booking_data", {})

    if booking_requested:
        # Extract booking fields from LLM reply using simple keyword scan
        _extract_booking_fields(reply_text, user_text, booking_data)

    if _booking_data_complete(booking_data):
        call_outcome = CallOutcome.booked

    # 6. TTS — synthesise reply audio
    audio_reply_path = await tts.synthesise(
        reply_text,
        output_path=os.path.join(settings.audio_temp_dir, f"{session_id}_out.wav"),
    )

    # 7. Append turn to CRM transcript
    now = datetime.utcnow().isoformat()
    turn_transcript = [
        {"role": "user", "content": user_text, "timestamp": now},
        {"role": "assistant", "content": reply_text, "timestamp": now},
    ]
    await crm.update_call_session(
        session_id,
        transcript=sess["history"],
    )

    return TurnResponse(
        session_id=session_id,
        assistant_text=reply_text,
        audio_path=audio_reply_path,
        call_outcome=call_outcome,
        booking_requested=booking_requested,
    )


# ─── End a Call ───────────────────────────────────────────────────────────────

@router.post("/{session_id}/end")
async def end_call(
    session_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    outcome: CallOutcome = CallOutcome.completed,
):
    """
    Called by Asterisk AGI when the call hangs up.
    Triggers CRM update, booking creation, and n8n workflow.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    sess = _sessions.pop(session_id)
    _, _, llm = _get_services(request)

    now = datetime.utcnow()
    background_tasks.add_task(
        _finalise_call,
        session_id=session_id,
        sess=sess,
        llm=llm,
        outcome=outcome,
        ended_at=now,
    )

    return {"status": "ended", "session_id": session_id}


async def _finalise_call(session_id, sess, llm, outcome, ended_at):
    """Background task — runs after call hangs up."""
    import httpx

    # 1. Summarise transcript
    summary = await llm.summarise_call(sess["history"])

    # 2. Upsert lead
    lead_id = await crm.upsert_lead(
        LeadCreate(
            business_name="Unknown (inbound call)",
            phone=sess["caller_number"],
            source="inbound_call",
        )
    )

    # 3. Create booking if data is complete
    booking_id = None
    booking_data = sess.get("booking_data", {})
    if _booking_data_complete(booking_data):
        from models import BookingRequest
        result = await booking_svc.book(
            BookingRequest(
                lead_id=lead_id,
                session_id=session_id,
                name=booking_data.get("name", "Caller"),
                email=booking_data.get("email", "unknown@unknown.com"),
                phone=sess["caller_number"],
                preferred_date=booking_data.get("date"),
                preferred_time=booking_data.get("time"),
            )
        )
        booking_id = result.booking_id
        outcome = CallOutcome.booked

    # 4. Update CRM
    await crm.update_call_session(
        session_id,
        ended_at=ended_at,
        outcome=outcome,
        lead_id=lead_id,
        booking_id=booking_id,
        summary=summary,
    )

    # 5. Trigger n8n webhook
    event = CallCompletedEvent(
        session_id=session_id,
        caller_number=sess["caller_number"],
        outcome=outcome,
        transcript_summary=summary,
        lead_id=lead_id,
        booking_id=booking_id,
    )
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(
                f"{settings.n8n_webhook_base_url}/call-completed",
                json=event.model_dump(mode="json"),
            )
    except Exception as exc:
        logger.warning("n8n webhook failed", error=str(exc))

    logger.info("Call finalised", session_id=session_id, outcome=outcome.value, lead_id=str(lead_id))


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _extract_booking_fields(reply: str, user_input: str, booking_data: dict) -> None:
    """
    Very lightweight extraction — a production system would use
    a structured LLM call with JSON mode output instead.
    """
    import re
    combined = (reply + " " + user_input).lower()

    if "email" not in booking_data:
        email_match = re.search(r"[\w.\-]+@[\w.\-]+\.\w+", combined)
        if email_match:
            booking_data["email"] = email_match.group(0)

    if "name" not in booking_data:
        name_match = re.search(r"my name is ([a-z ]+)", combined)
        if name_match:
            booking_data["name"] = name_match.group(1).strip().title()

    if "date" not in booking_data:
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", combined)
        if date_match:
            booking_data["date"] = date_match.group(1)

    if "time" not in booking_data:
        time_match = re.search(r"(\d{1,2}:\d{2})", combined)
        if time_match:
            booking_data["time"] = time_match.group(1)


def _booking_data_complete(booking_data: dict) -> bool:
    return all(k in booking_data for k in ("name", "email"))
