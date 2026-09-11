#!/usr/bin/env python3
import runpy
import sys
from pathlib import Path

script = Path(__file__).with_name("daily_hermes_update.py")
sys.argv = [str(script), "--restore-only"]
runpy.run_path(str(script), run_name="__main__")
