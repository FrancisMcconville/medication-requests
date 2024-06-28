from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database.main import get_session
from src.schema import (
    MedicationRequest,
    MedicationRequestFilter,
    MedicationRequestPatch,
)

router = APIRouter(prefix="/v1")


@router.post("/medication_request", tags=["MedicationRequest"])
async def post_medication_request(
    post_request: MedicationRequest, session: Session = Depends(get_session)
) -> MedicationRequest:
    return JSONResponse({"status": "todo"})


@router.get("/medication_request", tags=["MedicationRequest"])
async def get_medication_request(
    *,
    medication_request_filter: MedicationRequestFilter,
    session: Session = Depends(get_session)
) -> list[MedicationRequest]:
    return JSONResponse({"status": "todo"})


@router.patch("/medication_request", tags=["MedicationRequest"])
async def patch_medication_request(
    *, patch_request: MedicationRequestPatch, session: Session = Depends(get_session)
) -> MedicationRequest:
    return JSONResponse({"status": "todo"})
