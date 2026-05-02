import re
from typing import Tuple, Optional

class PhoneValidator:
    PATTERNS = {
        'international': r'^\+27[0-9]{9}$',
        'national_zero': r'^0[0-9]{9}$',
        'national': r'^[0-9]{10}$',
    }
    
    VALID_FIRST_DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    @staticmethod
    def validate(phone_number: str) -> Tuple[bool, str, Optional[str]]:
        if not phone_number:
            return False, "Phone number cannot be empty", None
        
        cleaned = phone_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        try:
            import phonenumbers
            from phonenumbers.phonenumberutil import NumberParseException
            
            parsed_number = phonenumbers.parse(cleaned, None)
            if phonenumbers.is_valid_number(parsed_number):
                standardized = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                return True, "", standardized
        except Exception:
            pass
        
        if re.match(PhoneValidator.PATTERNS['international'], cleaned):
            return True, "", cleaned
        elif re.match(PhoneValidator.PATTERNS['national_zero'], cleaned):
            standardized = "+27" + cleaned[1:]
            return True, "", standardized
        elif re.match(PhoneValidator.PATTERNS['national'], cleaned):
            standardized = "+27" + cleaned
            return True, "", standardized
        else:
            return False, "Invalid phone number format. Use +27XXXXXXXXX, 0XXXXXXXXX, or XXXXXXXXXX", None
    
    @staticmethod
    def extract_prefix(phone_number: str) -> str:
        if phone_number.startswith("+27"):
            return phone_number[3:5]
        elif phone_number.startswith("0"):
            return phone_number[1:3]
        else:
            return phone_number[1:3]
    
    @staticmethod
    def get_number_type(phone_number: str) -> str:
        try:
            import phonenumbers
            from phonenumbers.phonenumberutil import PhoneNumberType
            
            parsed_number = phonenumbers.parse(phone_number, None)
            number_type = phonenumbers.number_type(parsed_number)
            
            if number_type == PhoneNumberType.MOBILE:
                return "mobile"
            elif number_type == PhoneNumberType.FIXED_LINE:
                return "landline"
            elif number_type == PhoneNumberType.VOIP:
                return "voip"
            elif number_type == PhoneNumberType.UNKNOWN:
                return "unknown"
        except Exception:
            pass
        
        if phone_number.startswith("+27"):
            full_number = "0" + phone_number[3:]
        else:
            full_number = phone_number
        
        prefix = full_number[:3] if len(full_number) >= 3 else full_number
        voip_prefixes = ['087', '088']
        
        mobile_prefixes = [
            '060', '061', '062', '063', '064', '065', '066', '067', '068',
            '071', '072', '073', '074', '075', '076', '077', '078', '079',
            '081', '082', '083', '084', '085', '091', '092'
        ]
        
        landline_prefixes = [
            '011', '012', '013', '014', '015', '016', '017', '018',
            '021', '022', '023', '024', '027', '028',
            '031', '032', '033', '034', '035', '036', '037', '038',
            '041', '042', '043', '044', '045', '046', '047', '048',
            '051', '052', '053', '054', '055', '056', '057', '058'
        ]
        
        if prefix in voip_prefixes:
            return "voip"
        elif prefix in mobile_prefixes:
            return "mobile"
        elif prefix in landline_prefixes:
            return "landline"
        else:
            return "unknown"
