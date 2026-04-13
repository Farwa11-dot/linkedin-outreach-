"""
/bookings router — manual booking endpoint for the web UI or n8n workflows.
"""
from fastapi import APIRouter, HTTPException

from models import BookingRequest, BookingResult
from services.booking import BookingService

router = APIRouter()
booking_svc = BookingService()


@router.post("/", response_model=BookingResult)
async def create_booking(body: BookingRequest):
    try:
        result = await booking_svc.book(body)
        return result
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
