from typing import Dict, Tuple, List

PREFIX_PROVINCE_MAPPING = {
    '011': ('Gauteng', 'HIGH'),
    '012': ('Gauteng', 'HIGH'),
    '013': ('Mpumalanga', 'HIGH'),
    '014': ('North West', 'HIGH'),
    '015': ('Limpopo', 'HIGH'),
    '016': ('North West', 'HIGH'),
    '017': ('Gauteng', 'HIGH'),
    '018': ('Free State', 'HIGH'),
    '021': ('Western Cape', 'HIGH'),
    '022': ('Western Cape', 'HIGH'),
    '023': ('Eastern Cape', 'HIGH'),
    '024': ('Northern Cape', 'HIGH'),
    '027': ('Mpumalanga', 'HIGH'),
    '028': ('Eastern Cape', 'HIGH'),
    '031': ('KwaZulu-Natal', 'HIGH'),
    '032': ('KwaZulu-Natal', 'HIGH'),
    '033': ('KwaZulu-Natal', 'HIGH'),
    '034': ('KwaZulu-Natal', 'HIGH'),
    '035': ('KwaZulu-Natal', 'HIGH'),
    '036': ('KwaZulu-Natal', 'HIGH'),
    '037': ('KwaZulu-Natal', 'HIGH'),
    '038': ('KwaZulu-Natal', 'HIGH'),
    '041': ('Eastern Cape', 'HIGH'),
    '042': ('Eastern Cape', 'HIGH'),
    '043': ('Eastern Cape', 'HIGH'),
    '044': ('Eastern Cape', 'HIGH'),
    '045': ('Eastern Cape', 'HIGH'),
    '046': ('Eastern Cape', 'HIGH'),
    '047': ('Western Cape', 'HIGH'),
    '048': ('Western Cape', 'HIGH'),
    '051': ('Free State', 'HIGH'),
    '052': ('Free State', 'HIGH'),
    '053': ('Free State', 'HIGH'),
    '054': ('Northern Cape', 'HIGH'),
    '055': ('Northern Cape', 'HIGH'),
    '056': ('Free State', 'HIGH'),
    '057': ('Free State', 'HIGH'),
    '058': ('Northern Cape', 'HIGH'),
}

MOBILE_PREFIX_PROVINCE_HEURISTIC = {
    '60': ['Gauteng', 'Limpopo', 'North West'],
    '61': ['Gauteng', 'Mpumalanga'],
    '62': ['KwaZulu-Natal', 'Gauteng'],
    '63': ['Gauteng', 'Eastern Cape'],
    '64': ['Western Cape', 'Eastern Cape'],
    '65': ['Eastern Cape', 'Northern Cape'],
    '66': ['Gauteng', 'Free State'],
    '67': ['Limpopo', 'Mpumalanga'],
    '68': ['Mpumalanga', 'Limpopo'],
    '71': ['Western Cape', 'Gauteng'],
    '72': ['Western Cape', 'Eastern Cape'],
    '73': ['Gauteng', 'North West'],
    '74': ['Free State', 'Gauteng'],
    '75': ['Free State', 'Northern Cape'],
    '76': ['KwaZulu-Natal', 'Mpumalanga'],
    '78': ['Gauteng', 'Free State'],
    '79': ['Northern Cape', 'Free State'],
    '81': ['Limpopo', 'North West'],
    '82': ['Mpumalanga', 'Limpopo'],
    '83': ['Free State', 'North West'],
    '84': ['Gauteng', 'KwaZulu-Natal'],
    '85': ['North West', 'Gauteng'],
    '87': ['Eastern Cape', 'Western Cape'],
    '88': ['Northern Cape', 'Free State'],
    '91': ['Gauteng', 'Western Cape'],
    '92': ['Western Cape', 'Gauteng'],
}

class LocationInference:
    @staticmethod
    def infer_from_landline(phone_number: str) -> Dict[str, any]:
        if phone_number.startswith("+27"):
            prefix = "0" + phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[:3]
        else:
            prefix = "0" + phone_number[:2]

        if prefix in PREFIX_PROVINCE_MAPPING:
            province, confidence = PREFIX_PROVINCE_MAPPING[prefix]
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

        if prefix in MOBILE_PREFIX_PROVINCE_HEURISTIC:
            provinces = MOBILE_PREFIX_PROVINCE_HEURISTIC[prefix]
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
