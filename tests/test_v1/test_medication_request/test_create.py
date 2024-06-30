from pytest import fixture, mark
from sqlalchemy.orm import Session

from src.database.models import Clinician, Medication, MedicationRequest, Patient
from tests import client


class TestMedicationRequestCreate:
    @fixture(scope="class")
    def creation_request_payload(self) -> dict:
        return {
            "patient": {
                "first_name": "Francis",
                "last_name": "McConville",
                "date_of_birth": "1993-06-01",
                "sex": "male",
            },
            "clinician": {
                "first_name": "Robert",
                "last_name": "Hunter",
                "registration_id": "ROBHUNT",
            },
            "medication": {
                "code": "PC101",
                "code_name": "Penicillin",
                "code_system": "medcode",
                "strength_value": 25,
                "strength_unit": "mg",
                "form": "tablet",
            },
            "reason": "Infection",
            "prescribed_date": "2024-06-01",
            "start_date": "2024-06-01",
            "end_date": "2024-06-30",
            "frequency_per_day": 3,
            "status": "active",
        }

    @staticmethod
    def _get_medication_request_from_post_request(
        session: Session, payload: dict | None
    ) -> MedicationRequest:
        response = client.post("/v1/medication_request", json=payload)
        assert (
            response.status_code == 200
        ), f"Expected 200 status_code response but got {response.json()}"
        response_body = response.json()
        assert (
            response_body.get("id") is not None
        ), "Expected response to contain the ID of the created record"
        medication_request: MedicationRequest | None = session.get(
            MedicationRequest, response_body["id"]
        )
        assert medication_request
        return medication_request

    def test_valid_request_creates_matching_database_entry(
        self, creation_request_payload, session
    ):
        medication_request = self._get_medication_request_from_post_request(
            payload=creation_request_payload, session=session
        )
        assert medication_request.reason_text == creation_request_payload["reason"]
        assert (
            medication_request.prescribed_date.isoformat()
            == creation_request_payload["prescribed_date"]
        )
        assert (
            medication_request.start_date.isoformat()
            == creation_request_payload["start_date"]
        )
        assert (
            medication_request.end_date.isoformat()
            == creation_request_payload["end_date"]
        )
        assert (
            medication_request.frequency_per_day
            == creation_request_payload["frequency_per_day"]
        )
        assert medication_request.status.value == creation_request_payload["status"]

        medication: Medication = medication_request.medication
        medication_creation = creation_request_payload["medication"]
        assert medication
        assert medication.code == medication_creation["code"]
        assert medication.code_name == medication_creation["code_name"]
        assert medication.code_system == medication_creation["code_system"]
        assert medication.strength_value == medication_creation["strength_value"]
        assert medication.strength_unit == medication_creation["strength_unit"]
        assert medication.form.value == medication_creation["form"]

        clinician: Clinician = medication_request.clinician
        clinician_creation = creation_request_payload["clinician"]
        assert clinician
        assert clinician.first_name == clinician_creation["first_name"]
        assert clinician.last_name == clinician_creation["last_name"]
        assert clinician.registration_id == clinician_creation["registration_id"]

        patient: Patient = medication_request.patient
        patient_creation = creation_request_payload["patient"]
        assert patient
        assert patient.first_name == patient_creation["first_name"]
        assert patient.last_name == patient_creation["last_name"]
        assert patient.date_of_birth.isoformat() == patient_creation["date_of_birth"]
        assert patient.sex.value == patient_creation["sex"]

    def test_request_for_no_end_date(self, creation_request_payload, session):
        del creation_request_payload["end_date"]
        medication_request = self._get_medication_request_from_post_request(
            payload=creation_request_payload, session=session
        )
        assert medication_request.end_date is None

    def test_request_for_frequency_must_be_positive(
        self, creation_request_payload, session
    ):
        creation_request_payload["frequency_per_day"] = 0
        response = client.post("/v1/medication_request", json=creation_request_payload)
        assert response.status_code == 422
        # TODO expect an informative error message in the body

    @mark.xfail(reason="TODO")
    def test_request_linked_to_new_medication_creates_new_record(self):
        assert False

    @mark.xfail(reason="TODO")
    def test_request_linked_to_existing_medication_uses_existing_record(self):
        assert False

    @mark.xfail(reason="TODO")
    def test_request_linked_to_new_clinician_creates_new_record(self):
        assert False

    @mark.xfail(reason="TODO")
    def test_request_linked_to_existing_clinician_uses_existing_record(self):
        assert False

    @mark.xfail(reason="TODO")
    def test_request_linked_to_new_patient_creates_new_record(self):
        assert False

    @mark.xfail(reason="TODO")
    def test_request_linked_to_existing_patient_uses_existing_record(self):
        assert False
