from datetime import date

from pydantic import BaseModel

from src.enums import MedicationRequestStatus


class MedicationRequest(BaseModel):
    patient: "Patient"
    clinician: "Clinician"
    medication: "Medication"
    reason: str
    prescribed_date: date
    start_date: date
    end_date: date | None
    frequency_per_day: int
    status: MedicationRequestStatus


class DateRange(BaseModel):
    start: date
    end: date


class MedicationRequestFilter(BaseModel):
    status: MedicationRequestStatus | None
    date_range: DateRange | None


class MedicationRequestPatch(BaseModel):
    medication_request_reference: str
    end_date: date | None
    frequency: int | None
    status: MedicationRequestStatus | None


class Clinician(BaseModel):
    reference: str


class Medication(BaseModel):
    reference: str


class Patient(BaseModel):
    reference: str
