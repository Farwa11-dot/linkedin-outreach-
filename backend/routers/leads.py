"""
/leads router — CRUD endpoints for the CRM lead database.
"""
from uuid import UUID

from fastapi import APIRouter, HTTPException

from models import Lead, LeadCreate, LeadUpdate, LeadStatus
from services import crm

router = APIRouter()


@router.post("/", response_model=dict)
async def create_lead(body: LeadCreate):
    lead_id = await crm.upsert_lead(body)
    return {"lead_id": str(lead_id)}


@router.patch("/{lead_id}", response_model=dict)
async def update_lead(lead_id: UUID, body: LeadUpdate):
    await crm.update_lead(lead_id, body)
    return {"status": "updated"}


@router.post("/{lead_id}/suppress", response_model=dict)
async def suppress_lead(lead_id: UUID):
    """Mark a lead as suppressed (opt-out / do not contact)."""
    from models import ConsentStatus
    await crm.update_lead(
        lead_id,
        LeadUpdate(
            status=LeadStatus.suppressed,
            consent_status=ConsentStatus.suppressed,
        ),
    )
    return {"status": "suppressed"}
