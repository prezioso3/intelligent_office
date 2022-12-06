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