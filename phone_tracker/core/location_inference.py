from typing import Dict
from phone_tracker.core.prefix_data import LANDLINE_PREFIX_PROVINCES, MOBILE_PREFIX_PROVINCES

class LocationInference:
    @staticmethod
    def infer_from_landline(phone_number: str) -> Dict[str, any]:
        if phone_number.startswith("+27"):
            prefix = "0" + phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[:3]
        else:
            prefix = "0" + phone_number[:2]

        if prefix in LANDLINE_PREFIX_PROVINCES:
            province, confidence = LANDLINE_PREFIX_PROVINCES[prefix]
            return {
                'type': 'landline',
                'estimated_province': province,
                'confidence': confidence,
                'method': 'area_code_mapping',
                'inferred': True
            }

        return {
            'type': 'landline',
            'estimated_province': 'Unknown',
            'confidence': 'LOW',
            'method': 'unable_to_determine',
            'inferred': True
        }

    @staticmethod
    def infer_from_mobile(phone_number: str) -> Dict[str, any]:
        if phone_number.startswith("+27"):
            prefix = phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[1:3]
        else:
            prefix = phone_number[:2]

        if prefix in MOBILE_PREFIX_PROVINCES:
            provinces = MOBILE_PREFIX_PROVINCES[prefix]
            primary_province = provinces[0]
            confidence = 'MEDIUM'

            return {
                'type': 'mobile',
                'estimated_province': primary_province,
                'possible_provinces': provinces,
                'confidence': confidence,
                'method': 'prefix_heuristic',
                'inferred': True
            }

        return {
            'type': 'mobile',
            'estimated_province': 'Gauteng',
            'confidence': 'LOW',
            'method': 'default_assumption',
            'inferred': True
        }

    @staticmethod
    def infer_location(phone_number: str, number_type: str) -> Dict[str, any]:
        if number_type == 'landline':
            return LocationInference.infer_from_landline(phone_number)
        elif number_type == 'mobile':
            return LocationInference.infer_from_mobile(phone_number)
        else:
            return {
                'type': 'unknown',
                'estimated_province': 'Unknown',
                'confidence': 'LOW',
                'method': 'unknown_type',
                'inferred': True
            }
