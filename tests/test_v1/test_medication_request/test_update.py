import datetime

from src.database.models import MedicationRequest
from src.enums import MedicationRequestStatus
from tests import client
from tests.utils import make_medication_request


class TestMedicationRequestPatch:
    def test_id_does_not_exist_returns_error(self):
        response = client.patch(
            "/v1/medication_request", json={"id": 999, "frequency": 1}
        )
        assert response.status_code == 404

    def test_end_date_after_start_date_update_is_applied_and_returned(self, session):
        start_date = datetime.date(2024, 6, 30)
        end_date = datetime.date(2024, 7, 31)
        medication_request = make_medication_request(
            session=session, start_date=start_date, end_date=datetime.date(2024, 7, 20)
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "end_date": end_date.isoformat()},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json.get("end_date") == end_date.isoformat()
        updated_medication_request = session.get(MedicationRequest, response_json["id"])
        session.refresh(updated_medication_request)
        assert updated_medication_request.end_date == end_date

    def test_end_date_before_start_date_returns_validation_error(self, session):
        start_date = datetime.date(2024, 6, 30)
        end_date = datetime.date(2024, 6, 29)
        medication_request = make_medication_request(
            session=session, start_date=start_date
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "end_date": end_date.isoformat()},
        )
        assert response.status_code == 422
        # TODO should see a reasonable error message in the body

    def test_end_date_can_be_unset(self, session):
        start_date = datetime.date(2024, 6, 30)
        end_date = datetime.date(1970, 1, 1)
        medication_request = make_medication_request(
            session=session,
            start_date=start_date,
            end_date=datetime.datetime.now().date(),
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "end_date": end_date.isoformat()},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json.get("end_date") is None
        updated_medication_request = session.get(MedicationRequest, response_json["id"])
        session.refresh(updated_medication_request)
        assert updated_medication_request.end_date is None

    def test_positive_frequency_update_is_applied_and_returned(self, session):
        frequency_update = 3
        medication_request = make_medication_request(
            session=session, frequency=1, end_date=datetime.datetime.now().date()
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "frequency": frequency_update},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json.get("frequency_per_day") == frequency_update
        updated_medication_request = session.get(MedicationRequest, response_json["id"])
        session.refresh(updated_medication_request)
        assert updated_medication_request.frequency_per_day == frequency_update

    def test_negative_frequency_update_returns_error(self, session):
        frequency_update = -1
        medication_request = make_medication_request(
            session=session, frequency=1, end_date=datetime.datetime.now().date()
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "frequency": frequency_update},
        )
        assert response.status_code == 422

    def test_status_update_is_applied_and_returned(self, session):
        # TODO may want to prevent moving from completed back to done etc
        status_update = "completed"
        medication_request = make_medication_request(
            session=session, frequency=1, status=MedicationRequestStatus.active
        )
        response = client.patch(
            "/v1/medication_request",
            json={"id": medication_request.id, "status": status_update},
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json.get("status") == status_update
        updated_medication_request = session.get(MedicationRequest, response_json["id"])
        session.refresh(updated_medication_request)
        assert updated_medication_request.status.value == status_update
