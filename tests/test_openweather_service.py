import unittest
from unittest.mock import patch
import uuid
from typing import Any
from sky_alert.openweather_service import OpenweatherService
from tests.test_constants import MOCK_OPENWEATHER_RESPONSE_JSON, HOURS_IN_DAY
import datetime


class MockOpenweatherResponse:
    def __init__(self, json_data: dict[str, Any], status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> dict[str, Any]:
        return self.json_data


class TestOpenweatherService(unittest.TestCase):
    def setUp(self) -> None:
        self.ows = OpenweatherService()

    @patch("sky_alert.openweather_service.requests.get")
    def test_populate_for_coord_success(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        # WHEN
        response = self.ows.populate_for_coord(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.ows.most_recent_weather[(sample_lat, sample_lon)], mock_json_data
        )

    @patch("sky_alert.openweather_service.requests.get")
    def test_populate_for_coord_401(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=401
        )

        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        # WHEN
        response = self.ows.populate_for_coord(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertEqual(response.status_code, 401)
        self.assertFalse((sample_lat, sample_lon) in self.ows.most_recent_weather)

    @patch("sky_alert.openweather_service.requests.get")
    def test_populate_for_coord_404(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=404
        )

        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        # WHEN
        response = self.ows.populate_for_coord(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertEqual(response.status_code, 404)
        self.assertFalse((sample_lat, sample_lon) in self.ows.most_recent_weather)

    @patch("sky_alert.openweather_service.requests.get")
    def test_populate_for_coord_500(self, mock_get: Any) -> None:
        # GIVEN
        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=500
        )

        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        # WHEN
        response = self.ows.populate_for_coord(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertEqual(response.status_code, 500)
        self.assertFalse((sample_lat, sample_lon) in self.ows.most_recent_weather)

    @patch("sky_alert.openweather_service.requests.get")
    def test_update_most_recent_weather_with_no_data(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        self.ows.update_most_recent_weather(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertTrue((sample_lat, sample_lon) in self.ows.most_recent_weather)
        mock_get.assert_called_once()

    @patch("sky_alert.openweather_service.requests.get")
    def test_update_most_recent_weather_with_data(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        self.ows.most_recent_weather[
            (sample_lat, sample_lon)
        ] = MOCK_OPENWEATHER_RESPONSE_JSON

        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        self.ows.update_most_recent_weather(lat=sample_lat, lon=sample_lon)

        # THEN
        self.assertTrue((sample_lat, sample_lon) in self.ows.most_recent_weather)
        self.assertFalse(mock_get.called)


class TestSunDataParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.ows = OpenweatherService()

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_sunrise_sunset_from_json_update_not_called(
        self, mock_get: Any
    ) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        self.ows.most_recent_weather[
            (sample_lat, sample_lon)
        ] = MOCK_OPENWEATHER_RESPONSE_JSON

        # WHEN
        response = self.ows.get_sun_data_today(lat=sample_lat, lon=sample_lon)

        # THEN
        sunrise_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON.get("current").get("sunrise")
        )
        sunset_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["current"]["sunset"]
        )
        self.assertEqual(response.sunrise, sunrise_datetime)
        self.assertEqual(response.sunset, sunset_datetime)

        # mock_get shouldn't have been called since we have data with sample_lat and sample_lon
        self.assertFalse(mock_get.called)

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_sunrise_sunset_from_json_update_called(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        response = self.ows.get_sun_data_today(lat=sample_lat, lon=sample_lon)

        # THEN
        sunrise_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["current"]["sunrise"]
        )
        sunset_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["current"]["sunset"]
        )
        self.assertEqual(response.sunrise, sunrise_datetime)
        self.assertEqual(response.sunset, sunset_datetime)

        # mock_get should have been called since we don't have data with sample_lat and sample_lon
        mock_get.assert_called_once()

    @patch("sky_alert.openweather_service.requests.get")
    def test_given_sunrise_sunset_without_data(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        with self.assertRaises(KeyError):
            response = self.ows.get_sun_data_today(lat=sample_lat, lon=sample_lon)


class TestMoonDataParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.ows = OpenweatherService()

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_moonrise_moonset_from_json_update_not_called(
        self, mock_get: Any
    ) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        self.ows.most_recent_weather[
            (sample_lat, sample_lon)
        ] = MOCK_OPENWEATHER_RESPONSE_JSON

        # WHEN
        response = self.ows.get_moon_data_today(lat=sample_lat, lon=sample_lon)

        # THEN
        moonrise_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moonrise"]
        )
        moonset_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moonset"]
        )
        moon_phase = MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moon_phase"]
        self.assertEqual(response.moonrise, moonrise_datetime)
        self.assertEqual(response.moonset, moonset_datetime)
        self.assertEqual(response.moonphase, moon_phase)

        # mock_get shouldn't have been called since we have data with sample_lat and sample_lon
        self.assertFalse(mock_get.called)

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_moonrise_moonset_from_json_update_called(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        response = self.ows.get_moon_data_today(lat=sample_lat, lon=sample_lon)

        # THEN
        moonrise_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moonrise"]
        )
        moonset_datetime = datetime.datetime.utcfromtimestamp(
            MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moonset"]
        )

        self.assertEqual(response.moonrise, moonrise_datetime)
        self.assertEqual(response.moonset, moonset_datetime)
        self.assertEqual(
            response.moonphase, MOCK_OPENWEATHER_RESPONSE_JSON["daily"][0]["moon_phase"]
        )

        # mock_get should have been called since we don't have data with sample_lat and sample_lon
        mock_get.assert_called_once()

    @patch("sky_alert.openweather_service.requests.get")
    def test_given_moonrise_moonset_without_data(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        with self.assertRaises(KeyError):
            response = self.ows.get_moon_data_today(lat=sample_lat, lon=sample_lon)


class TestCloudDataParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.ows = OpenweatherService()

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_hourly_cloud_data_from_json_update_not_called(
        self, mock_get: Any
    ) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        self.ows.most_recent_weather[
            (sample_lat, sample_lon)
        ] = MOCK_OPENWEATHER_RESPONSE_JSON

        # WHEN
        response = self.ows.get_cloud_data_24_hours(lat=sample_lat, lon=sample_lon)

        # THEN
        cloud_data = []
        for i in range(HOURS_IN_DAY):
            cloud_data.append(MOCK_OPENWEATHER_RESPONSE_JSON["hourly"][i]["clouds"])

        self.assertEqual(response.cloud_cover, cloud_data)

        # mock_get shouldn't have been called since we have data with sample_lat and sample_lon
        self.assertFalse(mock_get.called)

    @patch("sky_alert.openweather_service.requests.get")
    def test_get_hourly_cloud_data_from_json_update_called(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data = MOCK_OPENWEATHER_RESPONSE_JSON
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        response = self.ows.get_cloud_data_24_hours(lat=sample_lat, lon=sample_lon)

        # THEN
        cloud_data = []
        for i in range(HOURS_IN_DAY):
            cloud_data.append(MOCK_OPENWEATHER_RESPONSE_JSON["hourly"][i]["clouds"])

        self.assertEqual(response.cloud_cover, cloud_data)

        # mock_get should have been called since we don't have data with sample_lat and sample_lon
        mock_get.assert_called_once()

    @patch("sky_alert.openweather_service.requests.get")
    def test_given_clouds_without_data(self, mock_get: Any) -> None:
        # GIVEN
        sample_lat = str(uuid.uuid4())
        sample_lon = str(uuid.uuid4())

        mock_json_data: dict[str, str] = {}
        mock_get.return_value = MockOpenweatherResponse(
            json_data=mock_json_data, status_code=200
        )

        # WHEN
        with self.assertRaises(KeyError):
            response = self.ows.get_cloud_data_24_hours(lat=sample_lat, lon=sample_lon)
