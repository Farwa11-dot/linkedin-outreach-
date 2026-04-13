"""
CRM service — writes call data, leads, and transcripts to PostgreSQL via asyncpg.

Uses raw asyncpg for performance. Supabase's REST API can be used
as an alternative by swapping the write methods below to use
the supabase-py client.
"""
import json
import hashlib
from datetime import datetime
from typing import Optional
from uuid import UUID

import asyncpg
import structlog

from config import get_settings
from models import CallSession, Lead, LeadCreate, LeadUpdate, CallOutcome

logger = structlog.get_logger()
settings = get_settings()

_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        # Strip the +asyncpg dialect prefix for asyncpg native URL
        dsn = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        _pool = await asyncpg.create_pool(dsn=dsn, min_size=2, max_size=10)
    return _pool


# ─── Call Logging ─────────────────────────────────────────────────────────────

async def create_call_session(session: CallSession) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO call_sessions (
                session_id, call_id, caller_number, called_number,
                started_at, outcome, transcript, lead_id
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (session_id) DO NOTHING
            """,
            session.session_id,
            session.call_id,
            _hash_pii(session.caller_number),
            session.called_number,
            session.started_at,
            session.outcome.value,
            json.dumps(session.transcript),
            session.lead_id,
        )
    logger.info("Call session created", session_id=str(session.session_id))


async def update_call_session(
    session_id: UUID,
    *,
    ended_at: Optional[datetime] = None,
    outcome: Optional[CallOutcome] = None,
    transcript: Optional[list] = None,
    lead_id: Optional[UUID] = None,
    booking_id: Optional[str] = None,
    summary: Optional[str] = None,
) -> None:
    pool = await get_pool()
    updates = {}
    if ended_at:
        updates["ended_at"] = ended_at
    if outcome:
        updates["outcome"] = outcome.value
    if transcript is not None:
        updates["transcript"] = json.dumps(transcript)
    if lead_id:
        updates["lead_id"] = lead_id
    if booking_id:
        updates["booking_id"] = booking_id
    if summary:
        updates["summary"] = summary

    if not updates:
        return

    set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(updates))
    values = [session_id] + list(updates.values())

    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE call_sessions SET {set_clause} WHERE session_id = $1",
            *values,
        )


# ─── Lead Management ─────────────────────────────────────────────────────────

async def upsert_lead(lead_data: LeadCreate) -> UUID:
    """
    Insert a new lead or return the existing lead_id if the phone number
    has been seen before.
    """
    pool = await get_pool()
    phone_hash = _hash_pii(lead_data.phone)

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM leads WHERE phone_hash = $1", phone_hash
        )
        if row:
            return row["id"]

        lead = Lead(**lead_data.model_dump())
        await conn.execute(
            """
            INSERT INTO leads (
                id, business_name, owner_name, phone_hash,
                email_hash, industry, city, country,
                source, consent_status, notes, status, created_at, updated_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
            """,
            lead.id,
            lead.business_name,
            lead.owner_name,
            phone_hash,
            _hash_pii(lead.email) if lead.email else None,
            lead.industry,
            lead.city,
            lead.country,
            lead.source,
            lead.consent_status.value,
            lead.notes,
            lead.status.value,
            lead.created_at,
            lead.updated_at,
        )
        logger.info("Lead created", lead_id=str(lead.id))
        return lead.id


async def update_lead(lead_id: UUID, update: LeadUpdate) -> None:
    pool = await get_pool()
    data = update.model_dump(exclude_none=True)
    if not data:
        return
    set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(data))
    values = [lead_id] + list(data.values())
    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE leads SET {set_clause}, updated_at = NOW() WHERE id = $1",
            *values,
        )


# ─── PII Hashing (Compliance Rule 4) ─────────────────────────────────────────

def _hash_pii(value: Optional[str]) -> Optional[str]:
    """SHA-256 hash of PII fields before storing. Never log raw PII."""
    if not value:
        return None
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()
