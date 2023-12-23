from fastapi.testclient import TestClient
from sky_alert.endpoint import app
import unittest
from unittest.mock import patch
import datetime
from typing import Any

client = TestClient(app)


class MockOpenweatherResponse:
    def __init__(self, json_data: dict[str, Any], status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> dict[str, Any]:
        return self.json_data


class TestEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_healthz(self) -> None:
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    @patch("sky_alert.endpoint.requests.get")
    def test_openweather_sun_data(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data = {
            "current": {
                "dt": 1684929490,
                "sunrise": 1684926645,
                "sunset": 1684977332,
            }
        }
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        response = self.client.get("/openweather_sun_data")

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["sunrise"],
            datetime.datetime.utcfromtimestamp(1684926645).isoformat(),
        )
        self.assertEqual(
            response.json()["sunset"],
            datetime.datetime.utcfromtimestamp(1684977332).isoformat(),
        )

    @patch("sky_alert.endpoint.requests.get")
    def test_openweather_sun_data_401(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data: dict[str, Any] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=401
        )

        # WHEN
        response = self.client.get("/openweather_sun_data")
        # THEN
        self.assertEqual(response.status_code, 401)

    @patch("sky_alert.endpoint.requests.get")
    def test_openweather_sun_data_404(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data: dict[str, Any] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=404
        )

        # WHEN
        response = self.client.get("/openweather_sun_data")
        # THEN
        self.assertEqual(response.status_code, 404)
