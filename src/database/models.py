from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.enums import MedicationForm, MedicationRequestStatus, Sex


class Base(DeclarativeBase): ...


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[Sex] = mapped_column(Enum(Sex), nullable=False)


class Clinician(Base):
    __tablename__ = "clinicians"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    registration_id: Mapped[str] = mapped_column(String, index=True, nullable=False)


class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    code_name: Mapped[str] = mapped_column(String, nullable=False)
    code_system: Mapped[str] = mapped_column(String, nullable=False)
    # TODO Is this nullable? do all medications have a strength?
    strength_value: Mapped[int] = mapped_column(Integer, nullable=False)
    strength_unit: Mapped[str] = mapped_column(String, nullable=False)
    form: Mapped[MedicationForm] = mapped_column(Enum(MedicationForm), nullable=False)


class MedicationRequest(Base):
    __tablename__ = "medication_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = ForeignKey("patients.id", index=True)
    patient: Mapped[Patient] = relationship(
        Patient, back_populates="medication_requests"
    )

    clinician_id: Mapped[int] = ForeignKey("clinicians.id", index=True)
    clinician: Mapped[Clinician] = relationship(
        Clinician, back_populates="medication_requests"
    )

    medication_id: Mapped[int] = ForeignKey("medications.id", index=True)
    medication: Mapped[Medication] = relationship(
        Medication, back_populates="medication_requests"
    )

    reason_text: Mapped[str] = mapped_column(Text, nullable=False)
    prescribed_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    frequency_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[MedicationRequestStatus] = mapped_column(
        Enum(MedicationRequestStatus), nullable=False
    )
