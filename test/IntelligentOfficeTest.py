import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from mock.RTC import RTC
from IntelligentOffice import IntelligentOffice
from IntelligentOfficeError import IntelligentOfficeError


class IntelligentOfficeTest(unittest.TestCase):
    """
    Define your test cases here
    """

    def setUp(self) -> None:  # called one time before all test case
        self.io = IntelligentOffice()

    @patch.object(GPIO, "input")
    def test_quadrant_occupancy_1(self, mock_sensor_value):
        mock_sensor_value.return_value = 4
        res = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertTrue(res)

    @patch.object(GPIO, "input")
    def test_quadrant_occupancy_empty_1(self, mock_sensor_value):
        mock_sensor_value.return_value = 0
        res = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertFalse(res)

    @patch.object(GPIO, "input")
    def test_quadrant_occupancy_2(self, mock_sensor_value):
        mock_sensor_value.return_value = 12
        res = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_2)
        self.assertTrue(res)

    @patch.object(GPIO, "input")
    def test_quadrant_occupancy_empty_2(self, mock_sensor_value):
        mock_sensor_value.return_value = 0
        res = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_2)
        self.assertFalse(res)

    def test_quadrant_occupancy_wrong_pin(self):
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, 50)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_open(self, mock_time, mock_day):
        mock_day.return_value = 'MONDAY'
        mock_time.return_value = "16:28:18"
        self.io.manage_blinds_based_on_time()
        self.assertTrue(self.io.blinds_open)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_closed(self, mock_time, mock_day):
        mock_day.return_value = 'SUNDAY'
        mock_time.return_value = "12:11:01"
        self.io.manage_blinds_based_on_time()
        self.assertFalse(self.io.blinds_open)