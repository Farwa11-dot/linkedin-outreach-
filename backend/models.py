from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


# ─── Enums ────────────────────────────────────────────────────────────────────

class CallOutcome(str, Enum):
    booked = "booked"
    callback_requested = "callback_requested"
    not_interested = "not_interested"
    voicemail = "voicemail"
    transferred = "transferred"
    completed = "completed"
    error = "error"


class LeadStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    demo_booked = "demo_booked"
    proposal_sent = "proposal_sent"
    won = "won"
    lost = "lost"
    suppressed = "suppressed"


class ConsentStatus(str, Enum):
    opted_in = "opted_in"
    unknown = "unknown"
    opted_out = "opted_out"
    suppressed = "suppressed"


# ─── Call Models ──────────────────────────────────────────────────────────────

class CallSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    call_id: str                         # Asterisk UniqueID
    caller_number: str
    called_number: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    outcome: CallOutcome = CallOutcome.completed
    transcript: list[dict] = []          # [{role, content, timestamp}]
    lead_id: Optional[UUID] = None
    booking_id: Optional[str] = None
    recording_path: Optional[str] = None


class SpeechRequest(BaseModel):
    session_id: UUID
    audio_path: str                      # path to .wav file
    caller_number: str


class SpeechResponse(BaseModel):
    session_id: UUID
    transcript: str
    llm_reply: str
    audio_reply_path: str                # path to synthesised .wav


class TurnRequest(BaseModel):
    """Single conversational turn."""
    session_id: UUID
    user_text: str
    caller_number: str
    conversation_history: list[dict] = []


class TurnResponse(BaseModel):
    session_id: UUID
    assistant_text: str
    audio_path: str
    call_outcome: Optional[CallOutcome] = None
    booking_requested: bool = False


# ─── Lead Models ──────────────────────────────────────────────────────────────

class LeadCreate(BaseModel):
    business_name: str
    owner_name: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None
    industry: Optional[str] = None
    city: Optional[str] = None
    country: str = "US"
    source: str = "inbound_call"
    consent_status: ConsentStatus = ConsentStatus.unknown
    notes: Optional[str] = None


class Lead(LeadCreate):
    id: UUID = Field(default_factory=uuid4)
    status: LeadStatus = LeadStatus.new
    icp_score: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    icp_score: Optional[int] = None
    owner_name: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    consent_status: Optional[ConsentStatus] = None


# ─── Booking Models ───────────────────────────────────────────────────────────

class BookingRequest(BaseModel):
    lead_id: UUID
    session_id: UUID
    name: str
    email: EmailStr
    phone: str
    preferred_date: Optional[str] = None   # ISO 8601
    preferred_time: Optional[str] = None   # HH:MM
    notes: Optional[str] = None
    event_type_slug: str = "demo-call"


class BookingResult(BaseModel):
    booking_id: str
    calendar_link: str
    meeting_url: Optional[str] = None
    confirmed_at: datetime


# ─── Webhook / n8n Models ────────────────────────────────────────────────────

class CallCompletedEvent(BaseModel):
    event: str = "call.completed"
    session_id: UUID
    caller_number: str
    outcome: CallOutcome
    transcript_summary: str
    lead_id: Optional[UUID] = None
    booking_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
