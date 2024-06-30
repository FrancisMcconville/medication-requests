from datetime import date

from pydantic import BaseModel, Field

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


class ClinicianDetails(BaseModel):
    id: int
    first_name: str
    last_name: str


class MedicationDetails(BaseModel):
    id: int
    code_name: str


class MedicationRequestDetails(BaseModel):
    id: int
    reason_text: str
    prescribed_date: date
    start_date: date
    end_date: date | None
    frequency_per_day: int
    status: MedicationRequestStatus
    clinician: ClinicianDetails
    medication: MedicationDetails


class MedicationRequestUpdate(BaseModel):
    id: int
    end_date: date | None = Field(
        default=None, title="Set this to 1970-01-01 to unset the end_date"
    )
    frequency: int | None = None
    status: MedicationRequestStatus | None = None
