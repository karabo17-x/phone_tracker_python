import logging
import os
from datetime import datetime
from typing import Optional

class PhoneTrackerLogger:
    LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs')
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PhoneTrackerLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        if not os.path.exists(self.LOG_DIR):
            try:
                os.makedirs(self.LOG_DIR)
            except Exception:
                pass
        self._logger = logging.getLogger('phone_tracker')
        self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            log_file = os.path.join(self.LOG_DIR, f'phone_tracker_{datetime.now().strftime("%Y%m%d")}.log')
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.INFO)
                formatter = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
            except Exception:
                pass

    def log_query(self, phone_number: str, provider: str, region: str, risk_level: str):
        if self._logger:
            self._logger.info(
                f"Query | Phone: {phone_number} | Provider: {provider} | Region: {region} | Risk: {risk_level}"
            )
    
    def log_error(self, error_msg: str, phone_number: Optional[str] = None):
        if self._logger:
            if phone_number:
                self._logger.error(f"Error for {phone_number}: {error_msg}")
            else:
                self._logger.error(f"Error: {error_msg}")
    
    def log_info(self, message: str):
        if self._logger:
            self._logger.info(message)
    
    def get_logger(self):
        return self._logger


logger = PhoneTrackerLogger()
