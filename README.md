# 📞 South African Phone Number Intelligence Tool


## 🎯 Overview

**Phone Tracker** is a sophisticated, modular Python application designed for analyzing South African phone numbers. It combines validation, provider identification, geolocation estimation, and risk analysis 

 **Phone Number Validation** - Multiple format support (+27, 0XX, etc.)
 **Provider Identification** - MTN, Vodacom, Cell C, Telkom, Rain, and more
 **Geographic Estimation** - Province and city inference from area codes
 **Risk Analysis** - Spam/suspicious pattern detection
 **Subscriber Information** - Simulated data (for demonstration)
 **Beautiful CLI** - Hacker-style terminal interface with colors
 **Comprehensive Logging** - Track all queries and operations
 **Unit Tests** - Full test coverage for reliability
 **Modular Architecture** - Clean, maintainable code structure
---

## 🚀 Quick Start

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
│   ├── api/                    # External API integrations
│   │   ├── __init__.py
│   │   └── external_services.py # NumVerify, AbstractAPI, mock data
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

## 🔍 Core Features Explained

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

Automatically identifies mobile and fixed-line operators:

- **MTN** - Largest operator
- **Vodacom** - Second largest
- **Cell C** - Smaller operator
- **Telkom** - Fixed-line and mobile
- **Rain** - Newer operator
- **Other** - International or unknown

```python
from phone_tracker.core import ProviderLookup

provider, code = ProviderLookup.identify_provider("+27612345678")
# Returns: ("MTN", "MTN")
```

### 3. Geographic Estimation

Estimates province and city based on area code:

- **Gauteng**: Johannesburg (011), Pretoria (012), etc.
- **Western Cape**: Cape Town (021), Stellenbosch, etc.
- **KwaZulu-Natal**: Durban (031), Pietermaritzburg, etc.
- Plus 6 other provinces

Includes mock GPS coordinates for visualization.

```python
from phone_tracker.core.provider_lookup import GeolocationLookup

region, city = GeolocationLookup.estimate_region("+27112345678")
# Returns: ("Gauteng", "Johannesburg")

coords = GeolocationLookup.get_approximate_coordinates("Gauteng")
# Returns: (-25.7461, 28.2293)
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

### 5. Subscriber Information (Simulated)

Mock subscriber data for demonstration:

⚠️ **IMPORTANT**: This is simulated data. Real telecom data is highly regulated and requires special authorization.

```python
from phone_tracker.api import MockSubscriberDatabase

data = MockSubscriberDatabase.lookup("+27612345678")
# Returns simulated account information
```

---

## 🛠️ API Integration Examples

### NumVerify API

```python
from phone_tracker.api import NumVerifyAPIClient

client = NumVerifyAPIClient(api_key="")
result = client.validate("+27612345678")
```

### AbstractAPI

```python
from phone_tracker.api import AbstractAPIClient

client = AbstractAPIClient("")
result = client.validate("+27612345678")
```

---

## 🧪 Running Tests

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

## 📊 Example Output

```
╔─────────────────────────────────────────╗
│     🔍 SOUTH AFRICAN PHONE TRACKER 🔍   │
│     Intelligence & Risk Analysis Tool   │
╚─────────────────────────────────────────╝

📞 Enter phone number: +27612345678
⠸ Analyzing...

────────────────────────────────────────────
📊 ANALYSIS RESULTS
────────────────────────────────────────────

Basic Information:
  Phone Number:      +27 61 234 5678
  National Format:   061 234 5678
  E.164 Format:      +27612345678
  Type:              MOBILE

Provider Information:
  Operator:          MTN
  Operator Code:     MTN

Geographic Information:
  Province:          Gauteng
  Primary City:      Johannesburg
  Coordinates:       -25.7461°, 28.2293°
  Accuracy:          LOW (Area code based)
  Map Link:          https://maps.google.com/?q=-25.7461,28.2293

Risk Analysis:
  Risk Level:        LOW
  Risk Score:        0/5
  Recommendation:    Safe to answer
  Flags:             None

Subscriber Information :
  Status:            ACTIVE
  Account Type:      Prepaid
  SIM Type:          Standard SIM
  Activation Date:   2020-05-15
  Last Activity:     2024-03-25
  Note: This is simulated data for demonstration purposes only.

────────────────────────────────────────────
```

---

## 🔐 Security & Privacy

### Transparency
- ✓ No actual tracking 
- ✓ Simulated subscriber data 
- ✓ Local operation 
- ✓ Comprehensive logging for audit trails

### Data Protection
- API keys not hardcoded 
- Logs stored locally with proper permissions
- Optional privacy mode masks sensitive digits

---

## ⚙️ Configuration


### Using in Code

```python
from phone_tracker.api import EnrichmentService

enrichment = EnrichmentService(
    numverify_key="",
    abstractapi_key=""
)
```

---

## 📝 Logging

Logs are automatically saved to `logs/` directory:

```
logs/
├── phone_tracker_20240325.log
├── phone_tracker_20240326.log
└── ...
```

View recent logs:
```bash
tail -f logs/phone_tracker_$(date +%Y%m%d).log
```

---

## 🚀 Advanced Usage

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

## 📖 Module Documentation

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
| `external_services.py` | API integrations & mock databases |

---

## ⚠️ Important Disclaimers

1. **Not Actual Tracking**: This tool estimates location based on area codes only. It cannot track actual device location.

2. **No Real Subscriber Data**: Subscriber information shown is simulated data for demonstration purposes.

3. **Educational Purpose**: Designed for cybersecurity education, testing.


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

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for usage examples

