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


class TestSunEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_healthz(self) -> None:
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())
