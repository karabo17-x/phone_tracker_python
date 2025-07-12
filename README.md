# phone_tracker_python

# 📞 Phone Number Location Tracker

A Python-based CLI tool to trace phone numbers and retrieve location details using the Google Maps Geocoding API and the `phonenumbers` library. Specifically enhanced for South African numbers with province mapping.

---

## 🔍 Features

- Validates international phone numbers
- Identifies:
  - Carrier (service provider)
  - Country and region
  - Local area (based on number)
  - Province (for South African numbers using area code mapping)
  - Approximate location (via Google Maps Geocoding API)
- CLI interface for quick input and result display

---

## 🛠 Requirements

- Python 3.7+
- A valid [Google Maps Geocoding API Key](https://developers.google.com/maps/documentation/geocoding/get-api-key)

### Python Dependencies

Install with:

```bash
pip install -r requirements.txt

git clone https://github.com/yourusername/phone-number-location-tracker.git
cd phone-number-location-tracker


export GOOGLE_API_KEY='your-api-key-here'


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_API_KEY"


GOOGLE_API_KEY = "your-api-key-here"

python phone_tracker.py
