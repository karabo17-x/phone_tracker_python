import json
import os
import re
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

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

    @staticmethod
    def analyze(phone_number: str, call_history: Optional[List[datetime]] = None) -> Dict[str, Any]:
        if not phone_number or not isinstance(phone_number, str):
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
        
        if call_history and len(call_history) > 1:
            if RiskAnalyzer._detect_rapid_calls(call_history):
                risk_score += RiskAnalyzer.RAPID_CALLS_SCORE
                flags.append("Repeated calls detected")
        
        if RiskAnalyzer._is_uncommon_format(phone_number):
            risk_score += RiskAnalyzer.UNCOMMON_FORMAT_SCORE
            flags.append("Uncommon format")
        
        risk_level = RiskAnalyzer._score_to_level(risk_score)
        
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
    def _detect_rapid_calls(call_history: List[datetime]) -> bool:
        try:
            if not call_history or len(call_history) < 2:
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
    @staticmethod
    def analyze_pattern(call_frequency: int, call_duration_minutes: float, time_of_day: str) -> Dict[str, Any]:
        anomalies = []
        
        if call_frequency > 10:
            anomalies.append("Unusually high call frequency")
        
        if call_duration_minutes < 1:
            anomalies.append("Very brief calls (< 1 minute)")
        
        if time_of_day in ['night', 'early_morning']:
            anomalies.append("Calls at unusual hours")
        
        return {
            'call_frequency': call_frequency,
            'avg_duration': call_duration_minutes,
            'time_pattern': time_of_day,
            'anomalies': anomalies,
            'is_suspicious': len(anomalies) > 0
        }
