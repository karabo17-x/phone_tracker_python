import os
import sys
import time
from typing import Optional
from datetime import datetime
from phone_tracker.core import (
    PhoneValidator,
    ProviderLookup,
    RiskAnalyzer,
    LocationInference,
    ActivityStatus
)
from phone_tracker.ui.banner import build_cli_banner
from phone_tracker.utils import PhoneFormatter, OutputFormatter, logger


class PhoneTrackerCLI:
    def __init__(self):
        self.formatter = OutputFormatter()
        self.phone_formatter = PhoneFormatter()
        self.validator = PhoneValidator()
        self.provider_lookup = ProviderLookup()
        self.risk_analyzer = RiskAnalyzer()
        self.location_inference = LocationInference()
        self.activity_status = ActivityStatus()
    
    def show_banner(self):
        print(self.formatter.colorize(build_cli_banner(), 'CYAN'))

    def show_analysis_header(self, phone_number: str):
        print(self.formatter.colorize("\n[COMMAND CENTER] Phone Tracker scan initialized", 'CYAN'))
        print(f"Target Number: {self.formatter.colorize(phone_number, 'GREEN')}")
        print(self.formatter.colorize("Scope: provider, location estimate, activity, and risk", 'BLUE'))
    
    def show_separator(self, title: Optional[str] = None):
        if title:
            print(f"\n{self.formatter.bold(title)}")
        print(self.formatter.create_separator())
    
    def show_loading(self, message: str = "Processing"):
        frames = ["-", "\\", "|", "/"]
        for i in range(20):
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{self.formatter.colorize(frame, 'CYAN')} {message}...")
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.flush()
    
    def analyze_number(self, phone_number: str) -> bool:
        is_valid, error_msg, standardized = self.validator.validate(phone_number)
        
        if not is_valid:
            print(self.formatter.error(error_msg))
            return False
        
        self.show_analysis_header(standardized)
        self.show_loading("Analyzing")
        
        number_type = self.validator.get_number_type(standardized)
        provider_info = self.provider_lookup.identify_provider_detailed(standardized)
        location_info = self.location_inference.infer_location(standardized, number_type)
        activity_info = self.activity_status.get_activity_summary(standardized)
        risk_analysis = self.risk_analyzer.analyze(standardized)
        
        self.display_results(
            standardized,
            number_type,
            provider_info,
            location_info,
            activity_info,
            risk_analysis
        )
        
        logger.log_query(standardized, provider_info['provider'], location_info['estimated_province'], risk_analysis['risk_level'])
        
        return True
    
    def display_results(self, phone_number: str, number_type: str, provider_info: dict, 
                       location_info: dict, activity_info: dict, risk_analysis: dict):
        
        self.show_separator(" PHONE NUMBER ANALYSIS")
        
        print(f"\n{self.formatter.bold('BASIC INFORMATION')}")
        print(f"International Format: {self.formatter.colorize(phone_number, 'GREEN')}")
        print(f"National Format: {self.formatter.colorize(self.phone_formatter.to_national(phone_number), 'GREEN')}")
        print(f"Number Type: {self.formatter.colorize(number_type.upper(), 'CYAN')}")
        
        print(f"\n{self.formatter.bold('PROVIDER INFORMATION')}")
        provider_confidence_color = 'GREEN' if provider_info['confidence'] == 'HIGH' else 'YELLOW'
        print(f"Provider: {self.formatter.colorize(provider_info['provider'], 'MAGENTA')}")
        print(f"Operator Code: {self.formatter.colorize(provider_info['code'], 'MAGENTA')}")
        print(f"Type: {provider_info['type']}")
        print(f"Confidence: {self.formatter.colorize(provider_info['confidence'], provider_confidence_color)}")
        print(f"Method: {provider_info['method']}")
        
        print(f"\n{self.formatter.bold('ESTIMATED GEOGRAPHIC LOCATION')}")
        location_confidence_color = 'GREEN' if location_info['confidence'] == 'HIGH' else ('YELLOW' if location_info['confidence'] == 'MEDIUM' else 'RED')
        print(f"Estimated Province: {self.formatter.colorize(location_info['estimated_province'], location_confidence_color)}")
        
        if 'possible_provinces' in location_info and location_info['possible_provinces']:
            print(f"  Possible Provinces: {', '.join(location_info['possible_provinces'][:3])}")
        
        print(f"Confidence Level: {self.formatter.colorize(location_info['confidence'], location_confidence_color)}")
        print(f"Inference Method: {location_info['method']}")
        print(f"Status: {self.formatter.warning('ESTIMATED - Not exact location')}")
        
        print(f"\n{self.formatter.bold('ACTIVITY STATUS')}")
        print(f"Format Valid: {activity_info['format_valid']}")
        print(f"Likely Active: {activity_info['activity_status']}")
        print(f"Last Activity: {self.formatter.warning(activity_info['last_activity'])}")
        print(f"Data Source: {activity_info['data_source']}")
        print(f"Status: {self.formatter.warning('No real-time tracking')}")
        
        print(f"\n{self.formatter.bold('RISK ANALYSIS')}")
        risk_color = self._get_risk_color(risk_analysis['risk_level'])
        print(f"Risk Level: {self.formatter.colorize(risk_analysis['risk_level'], risk_color)}")
        print(f"Risk Score: {risk_analysis['risk_score']}/5")
        print(f"Recommendation: {self.formatter.colorize(risk_analysis['recommendation'], risk_color)}")
        
        if risk_analysis['flags']:
            print(f"  Flags:")
            for flag in risk_analysis['flags']:
                print(f"    - {self.formatter.warning(flag)}")
        else:
            print(f"  Flags: {self.formatter.success('None')}")
        
        print("\n" + self.formatter.create_separator())
    
    def _get_risk_color(self, risk_level: str) -> str:
        colors = {
            'LOW': 'GREEN',
            'MEDIUM': 'YELLOW',
            'HIGH': 'RED',
            'CRITICAL': 'RED'
        }
        return colors.get(risk_level, 'WHITE')
    
    def interactive_mode(self):
        self.show_banner()
        
        print(self.formatter.info("Enter a South African phone number to analyze"))
        print(self.formatter.info("Formats: +27123456789, 0123456789, or 27123456789"))
        print(self.formatter.info("Type 'quit' to exit\n"))
        
        while True:
            try:
                phone_number = input(self.formatter.colorize(" Enter phone number: ", 'BLUE')).strip()
                
                if phone_number.lower() in ['quit', 'exit', 'q']:
                    print(self.formatter.info("Thank you for using Phone Tracker!"))
                    break
                
                if not phone_number:
                    print(self.formatter.warning("Please enter a phone number\n"))
                    continue
                
                success = self.analyze_number(phone_number)
                if success:
                    print("")
                
            except KeyboardInterrupt:
                print(f"\n{self.formatter.info('Exiting...')}")
                break
            except Exception as e:
                print(self.formatter.error(f"An error occurred: {str(e)}"))
    
    def single_query(self, phone_number: str):
        self.show_banner()
        success = self.analyze_number(phone_number)
        sys.exit(0 if success else 1)

def run_cli():
    cli = PhoneTrackerCLI()
    
    if len(sys.argv) > 1:
        phone_number = " ".join(sys.argv[1:])
        cli.single_query(phone_number)
    else:
        cli.interactive_mode()

if __name__ == "__main__":
    run_cli()
