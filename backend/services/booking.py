"""
Booking service — integrates with Cal.com (self-hosted) or Google Calendar.

Cal.com exposes a REST API identical in structure to the cloud version.
Set CALCOM_BASE_URL to your self-hosted instance (e.g. http://calcom:3000).

Google Calendar is the fallback — set GOOGLE_CALENDAR_CREDENTIALS_PATH
to a service-account JSON file with Calendar API access.
"""
import os
from datetime import datetime, timedelta
from typing import Optional

import httpx
import structlog

from config import get_settings
from models import BookingRequest, BookingResult

logger = structlog.get_logger()
settings = get_settings()


class BookingService:
    """Try Cal.com first; fall back to Google Calendar."""

    async def book(self, req: BookingRequest) -> BookingResult:
        try:
            return await self._calcom_book(req)
        except Exception as exc:
            logger.warning("Cal.com booking failed, trying Google Calendar", error=str(exc))
            return await self._google_book(req)

    # ─── Cal.com ──────────────────────────────────────────────────────────────

    async def _calcom_book(self, req: BookingRequest) -> BookingResult:
        """
        POST /api/v1/bookings to the self-hosted Cal.com instance.

        Requires the event type slug to exist in Cal.com already.
        The eventTypeId is looked up by slug first.
        """
        async with httpx.AsyncClient(base_url=settings.calcom_base_url, timeout=10) as client:
            # 1. Look up event type ID
            resp = await client.get(
                "/api/v1/event-types",
                params={"apiKey": settings.calcom_api_key},
            )
            resp.raise_for_status()
            event_types = resp.json().get("event_types", [])
            event_type_id = next(
                (et["id"] for et in event_types if et["slug"] == req.event_type_slug),
                None,
            )
            if not event_type_id:
                raise ValueError(f"Cal.com event type '{req.event_type_slug}' not found")

            # 2. Build start time
            start_dt = _parse_preferred_datetime(req.preferred_date, req.preferred_time)

            # 3. Create booking
            payload = {
                "eventTypeId": event_type_id,
                "start": start_dt.isoformat(),
                "end": (start_dt + timedelta(minutes=30)).isoformat(),
                "responses": {
                    "name": req.name,
                    "email": req.email,
                    "phone": req.phone,
                    "notes": req.notes or "",
                },
                "timeZone": "UTC",
                "language": "en",
                "metadata": {
                    "lead_id": str(req.lead_id),
                    "session_id": str(req.session_id),
                },
            }
            resp = await client.post(
                "/api/v1/bookings",
                json=payload,
                params={"apiKey": settings.calcom_api_key},
            )
            resp.raise_for_status()
            data = resp.json()

        logger.info("Cal.com booking created", uid=data.get("uid"))
        return BookingResult(
            booking_id=data["uid"],
            calendar_link=f"{settings.calcom_base_url}/booking/{data['uid']}",
            meeting_url=data.get("videoCallData", {}).get("url"),
            confirmed_at=datetime.utcnow(),
        )

    # ─── Google Calendar ──────────────────────────────────────────────────────

    async def _google_book(self, req: BookingRequest) -> BookingResult:
        """
        Insert an event using a Google service account.
        Credentials JSON must be mounted at GOOGLE_CALENDAR_CREDENTIALS_PATH.
        """
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        import asyncio

        start_dt = _parse_preferred_datetime(req.preferred_date, req.preferred_time)
        end_dt = start_dt + timedelta(minutes=30)

        creds = Credentials.from_service_account_file(
            settings.google_calendar_credentials_path,
            scopes=["https://www.googleapis.com/auth/calendar"],
        )
        loop = asyncio.get_event_loop()
        event_id = await loop.run_in_executor(
            None,
            lambda: _insert_google_event(creds, settings.google_calendar_id, req, start_dt, end_dt),
        )

        return BookingResult(
            booking_id=event_id,
            calendar_link=f"https://calendar.google.com/calendar/event?eid={event_id}",
            confirmed_at=datetime.utcnow(),
        )


def _insert_google_event(creds, calendar_id, req: BookingRequest, start_dt, end_dt) -> str:
    from googleapiclient.discovery import build
    service = build("calendar", "v3", credentials=creds, cache_discovery=False)
    event = {
        "summary": f"AI Receptionist Demo — {req.name}",
        "description": f"Phone: {req.phone}\nNotes: {req.notes or ''}",
        "start": {"dateTime": start_dt.isoformat() + "Z", "timeZone": "UTC"},
        "end": {"dateTime": end_dt.isoformat() + "Z", "timeZone": "UTC"},
        "attendees": [{"email": req.email}],
    }
    created = service.events().insert(calendarId=calendar_id, body=event, sendUpdates="all").execute()
    return created["id"]


def _parse_preferred_datetime(date_str: Optional[str], time_str: Optional[str]) -> datetime:
    """
    Parse caller's preferred date/time, defaulting to next business day at 10am UTC.
    """
    if date_str and time_str:
        try:
            return datetime.fromisoformat(f"{date_str}T{time_str}:00")
        except ValueError:
            pass
    # Default: tomorrow at 10:00 UTC
    tomorrow = datetime.utcnow().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return tomorrow
