from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Clinician, Medication, MedicationRequest, Patient
from src.enums import MedicationRequestStatus
from src.schema import (
    ClinicianCreate,
    ClinicianDetails,
    MedicationCreate,
    MedicationDetails,
    MedicationRequestCreate,
    MedicationRequestCreationResult,
    MedicationRequestDetails,
    PatientCreate,
)


def medication_request_create(
    session: Session, request: MedicationRequestCreate
) -> MedicationRequestCreationResult:
    medication_request = MedicationRequest(
        patient=_get_or_create_patient(session=session, request=request.patient),
        clinician=_get_or_create_clinician(session=session, request=request.clinician),
        medication=_get_or_create_medication(
            session=session, request=request.medication
        ),
        reason_text=request.reason,
        prescribed_date=request.prescribed_date,
        start_date=request.start_date,
        end_date=request.end_date,
        frequency_per_day=request.frequency_per_day,
        status=request.status,
    )
    session.add(medication_request)
    session.commit()
    session.refresh(medication_request)
    return MedicationRequestCreationResult(id=medication_request.id)


def _get_or_create_patient(session: Session, request: PatientCreate) -> Patient:
    return Patient.get_or_create_by(
        session=session,
        first_name=request.first_name,
        last_name=request.last_name,
        date_of_birth=request.date_of_birth,
        sex=request.sex,
    )


def _get_or_create_clinician(session: Session, request: ClinicianCreate) -> Clinician:
    return Clinician.get_or_create_by(
        session=session,
        first_name=request.first_name,
        last_name=request.last_name,
        registration_id=request.registration_id,
    )


def _get_or_create_medication(
    session: Session, request: MedicationCreate
) -> Medication:
    return Medication.get_or_create_by(
        session=session,
        code=request.code,
        code_name=request.code_name,
        code_system=request.code_system,
        strength_value=request.strength_value,
        strength_unit=request.strength_unit,
        form=request.form,
    )


def medication_request_filter(
    session: Session,
    status: MedicationRequestStatus | None,
    start_date: date | None,
    end_date: date | None,
) -> list[MedicationRequestDetails]:
    queryset = session.query(MedicationRequest)

    if status:
        queryset = queryset.filter(MedicationRequest.status == status)
    if start_date:
        queryset = queryset.filter(MedicationRequest.start_date >= start_date)
    if end_date:
        queryset = queryset.filter(MedicationRequest.end_date <= end_date)

    result = []
    for medication_request in queryset.all():
        result.append(
            MedicationRequestDetails(
                id=medication_request.id,
                reason_text=medication_request.reason_text,
                prescribed_date=medication_request.prescribed_date,
                start_date=medication_request.start_date,
                end_date=medication_request.end_date,
                frequency_per_day=medication_request.frequency_per_day,
                status=medication_request.status,
                clinician=ClinicianDetails(
                    id=medication_request.clinician.id,
                    first_name=medication_request.clinician.first_name,
                    last_name=medication_request.clinician.last_name,
                ),
                medication=MedicationDetails(
                    id=medication_request.medication.id,
                    code_name=medication_request.medication.code_name,
                ),
            )
        )
    return result
