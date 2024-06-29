from datetime import date

from pydantic import BaseModel

from src.enums import MedicationForm, MedicationRequestStatus, Sex


class MedicationRequestCreate(BaseModel):
    patient: "PatientCreate"
    clinician: "ClinicianCreate"
    medication: "MedicationCreate"
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


class ClinicianCreate(BaseModel):
    first_name: str
    last_name: str
    registration_id: str


class MedicationCreate(BaseModel):
    code: str
    code_name: str
    code_system: str
    strength_value: int
    strength_unit: str
    form: MedicationForm


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex


class MedicationRequestCreationResult(BaseModel):
    id: int
