from __future__ import annotations

def build_cli_banner() -> str:
    """Build the compact command-line identity shown when the app starts."""
    return r"""
   ____  _   _  ___  _   _ _____   _____ ____      _    ____ _  _______ ____  
  |  _ \| | | |/ _ \| \ | | ____| |_   _|  _ \    / \  / ___| |/ / ____|  _ \ 
  | |_) | |_| | | | |  \| |  _|     | | | |_) |  / _ \| |   | ' /|  _| | |_) |
  |  __/|  _  | |_| | |\  | |___    | | |  _ <  / ___ \ |___| . \| |___|  _ < 
  |_|   |_| |_|\___/|_| \_|_____|   |_| |_| \_\/_/   \_\____|_|\_\_____|_| \_\

  South African Phone Intelligence
  --------------------------------------------------------------------------

  Target  : Phone number analysis
  Modules : validation, carrier, location estimate, activity, risk
  Mode    : offline intelligence • no real-time tracking
"""
