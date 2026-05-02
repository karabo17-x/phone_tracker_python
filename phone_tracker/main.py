import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phone_tracker.ui.cli import run_cli


if __name__ == "__main__":
    run_cli()
