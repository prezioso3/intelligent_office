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

    @patch.object(GPIO, 'input')
    def test_light_level_under_min(self, mock_light_level):
        mock_light_level.return_value = 480
        self.io.manage_light_level()
        self.assertTrue(self.io.light_on)

    @patch.object(GPIO, 'input')
    def test_light_level_above_max(self, mock_light_level):
        mock_light_level.return_value = 580
        self.io.manage_light_level()
        self.assertFalse(self.io.light_on)

    @patch.object(GPIO, 'input')
    def test_light_vacant_quadrants(self, mock_sensor_values):
        mock_sensor_values.side_effect = [0,0,0,0]
        num_occ = self.io.get_occupied_quadrants()
        self.assertEqual(0, num_occ)

    @patch.object(GPIO, 'input')
    def test_light_one_quadrant_occupied(self, mock_sensor_values):
        mock_sensor_values.side_effect = [1, 0, 0, 0]
        num_occ = self.io.get_occupied_quadrants()
        self.assertEqual(1, num_occ)

    @patch.object(GPIO, 'input')
    def test_air_quality_CO2_under_min(self, mock_carbon_dioxide):
        mock_carbon_dioxide.return_value = 490
        self.io.monitor_air_quality()
        self.assertFalse(self.io.fan_switch_on)

    @patch.object(GPIO, 'input')
    def test_air_quality_CO2_above_max(self, mock_carbon_dioxide):
        mock_carbon_dioxide.return_value = 830
        self.io.monitor_air_quality()
        self.assertTrue(self.io.fan_switch_on)