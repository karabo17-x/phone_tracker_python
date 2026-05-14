import json
import os
import re
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from phone_tracker.utils.logger import PhoneTrackerLogger

class RiskAnalyzer:
    DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/sa_prefixes.json')
    RISK_LEVELS = {
        'LOW': 0,
        'MEDIUM': 1,
        'HIGH': 2,
        'CRITICAL': 3
    }
    
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
            patterns = [
                r'^0000',
                r'^1111',
                r'^(\d)\1{7,}',
            ]
            
            for pattern in patterns:
                if re.search(pattern, phone_number):
                    return True
            return False
        except (TypeError, re.error):
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
            
            if not phone_number.startswith("+27"):
                return False
            
            if len(phone_number) != RiskAnalyzer.SA_PHONE_LENGTH:
                return True
            
            if not phone_number[3:].isdigit():
                return True
            
            return False
        except (AttributeError, TypeError):
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


class CallPatternAnalyzer:
    # Threshold constants
    HIGH_CALL_FREQUENCY_THRESHOLD = 10
    MIN_CALL_DURATION_MINUTES = 1
    UNUSUAL_TIME_PERIODS = ['night', 'early_morning']
    MIN_CALL_FREQUENCY = 0
    
    @staticmethod
    def analyze_pattern(call_frequency: int, call_duration_minutes: float, time_of_day: str) -> Dict[str, Any]:
        logger = PhoneTrackerLogger()
        # Validate inputs
        if not isinstance(call_frequency, int) or call_frequency < CallPatternAnalyzer.MIN_CALL_FREQUENCY:
            logger.log_error(f'Invalid call frequency: {call_frequency}')
            return {
                'call_frequency': call_frequency,
                'avg_duration': call_duration_minutes,
                'time_pattern': time_of_day,
                'anomalies': ['Invalid call frequency'],
                'is_suspicious': True
            }
        
        if not isinstance(call_duration_minutes, (int, float)) or call_duration_minutes < 0:
            logger.log_error(f'Invalid call duration: {call_duration_minutes}')
            return {
                'call_frequency': call_frequency,
                'avg_duration': call_duration_minutes,
                'time_pattern': time_of_day,
                'anomalies': ['Invalid call duration'],
                'is_suspicious': True
            }
        
        if not isinstance(time_of_day, str) or not time_of_day:
            logger.log_error(f'Invalid time period: {time_of_day}')
            return {
                'call_frequency': call_frequency,
                'avg_duration': call_duration_minutes,
                'time_pattern': time_of_day,
                'anomalies': ['Invalid time period'],
                'is_suspicious': True
            }
        
        anomalies = []
        
        if call_frequency > CallPatternAnalyzer.HIGH_CALL_FREQUENCY_THRESHOLD:
            anomalies.append("Unusually high call frequency")
            logger._logger.info(f"High call frequency detected: {call_frequency} calls")
        
        if call_duration_minutes < CallPatternAnalyzer.MIN_CALL_DURATION_MINUTES:
            anomalies.append("Very brief calls (< 1 minute)")
            logger._logger.info(f"Brief call duration detected: {call_duration_minutes} minutes")
        
        if time_of_day in CallPatternAnalyzer.UNUSUAL_TIME_PERIODS:
            anomalies.append("Calls at unusual hours")
            logger._logger.info(f"Calls during unusual time: {time_of_day}")
        
        if len(anomalies) > 0:
            logger._logger.info(f"Pattern analysis detected {len(anomalies)} anomalies: {anomalies}")
        
        return {
            'call_frequency': call_frequency,
            'avg_duration': call_duration_minutes,
            'time_pattern': time_of_day,
            'anomalies': anomalies,
            'is_suspicious': len(anomalies) > 0
        }
