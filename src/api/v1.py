from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.crud import medication_request_create, medication_request_filter
from src.database.main import get_session
from src.enums import MedicationRequestStatus
from src.schema import (
    MedicationRequestCreate,
    MedicationRequestCreationResult,
    MedicationRequestDetails,
)

router = APIRouter(prefix="/v1")


@router.post("/medication_request", tags=["MedicationRequest"])
async def post_medication_request(
    create_request: MedicationRequestCreate, session: Session = Depends(get_session)
) -> MedicationRequestCreationResult:
    return medication_request_create(request=create_request, session=session)


@router.get("/medication_request", tags=["MedicationRequest"])
async def get_medication_request(
    status: MedicationRequestStatus | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    session: Session = Depends(get_session),
) -> list[MedicationRequestDetails]:
    return medication_request_filter(
        status=status, start_date=start_date, end_date=end_date, session=session
    )


#
# @router.patch("/medication_request", tags=["MedicationRequest"])
# async def patch_medication_request(
#     *, patch_request: MedicationRequestPatch, session: Session = Depends(get_session)
# ) -> MedicationRequest:
#     return JSONResponse({"status": "todo"})
