from sqlalchemy.orm import Session

from src.database.models import Clinician, Medication, MedicationRequest, Patient
from src.schema import (
    ClinicianCreate,
    MedicationCreate,
    MedicationRequestCreate,
    MedicationRequestCreationResult,
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
