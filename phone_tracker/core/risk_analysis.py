import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from phone_tracker.utils.formatter import PhoneFormatter
from phone_tracker.utils.logger import PhoneTrackerLogger

class RiskAnalyzer:
    # Risk score increments
    SPOOFED_PATTERN_SCORE = 2
    RAPID_CALLS_SCORE = 2
    UNCOMMON_FORMAT_SCORE = 1
    
    # Score thresholds
    CRITICAL_THRESHOLD = 4
    HIGH_THRESHOLD = 3
    MEDIUM_THRESHOLD = 1
    
    # Call pattern thresholds
    RAPID_CALL_WINDOW_MINUTES = 5
    SA_PHONE_LENGTH = 12
    MIN_CALL_HISTORY_LENGTH = 2
    MIN_PHONE_DIGITS = 7  # Minimum valid phone digits (even short country codes)
    MAX_PHONE_DIGITS = 15  # Maximum per ITU-T E.164 standard

    @staticmethod
    def analyze(phone_number: str, call_history: Optional[List[datetime]] = None) -> Dict[str, Any]:
        logger = PhoneTrackerLogger()
        if not phone_number or not isinstance(phone_number, str):
            logger.log_error('Invalid phone number format', phone_number)
            return {
                'risk_score': 0,
                'risk_level': 'LOW',
                'flags': ['Invalid phone number format'],
                'safe': False,
                'recommendation': 'Unable to analyze'
            }
        
        risk_score = 0
        flags = []
        
        if RiskAnalyzer._is_spoofed_pattern(phone_number):
            risk_score += RiskAnalyzer.SPOOFED_PATTERN_SCORE
            flags.append("Potential spoofed number")
            logger._logger.info(f"Spoofed pattern detected for {phone_number}")
        
        if call_history and len(call_history) >= RiskAnalyzer.MIN_CALL_HISTORY_LENGTH:
            if RiskAnalyzer._detect_rapid_calls(call_history):
                risk_score += RiskAnalyzer.RAPID_CALLS_SCORE
                flags.append("Repeated calls detected")
                logger._logger.info(f"Rapid calls detected for {phone_number}: {len(call_history)} calls")
        
        if RiskAnalyzer._is_uncommon_format(phone_number):
            risk_score += RiskAnalyzer.UNCOMMON_FORMAT_SCORE
            flags.append("Uncommon format")
            logger._logger.info(f"Uncommon format detected for {phone_number}")
        
        risk_level = RiskAnalyzer._score_to_level(risk_score)
        logger._logger.info(f"Risk analysis complete for {phone_number}: score={risk_score}, level={risk_level}, flags={flags}")
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'flags': flags,
            'safe': risk_level in ['LOW', 'MEDIUM'],
            'recommendation': RiskAnalyzer._get_recommendation(risk_level)
        }
    
    @staticmethod
    def _is_spoofed_pattern(phone_number: str) -> bool:
        try:
            national_number = re.sub(r'\D', '', PhoneFormatter.to_national(phone_number))
            patterns = [
                r'^0000',
                r'^1111',
                r'^(\d)\1{7,}',
            ]
            
            for pattern in patterns:
                if re.search(pattern, national_number):
                    return True
            return False
        except (AttributeError, TypeError, re.error):
            return False
    
    @staticmethod
    def _detect_rapid_calls(call_history: Optional[List[datetime]]) -> bool:
        try:
            if not call_history or len(call_history) < RiskAnalyzer.MIN_CALL_HISTORY_LENGTH:
                return False
            sorted_calls = sorted(call_history)
            
            for i in range(len(sorted_calls) - 1):
                time_diff = sorted_calls[i + 1] - sorted_calls[i]
                if time_diff < timedelta(minutes=RiskAnalyzer.RAPID_CALL_WINDOW_MINUTES):
                    return True
            
            return False
        except (TypeError, AttributeError, ValueError):
            return False
    
    @staticmethod
    def _is_uncommon_format(phone_number: str) -> bool:
        try:
            if not phone_number or not isinstance(phone_number, str):
                return True
            
            # Normalize: remove spaces, hyphens, parentheses, dots
            normalized = re.sub(r'[\s\-().]', '', phone_number)
            
            # Check if it's an international format (starts with +)
            if normalized.startswith('+'):
                return RiskAnalyzer._validate_international_format(normalized)
            
            # Check if it's a local format (all digits, 7-15 digits per E.164)
            if normalized.isdigit() and RiskAnalyzer.MIN_PHONE_DIGITS <= len(normalized) <= RiskAnalyzer.MAX_PHONE_DIGITS:
                return False  # Valid local format
            
            # Unrecognized format
            return True
        except (AttributeError, TypeError):
            return True
    
    @staticmethod
    def _validate_international_format(phone_number: str) -> bool:
        """Validate international phone format (flexible - any country code). Returns True if uncommon/invalid."""
        try:
            # Must start with + (already checked by caller)
            if not phone_number.startswith('+'):
                return True
            
            # Extract country code and digits
            # Country codes are 1-3 digits long (per ITU-T)
            rest = phone_number[1:]  # Remove +
            
            # Find where country code ends (after 1-3 digits)
            country_code_end = None
            for i in range(1, min(4, len(rest) + 1)):
                if rest[:i].isdigit():
                    country_code_end = i
            
            if country_code_end is None:
                return True  # Invalid format, no country code digits
            
            # Extract remaining digits (the actual phone number)
            phone_digits = rest[country_code_end:]
            
            # Validate: must be all digits and within valid range
            if not phone_digits.isdigit():
                return True  # Non-digit characters after country code
            
            # Check length is within E.164 limits (7-15 digits total)
            total_digits = country_code_end + len(phone_digits)
            if total_digits < RiskAnalyzer.MIN_PHONE_DIGITS or total_digits > RiskAnalyzer.MAX_PHONE_DIGITS:
                return True  # Invalid length
            
            return False  # Valid international format
        except (AttributeError, TypeError, ValueError):
            return True
    
    @staticmethod
    def _score_to_level(score: int) -> str:
        try:
            if not isinstance(score, (int, float)):
                return 'LOW'
            if score >= RiskAnalyzer.CRITICAL_THRESHOLD:
                return 'CRITICAL'
            elif score >= RiskAnalyzer.HIGH_THRESHOLD:
                return 'HIGH'
            elif score >= RiskAnalyzer.MEDIUM_THRESHOLD:
                return 'MEDIUM'
            else:
                return 'LOW'
        except (TypeError, ValueError):
            return 'LOW'
    
    @staticmethod
    def _get_recommendation(risk_level: str) -> str:
        try:
            if not isinstance(risk_level, str):
                return 'Unknown risk'
            recommendations = {
                'LOW': 'Safe to answer',
                'MEDIUM': 'Answer with caution',
                'HIGH': 'Extreme caution',
                'CRITICAL': 'Do not answer - block and report'
            }
            return recommendations.get(risk_level, 'Unknown risk')
        except (TypeError, AttributeError):
            return 'Unknown risk'
