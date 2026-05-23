#  South African Phone Number Intelligence Tool
##  Overview

**Phone Tracker** is a modular Python application designed for analyzing South African phone numbers. It combines validation, provider identification (using the phonenumbers library), geolocation estimation, and risk analysis 


##  Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
cd /phone_tracker_python
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python -m phone_tracker.main
```

Or use the command-line shortcut (after setup):
```bash
phone-tracker
```

### Usage Examples

#### Interactive Mode
```bash
python -m phone_tracker.main
```
Then enter phone numbers when prompted.

#### Single Query
```bash
python -m phone_tracker.main "+27612345678"
```

#### From Python Code
```python
from phone_tracker.core import PhoneValidator, ProviderLookup, RiskAnalyzer

# Validate
validator = PhoneValidator()
is_valid, error, standardized = validator.validate("+27612345678")

# Get provider
provider, code = ProviderLookup.identify_provider(standardized)

# Risk analysis
analyzer = RiskAnalyzer()
risk = analyzer.analyze(standardized)
```

---

## 📁 Project Structure

```
phone_tracker_python/
├── phone_tracker/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── validator.py        # Phone validation
│   │   ├── provider_lookup.py  # Provider & geolocation lookup
│   │   ├── risk_analysis.py    # Risk/spam detection
│   │   └── geolocation.py      # Geographic functions
│   ├── api/                    # External services
│   │   ├── __init__.py
│   │   └── external_services.py # Geocoding and region data
│   ├── data/                   # Data files
│   │   └── sa_prefixes.json    # SA phone prefixes database
│   ├── ui/                     # User interface
│   │   ├── __init__.py
│   │   └── cli.py              # Beautiful CLI
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── formatter.py        # Number formatting & colors
│       └── logger.py           # Logging system
├── tests/
│   ├── __init__.py
│   └── test_phone_tracker.py   # Unit tests
├── setup.py                    # Setup configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

##  Core Features Explained

### 1. Phone Number Validation

Validates multiple South African phone number formats:

- **E.164 International**: `+27612345678`
- **National Format**: `0612345678`
- **Alternative**: `27612345678`

```python
from phone_tracker.core import PhoneValidator

validator = PhoneValidator()
is_valid, error, standardized = validator.validate("+27612345678")
# Returns: (True, "", "+27612345678")
```

### 2. Provider Identification

Automatically identifies mobile and fixed-line operators using the **phonenumbers library**:

- **Data Sources**: 
  - Primary: phonenumbers library carrier database (accurate, real-time data)
  - Fallback: Local prefix database for comprehensive coverage
- **Supported Operators**: MTN, Vodacom, Cell C, Telkom, Rain, Neotel, and others
- **Confidence**: HIGH when matched against phonenumbers database

```python
from phone_tracker.core import ProviderLookup

provider_info = ProviderLookup.identify_provider_detailed("+27612345678")
# Returns: {
#   'provider': 'Vodacom',
#   'code': 'VODACOM',
#   'type': 'Mobile',
#   'confidence': 'HIGH',
#   'method': 'phonenumbers_database'
# }
```

### 3. Geographic Estimation

Estimates province and city based on area code:

```python
from phone_tracker.core.provider_lookup import GeolocationLookup

region, city = GeolocationLookup.estimate_region("+27112345678")
# Returns: ("Gauteng", "Johannesburg")

coords = GeolocationLookup.get_approximate_coordinates("Gauteng")
# Returns: (-25.7461, 28.2293) estimation
```

### 4. Risk Analysis

Detects suspicious patterns:

- **Spoofing patterns** - All zeros, repeating digits
- **Rapid calls** - Multiple calls within short timeframe
- **Uncommon formats** - Malformed numbers
- **Pattern matching** - Known spam indicators

Risk levels: LOW, MEDIUM, HIGH, CRITICAL

```python
from phone_tracker.core import RiskAnalyzer

analyzer = RiskAnalyzer()
risk = analyzer.analyze("+27612345678")
# Returns: 
# {
#   'risk_score': 0,
#   'risk_level': 'LOW',
#   'flags': [],
#   'safe': True,
#   'recommendation': 'Safe to answer'
# }
```

### 5. Accurate Phone Number Information

Utilizes the **phonenumbers library** for accurate phone number information:
- Number type detection (mobile, fixed-line, VOIP)
- Company/carrier identification
- Country and region information
- Geographic descriptors from phonenumbers database

```python
import phonenumbers
from phonenumbers import carrier, geocoder

num = phonenumbers.parse("+27612345678", None)
print(carrier.name_for_number(num, "en"))  # Returns: Vodacom
print(geocoder.description_for_number(num, "en"))  # Returns: location info
```

---

## � External Data Sources

The application uses:

### Primary Data Source: phonenumbers Library
- Accurate carrier/provider information
- Real-time number type detection
- Geographic information from global phonenumbers database
- Open-source and regularly updated

### Secondary Data Source: Local Prefix Database
- South African area codes and geographic regions
- Fallback when phonenumbers library lacks specific data
- Comprehensive coverage of SA number allocations

---

## Architecture Overview

### Core Integration with phonenumbers Library

All core modules now integrate with the **phonenumbers** library:

- **validator.py**: Uses phonenumbers for accurate validation and parsing
- **provider_lookup.py**: Uses phonenumbers.carrier for accurate provider info, falls back to prefix database
- **geolocation.py**: Uses phonenumbers.geocoder for location descriptions
- **activity_status.py**: Estimates activity based on number format validity

### Standalone CLI Script

The root-level `phone_tracker.py` is a standalone script that can run independently:

```bash
python phone_tracker.py
```
---

##  Running Tests

```bash
# Run all tests
python -m tests.test_phone_tracker

# Or directly
pytest tests/
```

Test coverage includes:
- Phone number validation
- Provider identification
- Geolocation lookup
- Risk analysis
- Number formatting
- Integration tests

---

##  Example Output

```
===========================================
│            SOUTH AFRICAN PHONE          │
│              TRACKER  ENGINE            |
===========================================

📞 Enter phone number: +27612345678
⠸ Analyzing...

────────────────────────────────────────────
           ANALYSIS RESULTS
────────────────────────────────────────────

Basic Information:
  Phone Number:      +27 61 234 5678
  National Format:   061 234 5678
  Type:              MOBILE

Provider Information:
  Operator:          MTN
  Operator Code:     MTN

Geographic Information:
  Province:          Gauteng
  Primary City:      Johannesburg
  

Risk Analysis:
  Risk Level:        LOW
  Risk Score:        0/5
  Recommendation:    Safe to answer
  Flags:             None

Subscriber Information :
  Account Type:      Prepaid
  SIM Type:          Standard SIM

────────────────────────────────────────────
```

---

## 🔐 Security & Privacy

### Transparency
-  No actual tracking 
-  Simulated subscriber data 
-  Local operation 
-  Comprehensive logging for audit trails

### Data Protection
- API keys not hardcoded 
- Logs stored locally with proper permissions
- Optional privacy mode masks sensitive digits

---

## ⚙️ Configuration

The application uses the phonenumbers library for accurate data. No API keys are required for core functionality.

---

##  Logging

All phone number queries are logged for audit trails:

```
logs/
├── phone_tracker_20240325.log
├── phone_tracker_20240326.log
└── ...
```

Each query records: phone number, provider, detected region, risk level.

View recent logs:
```bash
tail -f logs/phone_tracker_$(date +%Y%m%d).log
```

---

## Advanced Usage

### Custom Validation Rules

```python
from phone_tracker.core.validator import PhoneValidator

# Extend the validator
class CustomValidator(PhoneValidator):
    @staticmethod
    def validate_with_custom_rules(phone_number):
     
        pass
```

### Creating Custom Analyzers

```python
from phone_tracker.core.risk_analysis import RiskAnalyzer

class CustomAnalyzer(RiskAnalyzer):
    @staticmethod
    def analyze_custom_patterns(phone_number):
  
        pass
```

### Pretty Printing

```python
from phone_tracker.utils import OutputFormatter

fmt = OutputFormatter()
print(fmt.success("All good!"))
print(fmt.error("Something went wrong"))
print(fmt.warning("Be careful!"))
print(fmt.info("FYI..."))
print(fmt.create_table(["Name", "Value"], [["Test", "Pass"]]))
```

---

##  Module Documentation

### Core Modules

| Module | Purpose |
|--------|---------|
| `validator.py` | Phone number format validation & normalization |
| `provider_lookup.py` | Provider identification & geolocation |
| `risk_analysis.py` | Spam/suspicious pattern detection |
| `geolocation.py` | Region information & mapping |

### Utility Modules

| Module | Purpose |
|--------|---------|
| `formatter.py` | Number formatting & colored output |
| `logger.py` | Query logging and audit trails |

### API Modules

| Module | Purpose |
|--------|---------|
| `external_services.py` | Geocoding service & region information |

---

##  Important Disclaimers

1. **Not Actual Tracking**: Geographic information is estimated based on area codes and phonenumbers database. It cannot track actual device location.

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'phone_tracker'"

Solution: Install in development mode:
```bash
pip install -e .
```

### Python version compatibility issues

Ensure Python 3.8+:
```bash
python --version
```

### Import errors in tests

Add to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m tests.test_phone_tracker
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Real-time number validation API integration
- [ ] Web interface (Flask/FastAPI)
- [ ] Advanced ML-based spam detection
- [ ] Database persistence
- [ ] Caching layer (Redis)
- [ ] REST API wrapper
- [ ] Docker containerization
 
---
