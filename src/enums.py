from enum import Enum


class MedicationForm(Enum):
    powder = "powder"
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"


class Sex(Enum):
    male = "male"
    female = "female"


class MedicationRequestStatus(Enum):
    active = "active"
    on_hold = "on-hold"
    cancelled = "cancelled"
    completed = "completed"
