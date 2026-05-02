import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from phone_tracker.core.validator import PhoneValidator
from phone_tracker.core.provider_lookup import ProviderLookup, GeolocationLookup
from phone_tracker.core.risk_analysis import RiskAnalyzer
from phone_tracker.utils.formatter import PhoneFormatter


class TestPhoneValidator(unittest.TestCase):
    def setUp(self):
        self.validator = PhoneValidator()
    
    def test_international_format(self):
        is_valid, _, standardized = self.validator.validate("+27123456789")
        self.assertTrue(is_valid)
        self.assertEqual(standardized, "+27123456789")
    
    def test_national_format_with_zero(self):
        is_valid, _, standardized = self.validator.validate("0123456789")
        self.assertTrue(is_valid)
        self.assertEqual(standardized, "+27123456789")
    
    def test_invalid_format(self):
        is_valid, _, _ = self.validator.validate("invalid")
        self.assertFalse(is_valid)
    
    def test_empty_input(self):
        is_valid, _, _ = self.validator.validate("")
        self.assertFalse(is_valid)
    
    def test_extract_prefix(self):
        prefix = self.validator.extract_prefix("+27123456789")
        self.assertEqual(prefix, "12")
    
    def test_number_type_detection(self):
        number_type = self.validator.get_number_type("+27612345678")
        self.assertEqual(number_type, "mobile")
        number_type = self.validator.get_number_type("+27112345678")
        self.assertEqual(number_type, "landline")


class TestProviderLookup(unittest.TestCase):
    def setUp(self):
        self.lookup = ProviderLookup()
    
    def test_identify_provider(self):
        provider, code = self.lookup.identify_provider("+27612345678")
        self.assertIn(provider, ["MTN", "Vodacom", "Cell C", "Telkom", "Rain", "Unknown"])
    
    def test_get_all_operators(self):
        operators = self.lookup.get_all_operators()
        self.assertIsInstance(operators, dict)
        self.assertGreater(len(operators), 0)


class TestGeolocationLookup(unittest.TestCase):
    def setUp(self):
        self.lookup = GeolocationLookup()
    
    def test_estimate_region(self):
        region, city = self.lookup.estimate_region("+27112345678")
        self.assertIsInstance(region, str)
        self.assertIsInstance(city, str)
    
    def test_get_coordinates(self):
        coords = self.lookup.get_approximate_coordinates("Gauteng")
        self.assertEqual(len(coords), 2)
        self.assertIsInstance(coords[0], float)
        self.assertIsInstance(coords[1], float)


class TestRiskAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = RiskAnalyzer()
    
    def test_analyze_valid_number(self):
        result = self.analyzer.analyze("+27612345678")
        self.assertIn('risk_score', result)
        self.assertIn('risk_level', result)
        self.assertIn('flags', result)
        self.assertIn('recommendation', result)
    
    def test_low_risk_score(self):
        result = self.analyzer.analyze("+27612345678")
        self.assertIn(result['risk_level'], ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])


class TestPhoneFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = PhoneFormatter()
    
    def test_to_e164(self):
        result = self.formatter.to_e164("+27612345678")
        self.assertEqual(result, "+27612345678")
        result = self.formatter.to_e164("0612345678")
        self.assertEqual(result, "+27612345678")
    
    def test_to_readable(self):
        result = self.formatter.to_readable("+27612345678")
        self.assertIn("+27", result)
        self.assertIn("61", result)
    
    def test_mask_number(self):
        result = self.formatter.mask_number("+27612345678")
        self.assertTrue(result.startswith("+27"))
        self.assertTrue(result.endswith("5678"))
        self.assertIn("*", result)


class TestIntegration(unittest.TestCase):
    def test_full_analysis_flow(self):
        phone = "+27123456789"
        validator = PhoneValidator()
        is_valid, _, standardized = validator.validate(phone)
        self.assertTrue(is_valid)
        
        provider, _ = ProviderLookup.identify_provider(standardized)
        self.assertIsNotNone(provider)
        
        region, city = GeolocationLookup.estimate_region(standardized)
        self.assertIsNotNone(region)
        
        analyzer = RiskAnalyzer()
        risk = analyzer.analyze(standardized)
        self.assertIn('risk_level', risk)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPhoneValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestProviderLookup))
    suite.addTests(loader.loadTestsFromTestCase(TestGeolocationLookup))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPhoneFormatter))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1
if __name__ == "__main__":
    sys.exit(run_tests())
