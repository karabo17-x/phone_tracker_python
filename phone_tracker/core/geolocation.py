from typing import Dict, Tuple, Optional
from .provider_lookup import GeolocationLookup as GeoLookup

class Geolocation:
    @staticmethod
    def get_region_info(phone_number: str) -> Dict:
        region, city = GeoLookup.estimate_region(phone_number)
        coordinates = GeoLookup.get_approximate_coordinates(region)
        
        return {
            'region': region,
            'city': city,
            'latitude': coordinates[0],
            'longitude': coordinates[1],
            'accuracy': 'LOW',
            'note': 'an estimation based on area code.'
        }
    
    @staticmethod
    def get_all_regions() -> Dict[str, Tuple[float, float]]:
        regions = {
            'Gauteng': (-25.7461, 28.2293),
            'Western Cape': (-33.9249, 18.4241),
            'KwaZulu-Natal': (-29.8587, 31.0218),
            'Eastern Cape': (-33.9649, 25.6054),
            'Free State': (-29.1199, 25.5048),
            'Northern Cape': (-28.7411, 24.8753),
            'Limpopo': (-24.5282, 29.0163),
            'Mpumalanga': (-25.4833, 30.7667),
            'North West': (-25.6667, 25.8667),
        }
        return regions
    
    @staticmethod
    def format_coordinates(lat: float, lon: float) -> str:
        return f"{lat:.4f}°, {lon:.4f}°"
    
    @staticmethod
    def get_map_link(lat: float, lon: float) -> str:
        return f"https://maps.google.com/?q={lat},{lon}"
