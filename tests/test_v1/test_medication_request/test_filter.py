import datetime

from src.enums import MedicationRequestStatus
from tests import client
from tests.utils import make_medication_request


class TestMedicationRequestFilter:
    @staticmethod
    def get_medication_request_ids_from_request(params: dict | None = None):
        response = client.get("/v1/medication_request", params=params)
        assert response.status_code == 200, "Expected a successful response"
        response_json = response.json()
        return {record["id"] for record in response_json}

    def test_no_filter_applied_returns_all(self, session):
        # TODO we should paginate this, ALBs will 502 responses which are too large
        expected_count = 3
        for _ in range(expected_count):
            make_medication_request(session)
        response = client.get("/v1/medication_request")
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == expected_count

    def test_filter_by_status_returns_correct_records(self, session):
        expected_completed_status_count = 2

        completed_status_ids: list[int] = []
        for _ in range(expected_completed_status_count):
            completed_request = make_medication_request(
                session, status=MedicationRequestStatus.completed
            )
            completed_status_ids.append(completed_request.id)
        for _ in range(5):
            make_medication_request(session, status=MedicationRequestStatus.active)
        response_ids = self.get_medication_request_ids_from_request(
            params={"status": "completed"}
        )
        assert len(response_ids) == expected_completed_status_count
        assert set(response_ids) == set(completed_status_ids)

    def test_filter_by_end_date_returns_correct_records(self, session):
        end_date_filter = datetime.date(2024, 7, 20)
        expected_count_within_date_range = 2

        expected_match_ids: list[int] = []
        for _ in range(expected_count_within_date_range):
            match_request = make_medication_request(session, end_date=end_date_filter)
            expected_match_ids.append(match_request.id)
        for _ in range(5):
            make_medication_request(
                session, end_date=end_date_filter + datetime.timedelta(days=1)
            )
        response_ids = self.get_medication_request_ids_from_request(
            params={"end_date": end_date_filter.isoformat()}
        )
        assert len(response_ids) == expected_count_within_date_range
        assert set(response_ids) == set(expected_match_ids)

    def test_filter_by_start_date_returns_correct_records(self, session):
        start_date_filter = datetime.date(2024, 6, 1)
        expected_count_within_date_range = 4

        expected_match_ids: list[int] = []
        for _ in range(expected_count_within_date_range):
            match_request = make_medication_request(
                session, start_date=start_date_filter
            )
            expected_match_ids.append(match_request.id)
        for _ in range(5):
            make_medication_request(
                session, start_date=start_date_filter - datetime.timedelta(days=1)
            )
        response_ids = self.get_medication_request_ids_from_request(
            params={"start_date": start_date_filter.isoformat()}
        )
        assert len(response_ids) == expected_count_within_date_range
        assert set(response_ids) == set(expected_match_ids)

    def test_filter_returns_no_records(self, session):
        # implied that the database is empty
        response_ids = self.get_medication_request_ids_from_request()
        assert len(response_ids) == 0
