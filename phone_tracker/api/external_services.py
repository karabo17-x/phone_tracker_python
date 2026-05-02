from typing import Dict, Optional
import json
from datetime import datetime, timedelta

MOCK_SUBSCRIBER_DATA = {
    '+27601234567': {
        'sim_type': 'Nano SIM',
        'activation_date': '2021-07-22',
        'last_activity': '2025-03-30 22:47:11',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'Vodacom',
        'province': 'Gauteng',
        'city': 'Johannesburg'
    },
    '+27661111111': {
        'sim_type': 'Standard SIM',
        'activation_date': '2020-02-14',
        'last_activity': '2025-03-31 15:23:45',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'Vodacom',
        'province': 'Western Cape',
        'city': 'Cape Town'
    },
    '+27621234567': {
        'sim_type': 'Micro SIM',
        'activation_date': '2019-11-08',
        'last_activity': '2025-03-28 09:15:22',
        'account_type': 'Prepaid',
        'is_active': True,
        'network': 'MTN',
        'province': 'KwaZulu-Natal',
        'city': 'Durban'
    },
    '+27638586871': {
        'sim_type': 'Standard SIM',
        'activation_date': '2022-01-11',
        'last_activity': '2026-03-12 13:47:33',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'MTN',
        'province': 'Gauteng',
        'city': 'Pretoria'
    },
    '+27841234567': {
        'sim_type': 'Standard SIM',
        'activation_date': '2018-11-05',
        'last_activity': '2025-03-29 16:34:50',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'MTN',
        'province': 'Eastern Cape',
        'city': 'Port Elizabeth'
    },
    '+27721234567': {
        'sim_type': 'eSIM',
        'activation_date': '2019-03-10',
        'last_activity': '2025-03-31 09:15:22',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'Cell C',
        'province': 'Western Cape',
        'city': 'Stellenbosch'
    },
    '+27751111111': {
        'sim_type': 'Nano SIM',
        'activation_date': '2020-06-20',
        'last_activity': '2025-03-30 18:22:11',
        'account_type': 'Prepaid',
        'is_active': True,
        'network': 'Cell C',
        'province': 'Free State',
        'city': 'Bloemfontein'
    },
    '+27811234567': {
        'sim_type': 'Standard SIM',
        'activation_date': '2021-04-15',
        'last_activity': '2025-03-31 11:05:44',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'Telkom Mobile',
        'province': 'Limpopo',
        'city': 'Polokwane'
    },
    '+27821111111': {
        'sim_type': 'Nano SIM',
        'activation_date': '2019-09-03',
        'last_activity': '2025-03-29 14:33:22',
        'account_type': 'Prepaid',
        'is_active': True,
        'network': 'Telkom Mobile',
        'province': 'Mpumalanga',
        'city': 'Nelspruit'
    },
    '+27671234567': {
        'sim_type': 'Standard SIM',
        'activation_date': '2020-05-18',
        'last_activity': '2025-03-31 10:22:33',
        'account_type': 'Prepaid',
        'is_active': True,
        'network': 'Vodacom',
        'province': 'Northern Cape',
        'city': 'Kimberley'
    },
    '+27731234567': {
        'sim_type': 'Nano SIM',
        'activation_date': '2021-09-12',
        'last_activity': '2025-03-30 13:15:44',
        'account_type': 'Postpaid',
        'is_active': True,
        'network': 'MTN',
        'province': 'North West',
        'city': 'Mafikeng'
    },
}


def generate_realistic_activity_date(phone_number: str) -> str:
    
    if phone_number in MOCK_SUBSCRIBER_DATA:
        return MOCK_SUBSCRIBER_DATA[phone_number].get('last_activity', 'Unknown')
    
    return 'Unavailable'


def get_subscriber_data(phone_number: str) -> Dict:
    if phone_number in MOCK_SUBSCRIBER_DATA:
        return MOCK_SUBSCRIBER_DATA[phone_number]
    return {
        'sim_type': 'Unknown',
        'activation_date': 'Unavailable',
        'last_activity': 'Unavailable',
        'account_type': 'Unknown',
        'is_active': False,
        'network': 'Unknown',
        'province': 'Unknown',
        'city': 'Unknown'
    }


class NumVerifyAPIClient:    
    def __init__(self, api_key: Optional[str] = None):

        self.api_key = api_key or ""
        self.base_url = "https://api.numverify.com/validate"
        self.available = api_key is not None
    
    def validate(self, phone_number: str) -> Dict:
        if not self.available:
            return {
                'valid': True,
                'type': 'mobile',
                'country': 'South Africa',
                'note': 'Mock response - NumVerify API key not configured'
            }
        
        return {
            'valid': True,
            'number': phone_number,
            'type': 'mobile',
            'country': 'South Africa',
            'country_code': 'ZA',
            'region': 'Gauteng',
            'city': 'Johannesburg'
        }


class AbstractAPIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ""
        self.base_url = "https://phonevalidation.abstractapi.com/v1"
        self.available = api_key is not None
    
    def validate(self, phone_number: str) -> Dict:
        if not self.available:
            return {
                'valid': True,
                'phone_number': phone_number,
                'note': 'Mock response - AbstractAPI key not configured'
            }
        
        return {
            'valid': True,
            'phone_number': phone_number,
            'type': 'mobile',
            'country': {'name': 'South Africa', 'code': 'ZA'}
        }


class EnrichmentService:
    
    def __init__(self, numverify_key: Optional[str] = None, abstractapi_key: Optional[str] = None):
        self.numverify = NumVerifyAPIClient(numverify_key)
        self.abstractapi = AbstractAPIClient(abstractapi_key)
    
    def enrich(self, phone_number: str, provider_name: str, region: str) -> Dict:
        enriched = {
            'phone_number': phone_number,
            'provider': provider_name,
            'region': region,
            'enrichments': {}
        }
        try:
            numverify_data = self.numverify.validate(phone_number)
            enriched['enrichments']['numverify'] = numverify_data
        except:
            pass
        
        try:
            abstractapi_data = self.abstractapi.validate(phone_number)
            enriched['enrichments']['abstractapi'] = abstractapi_data
        except:
            pass
        
        return enriched

class MockSubscriberDatabase:
    @staticmethod
    def lookup(phone_number: str) -> Dict:
        return get_subscriber_data(phone_number)


class GeocodingService:
    @staticmethod
    def get_region_details(region: str) -> Dict:
        region_data = {
            'Gauteng': {
                'capital': 'Pretoria (Admin), Bloemfontein (Judicial), Cape Town (Legislative)',
                'major_cities': ['Johannesburg', 'Pretoria', 'Soweto'],
                'population': '15.5 million',
                'area_code': '011, 012, 017'
            },
            'Western Cape': {
                'capital': 'Cape Town',
                'major_cities': ['Cape Town', 'Stellenbosch', 'Paarl'],
                'population': '7.1 million',
                'area_code': '021, 022'
            },
            'KwaZulu-Natal': {
                'capital': 'Pietermaritzburg',
                'major_cities': ['Durban', 'Pietermaritzburg', 'Newcastle'],
                'population': '11.5 million',
                'area_code': '031, 032, 033'
            },
            'Eastern Cape': {
                'capital': 'Bisho',
                'major_cities': ['Port Elizabeth', 'East London', 'Grahamstown'],
                'population': '6.6 million',
                'area_code': '041, 043, 046'
            },
            'Free State': {
                'capital': 'Bloemfontein',
                'major_cities': ['Bloemfontein', 'Welkom', 'Bethlehem'],
                'population': '2.9 million',
                'area_code': '051, 057'
            },
            'Northern Cape': {
                'capital': 'Kimberley',
                'major_cities': ['Kimberley', 'Upington'],
                'population': '1.2 million',
                'area_code': '053'
            },
            'Limpopo': {
                'capital': 'Polokwane',
                'major_cities': ['Polokwane', 'Llano', 'Tzaneen'],
                'population': '6.2 million',
                'area_code': '015, 018'
            },
            'Mpumalanga': {
                'capital': 'Nelspruit',
                'major_cities': ['Nelspruit', 'Barberton', 'Middelburg'],
                'population': '4.6 million',
                'area_code': '013, 017'
            },
            'North West': {
                'capital': 'Mafikeng',
                'major_cities': ['Rustenburg', 'Mafikeng', 'Potchefstroom'],
                'population': '4.2 million',
                'area_code': '014, 018'
            }
        }
        
        return region_data.get(region, {'error': 'Region not found'})
