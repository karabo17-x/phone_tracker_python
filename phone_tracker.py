import phonenumbers
import requests
import os
from phonenumbers import geocoder, carrier
from phonenumbers.phonenumberutil import NumberParseException

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

ZA_AREA_CODES = {
    '11': 'Gauteng(Johannesburg)',
    '12': 'Gauteng(Pretoia)',
    '13': 'Mpumalanga',
    '14': 'North West',
    '15': 'Limpopo',
    '16': 'North West',
    '17': 'Gauteng',
    '18': 'Free State',
    '21': 'Western Cape',
    '22': 'Western Cape',
    '23': 'Eastern Cape',
    '24': 'Northern Cape',
    '27': 'KwaZulu-Natal',
    '28': 'Eastern Cape',
    '31': 'KwaZulu-Natal',
    '32': 'KwaZulu-Natal',
    '41': 'Estern Cape',
    '51': 'Free State',
    '57': 'Free State',
}

def get_geolocation(phone_number):
    try:
        params = {"address": phone_number, "key": GOOGLE_API_KEY}
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()

        results = response.json().get('results',[])
        if results:
            return results[0]['formatted_address']
    except Exception as e:
        print(f"Geocoding error: {e}")
    return "Precise location unavailable"  

def get_phone_details(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except NumberParseException:
        return "Error: Invalid phone number format"

    if not phonenumbers.is_valid_number(parsed_number):
        return "Error: Invalid phone number"
    
    country_code = phonenumbers.region_code_for_number(parsed_number)
    country_name = geocoder.country_name_for_number(parsed_number, "en")

    try:

        carrier_name = carrier.name_for_number(parsed_number, "en") or "Unknown carrier"

    except:
        carrier_name = "Carrier info Unavailable"


    precise_location = get_geolocation(phone_number)

    local_geo = geocoder.description_for_number(parsed_number, "en") or "Area information unavailable"  


    if country_code == 'ZA':
        national_number = str(parsed_number.national_number)
        area_code = national_number[:2]
        province = ZA_AREA_CODES.get(area_code, "Unknown province")

        return(
            f"\n Service Provider:{carrier_name}"
            f"\n Country: South Africa(ZA)"
            f"\n Province: {province}"
            f"\n Local Area:{local_geo}"
            f"\n Precise Location: {precise_location}"
        )
    else:
        return(
            f"\n Phone Number: {phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.INTERNATIONAL)}"
            f"\n Service Provider:{carrier}"
            f"\n Country:{country_name}"
            f"\n Region: {local_geo}"
            f"\n Precise Location: {precise_location}"
        )

if __name__ == "__main__":
    print("\n PHONE NUMBER LOCATION TRACKER") 
    print("------------------------------------------------")
    
    phone_number = input("\nEnter phone number in international format: ")

    print(get_phone_details(phone_number))
    print("\n" + "="*50 + "\n")
    




