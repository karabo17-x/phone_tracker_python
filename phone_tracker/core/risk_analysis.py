import json
import os
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class RiskAnalyzer:
    DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/sa_prefixes.json')
    RISK_LEVELS = {
        'LOW': 0,
        'MEDIUM': 1,
        'HIGH': 2,
        'CRITICAL': 3
    }
    @staticmethod
    def analyze(phone_number: str, call_history: List[datetime] = None) -> Dict:
        risk_score = 0
        flags = []
        
        if RiskAnalyzer._is_spoofed_pattern(phone_number):
            risk_score += 2
            flags.append("Potential spoofed number")
        
        if call_history and len(call_history) > 1:
            if RiskAnalyzer._detect_rapid_calls(call_history):
                risk_score += 2
                flags.append("repeated calls detected")
        
        if RiskAnalyzer._is_uncommon_format(phone_number):
            risk_score += 1
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
        patterns = [
            r'^0000',  # All zeros
            r'^1111',  # All ones
            r'^(\d)\1{7,}',  # Repeating digits
        ]
        
        import re
        for pattern in patterns:
            if re.search(pattern, phone_number):
                return True
        return False
    
    @staticmethod
    def _detect_rapid_calls(call_history: List[datetime]) -> bool:
        if len(call_history) < 2:
            return False
        sorted_calls = sorted(call_history)
        
        for i in range(len(sorted_calls) - 2):
            time_diff = sorted_calls[i + 2] - sorted_calls[i]
            if time_diff < timedelta(minutes=5):
                return True
        
        return False
    
    @staticmethod
    def _is_uncommon_format(phone_number: str) -> bool:
        try:
            if not phone_number.startswith("+27"):
                return False
            
            if len(phone_number) != 12:
                return True
            
            if not phone_number[3:].isdigit():
                return True
            
            return False
        except:
            return True
    
    @staticmethod
    def _score_to_level(score: int) -> str:
        if score >= 4:
            return 'CRITICAL'
        elif score >= 3:
            return 'HIGH'
        elif score >= 1:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def _get_recommendation(risk_level: str) -> str:
        recommendations = {
            'LOW': 'Safe to answer',
            'MEDIUM': 'Answer with caution',
            'HIGH': 'extreme caution',
            'CRITICAL': 'Do not answer - block and report'
        }
        return recommendations.get(risk_level, 'Unknown risk')


class CallPatternAnalyzer:
    
    @staticmethod
    def analyze_pattern(call_frequency: int, call_duration_minutes: float, time_of_day: str) -> Dict:
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
