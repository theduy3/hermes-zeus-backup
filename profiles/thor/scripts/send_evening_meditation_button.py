#!/usr/bin/env python3
"""Send Thor evening meditation reminder with music link and Done button."""
import os
import runpy
from pathlib import Path

os.environ.setdefault(
    "THOR_MEDITATION_REMINDER_TEXT",
    "🧘 Evening meditation — 20 min.\nMusic: https://music.youtube.com/watch?v=ThyQNMZZH-E&si=D-8kcTEkkpHdVKUV",
)
os.environ.setdefault("THOR_MEDITATION_MINUTES", "20")

script = Path(__file__).with_name("send_meditation_button.py")
runpy.run_path(str(script), run_name="__main__")
