i# phone_tracker_python

# 📞 Phone Number Location Tracker

A Python-based CLI tool to trace phone numbers and retrieve location details using the Google Maps Geocoding API and the `phonenumbers` library. Specifically enhanced for South African numbers with province mapping(doesn’t actually show the precise location) but it something I am working on currently.


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


python phone_tracker.py
