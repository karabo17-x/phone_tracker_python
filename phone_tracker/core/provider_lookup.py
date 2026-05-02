import json
import os
from typing import Dict, Optional, Tuple

MOBILE_PREFIX_TO_PROVINCE = {
    '60': 'Gauteng',
    '61': 'Gauteng',
    '62': 'KwaZulu-Natal',
    '63': 'Gauteng',
    '64': 'Western Cape',
    '65': 'Eastern Cape',
    '66': 'Gauteng',
    '67': 'Limpopo',
    '68': 'Mpumalanga',
    '71': 'Western Cape',
    '72': 'Western Cape',
    '73': 'Gauteng',
    '74': 'Free State',
    '75': 'Free State',
    '76': 'KwaZulu-Natal',
    '78': 'Gauteng',
    '79': 'Northern Cape',
    '81': 'Limpopo',
    '82': 'Mpumalanga',
    '83': 'Free State',
    '84': 'Gauteng',
    '85': 'North West',
    '87': 'Eastern Cape',
    '88': 'Northern Cape',
    '91': 'Gauteng',
    '92': 'Western Cape',
}

MOBILE_PREFIXES_DB = {
    '60': ('Vodacom', 'VODACOM', 'Mobile'),
    '61': ('Vodacom', 'VODACOM', 'Mobile'),
    '65': ('Vodacom', 'VODACOM', 'Mobile'),
    '66': ('Vodacom', 'VODACOM', 'Mobile'),
    '67': ('Vodacom', 'VODACOM', 'Mobile'),
    '68': ('Vodacom', 'VODACOM', 'Mobile'),
    '73': ('Vodacom', 'VODACOM', 'Mobile'),
    '62': ('MTN', 'MTN', 'Mobile'),
    '63': ('MTN', 'MTN', 'Mobile'),
    '64': ('MTN', 'MTN', 'Mobile'),
    '84': ('MTN', 'MTN', 'Mobile'),
    '85': ('MTN', 'MTN', 'Mobile'),
    '71': ('Cell C', 'CELLC', 'Mobile'),
    '72': ('Cell C', 'CELLC', 'Mobile'),
    '74': ('Cell C', 'CELLC', 'Mobile'),
    '75': ('Cell C', 'CELLC', 'Mobile'),
    '76': ('Cell C', 'CELLC', 'Mobile'),
    '79': ('Cell C', 'CELLC', 'Mobile'),
    '78': ('Telkom Mobile', 'TELKOM', 'Mobile'),
    '81': ('Telkom Mobile', 'TELKOM', 'Mobile'),
    '82': ('Telkom Mobile', 'TELKOM', 'Mobile'),
    '83': ('Telkom Mobile', 'TELKOM', 'Mobile'),
    '87': ('Neotel', 'NEOTEL', 'Mobile'),
    '88': ('Neotel', 'NEOTEL', 'Mobile'),
    '91': ('Rain', 'RAIN', 'Mobile'),
    '92': ('Telkom Fixed Wireless', 'TELKOM-FW', 'Fixed Wireless'),
}

LANDLINE_PREFIXES_DB = {
    '011': ('Telkom Gauteng', 'TELKOM-LINE', 'Landline'),
    '012': ('Telkom Gauteng', 'TELKOM-LINE', 'Landline'),
    '013': ('Telkom Mpumalanga', 'TELKOM-LINE', 'Landline'),
    '014': ('Telkom North West', 'TELKOM-LINE', 'Landline'),
    '015': ('Telkom Limpopo', 'TELKOM-LINE', 'Landline'),
    '016': ('Telkom North West', 'TELKOM-LINE', 'Landline'),
    '017': ('Telkom Gauteng', 'TELKOM-LINE', 'Landline'),
    '018': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
    '021': ('Telkom Western Cape', 'TELKOM-LINE', 'Landline'),
    '022': ('Telkom Western Cape', 'TELKOM-LINE', 'Landline'),
    '023': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '024': ('Telkom Northern Cape', 'TELKOM-LINE', 'Landline'),
    '027': ('Telkom Mpumalanga', 'TELKOM-LINE', 'Landline'),
    '028': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '031': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '032': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '033': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '034': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '035': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '036': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '037': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '038': ('Telkom KwaZulu-Natal', 'TELKOM-LINE', 'Landline'),
    '041': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '042': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '043': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '044': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '045': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '046': ('Telkom Eastern Cape', 'TELKOM-LINE', 'Landline'),
    '047': ('Telkom Western Cape', 'TELKOM-LINE', 'Landline'),
    '048': ('Telkom Western Cape', 'TELKOM-LINE', 'Landline'),
    '051': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
    '052': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
    '053': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
    '054': ('Telkom Northern Cape', 'TELKOM-LINE', 'Landline'),
    '055': ('Telkom Northern Cape', 'TELKOM-LINE', 'Landline'),
    '056': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
    '057': ('Telkom Free State', 'TELKOM-LINE', 'Landline'),
}


class ProviderLookup:
    DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/sa_prefixes.json')
    
    _cache: Dict = {}
    
    @classmethod
    def load_data(cls) -> Dict:
        if not cls._cache:
            try:
                with open(cls.DATA_FILE, 'r') as f:
                    cls._cache = json.load(f)
            except FileNotFoundError:
                cls._cache = {}
        return cls._cache
    
    @staticmethod
    def identify_provider(phone_number: str) -> Tuple[str, str]:
        if phone_number.startswith("+27"):
            prefix = phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[1:3]
        else:
            prefix = phone_number[0:2]
        
        if prefix in MOBILE_PREFIXES_DB:
            operator_name, operator_code, _ = MOBILE_PREFIXES_DB[prefix]
            return operator_name, operator_code
        
        if phone_number.startswith("+27"):
            three_digit = "0" + phone_number[3:5]  
        elif phone_number.startswith("0"):
            three_digit = phone_number[0:3]
        else:
            three_digit = "0" + phone_number[0:2]
        
        if three_digit in LANDLINE_PREFIXES_DB:
            operator_name, operator_code, _ = LANDLINE_PREFIXES_DB[three_digit]
            return operator_name, operator_code
        
        return "Unknown", "UNKNOWN"

    @staticmethod
    def identify_provider_detailed(phone_number: str) -> Dict[str, any]:
        if phone_number.startswith("+27"):
            prefix = phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[1:3]
        else:
            prefix = phone_number[0:2]
        
        if prefix in MOBILE_PREFIXES_DB:
            operator_name, operator_code, sim_type = MOBILE_PREFIXES_DB[prefix]
            return {
                'provider': operator_name,
                'code': operator_code,
                'type': sim_type,
                'confidence': 'HIGH',
                'method': 'mobile_prefix_match',
                'inferred': False
            }
        
        if phone_number.startswith("+27"):
            three_digit = "0" + phone_number[3:5]
        elif phone_number.startswith("0"):
            three_digit = phone_number[0:3]
        else:
            three_digit = "0" + phone_number[0:2]
        
        if three_digit in LANDLINE_PREFIXES_DB:
            operator_name, operator_code, line_type = LANDLINE_PREFIXES_DB[three_digit]
            return {
                'provider': operator_name,
                'code': operator_code,
                'type': line_type,
                'confidence': 'HIGH',
                'method': 'landline_area_code_match',
                'inferred': False
            }
        
        return {
            'provider': 'Unknown',
            'code': 'UNKNOWN',
            'type': 'Unknown',
            'confidence': 'LOW',
            'method': 'unable_to_identify',
            'inferred': True
        }

    @staticmethod
    def get_all_operators() -> Dict:
        operators = {}
        for prefix, (name, code, sim_type) in MOBILE_PREFIXES_DB.items():
            if name not in operators:
                operators[name] = {'code': code, 'type': sim_type}
        return operators


class GeolocationLookup:
    ZA_AREA_CODES = {
        '11': 'Gauteng (Johannesburg)',
        '12': 'Gauteng (Pretoria)',
        '13': 'Mpumalanga (Witbank)',
        '14': 'North West (Rustenburg)',
        '15': 'Limpopo (Polokwane)',
        '16': 'North West (Mafikeng)',
        '17': 'Gauteng (Kempton Park)',
        '18': 'Free State (Bloemfontein)',
        '21': 'Western Cape (Cape Town)',
        '22': 'Western Cape (Mossel Bay)',
        '23': 'Eastern Cape (East London)',
        '24': 'Northern Cape (Kimberley)',
        '27': 'Mpumalanga (Nelspruit)',
        '28': 'Eastern Cape (Mthatha)',
        '31': 'KwaZulu-Natal (Durban)',
        '32': 'KwaZulu-Natal (Pietermaritzburg)',
        '33': 'KwaZulu-Natal (Richards Bay)',
        '34': 'KwaZulu-Natal (Newcastle)',
        '41': 'Eastern Cape (Port Elizabeth)',
        '42': 'Eastern Cape (Uitenhage)',
        '44': 'Eastern Cape (Knysna)',
        '45': 'Eastern Cape (George)',
        '46': 'Eastern Cape (Caledon)',
        '47': 'Western Cape (Hermanus)',
        '48': 'Western Cape (Worcester)',
        '51': 'Free State (Bloemfontein)',
        '52': 'Free State (Welkom)',
        '53': 'Free State (Winburg)',
        '56': 'Free State (Thaba Nchu)',
        '57': 'Free State (Ladybrand)',
        '58': 'Northern Cape (Kimberley)',
    }
    
    DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/sa_prefixes.json')
    
    _cache: Dict = {}
    
    @classmethod
    def load_data(cls) -> Dict:
        """Load SA prefix data."""
        if not cls._cache:
            try:
                with open(cls.DATA_FILE, 'r') as f:
                    cls._cache = json.load(f)
            except FileNotFoundError:
                cls._cache = {}
        return cls._cache
    
    @staticmethod
    def estimate_region(phone_number: str) -> Tuple[str, str]:
        from phone_tracker.api.external_services import MOCK_SUBSCRIBER_DATA
        
        if phone_number in MOCK_SUBSCRIBER_DATA:
            province = MOCK_SUBSCRIBER_DATA[phone_number].get('province', 'Unknown')
            city = MOCK_SUBSCRIBER_DATA[phone_number].get('city', 'Unknown')
            return province, city
        
        if phone_number.startswith("+27"):
            prefix = phone_number[3:5]
        elif phone_number.startswith("0"):
            prefix = phone_number[1:3]
        else:
            prefix = phone_number[0:2]
        
        if prefix in GeolocationLookup.ZA_AREA_CODES:
            location = GeolocationLookup.ZA_AREA_CODES[prefix]
            return location, prefix
        
        if prefix in MOBILE_PREFIX_TO_PROVINCE:
            province = MOBILE_PREFIX_TO_PROVINCE[prefix]
            return province, f"{prefix} (Mobile)"
        
        return "Gauteng", "Unknown (Likely mobile)"
    
    @staticmethod
    def get_approximate_coordinates(region: str) -> Tuple[float, float]:
        coordinates = {
            "Gauteng": (-25.7461, 28.2293),
            "Western Cape": (-33.9249, 18.4241),
            "KwaZulu-Natal": (-29.8587, 31.0218),
            "Eastern Cape": (-33.9649, 25.6054),
            "Free State": (-29.1199, 25.5048),
            "Northern Cape": (-28.7411, 24.8753),
            "Limpopo": (-24.5282, 29.0163),
            "Mpumalanga": (-25.4833, 30.7667),
            "North West": (-25.6667, 25.8667),
        }
        return coordinates.get(region, (-25.5, 27.5))
