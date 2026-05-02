from typing import Optional 

class PhoneFormatter:
    @staticmethod
    def to_e164(phone_number: str) -> str:
        if phone_number.startswith("+27"):
            return phone_number
        elif phone_number.startswith("0"):
            return "+27" + phone_number[1:]
        else:
            return "+27" + phone_number
    
    @staticmethod
    def to_national(phone_number: str) -> str:
        clean = phone_number.replace("+27", "0").replace(" ", "").replace("-", "")
        
        if len(clean) == 10 and clean.startswith("0"):
            return f"{clean[0:3]} {clean[3:6]} {clean[6:10]}"
        return clean
    
    @staticmethod
    def to_readable(phone_number: str) -> str:
        if phone_number.startswith("+27"):
            number = phone_number[3:]
        elif phone_number.startswith("0"):
            number = phone_number[1:]
        else:
            number = phone_number
        
        if len(number) == 9:
            return f"+27 {number[0:2]} {number[2:5]} {number[5:9]}"
        return phone_number
    
    @staticmethod
    def mask_number(phone_number: str, mask_char: str = "*") -> str:
        if not phone_number.startswith("+27"):
            phone_number = PhoneFormatter.to_e164(phone_number)
        
        if phone_number.startswith("+27"):
            prefix = phone_number[:6]
            suffix = phone_number[-4:]
            masked_part = mask_char * (len(phone_number) - 10)
            return f"{prefix}{masked_part}{suffix}"
        
        return phone_number
    
    @staticmethod
    def get_display_number(phone_number: str, privacy: bool = False) -> str:
        if privacy:
            return PhoneFormatter.mask_number(phone_number)
        return PhoneFormatter.to_readable(phone_number)


class OutputFormatter:
    COLORS = {
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
    }
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        color_code = OutputFormatter.COLORS.get(color.upper(), '')
        reset_code = OutputFormatter.COLORS['RESET']
        return f"{color_code}{text}{reset_code}"
    
    @staticmethod
    def bold(text: str) -> str:
        return OutputFormatter.colorize(text, 'BOLD')
    
    @staticmethod
    def success(text: str) -> str:
        return OutputFormatter.colorize(f"{text}", 'GREEN')
    
    @staticmethod
    def error(text: str) -> str:
        return OutputFormatter.colorize(f" {text}", 'RED')
    
    @staticmethod
    def warning(text: str) -> str:
        return OutputFormatter.colorize(f"{text}", 'YELLOW')
    
    @staticmethod
    def info(text: str) -> str:
        return OutputFormatter.colorize(f"[INFO] {text}", 'BLUE')
    
    @staticmethod
    def header(text: str) -> str:
        return OutputFormatter.colorize(text, 'CYAN')
    
    @staticmethod
    def create_separator(width: int = 60, char: str = "─") -> str:
        return OutputFormatter.colorize(char * width, 'BLUE')
    
    @staticmethod
    def create_table(headers: list, rows: list) -> str:
        result = []
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        result.append(OutputFormatter.bold(header_line))
        result.append("-" * len(header_line))
        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            result.append(row_line)
        
        return "\n".join(result)
