from typing import Dict

class ActivityStatus:
    @staticmethod
    def estimate_status(phone_number: str) -> Dict[str, any]:
        return {
            'likely_active': 'Unknown',
            'last_activity': 'Not Available',
            'data_source': 'Estimation',
            'note': 'No private telecom data accessed.',
            'confidence': 'UNAVAILABLE',
            'inferred': False
        }

    @staticmethod
    def validate_number_format(phone_number: str) -> Dict[str, any]:
        if phone_number.startswith("+27") or phone_number.startswith("0"):
            return {
                'format_valid': True,
                'likely_active': 'Possibly',
                'reason': 'Valid SA number format',
                'confidence': 'LOW'
            }

        return {
            'format_valid': False,
            'likely_active': 'Unknown',
            'reason': 'Invalid phone number format',
            'confidence': 'N/A'
        }

    @staticmethod
    def get_activity_summary(phone_number: str) -> Dict[str, any]:
        format_check = ActivityStatus.validate_number_format(phone_number)
        status = ActivityStatus.estimate_status(phone_number)

        return {
            'phone_number': phone_number,
            'format_valid': format_check['format_valid'],
            'activity_status': status['likely_active'],
            'last_activity': status['last_activity'],
            'data_source': status['data_source'],
            'limitations': status['note'],
            'inferred': False
        }
