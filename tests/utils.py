from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Clinician, Medication, MedicationRequest, Patient
from src.enums import MedicationForm, MedicationRequestStatus, Sex


def get_dummy_medication_request() -> MedicationRequest:
    return MedicationRequest(
        reason_text="dummy reason",
        prescribed_date=datetime.now().date(),
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        frequency_per_day=1,
        status=MedicationRequestStatus.active,
        clinician=get_dummy_clinician(),
        medication=get_dummy_medication(),
        patient=get_dummy_patient(),
    )


def make_medication_request(session: Session, **kwargs) -> MedicationRequest:
    dummy_request = get_dummy_medication_request()
    for key, value in kwargs.items():
        setattr(dummy_request, key, value)
    session.add(dummy_request)
    session.commit()
    session.refresh(dummy_request)
    return dummy_request


def get_dummy_clinician() -> Clinician:
    return Clinician(
        first_name="dummy clinician first name",
        last_name="dummy clinician last name",
        registration_id="dummy",
    )


def get_dummy_medication() -> Medication:
    return Medication(
        code="DUMMY#1",
        code_name="Dummy medication",
        code_system="dummy",
        strength_value="5",
        strength_unit="mg",
        form=MedicationForm.syrup,
    )


def get_dummy_patient() -> Patient:
    return Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth=datetime.now().date() - timedelta(days=365 * 30),
        sex=Sex.male,
    )
