import unittest
from converter.distance import DistanceConverter
from converter.temperature import TemperatureConverter
from converter.mass import MassConverter
from converter.currency import CurrencyConverter

class TestConverter(unittest.TestCase):

    def test_distance_conversion(self):
        self.assertAlmostEqual(DistanceConverter.km_to_miles(1), 0.621371)
        self.assertAlmostEqual(DistanceConverter.miles_to_km(1), 1.60934)

    def test_temperature_conversion(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32), 0)

    def test_mass_conversion(self):
        self.assertAlmostEqual(MassConverter.kg_to_lb(1), 2.20462)
        #self.assertAlmostEqual(MassConverter.lb_to_kg(2.20462), 1)

    def test_currency_conversion(self):
        # You would mock the API request in a real test environment
        result = CurrencyConverter.convert('USD', 'EUR', 1)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()