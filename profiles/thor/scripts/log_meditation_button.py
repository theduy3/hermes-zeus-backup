#!/usr/bin/env python3
"""Log a meditation button click into Thor's monthly meditation log."""
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def hermes_home() -> Path:
    import os
    return Path(os.environ.get("HERMES_HOME", "/home/hermes/.hermes/profiles/thor"))


def main() -> int:
    try:
        minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    except ValueError:
        minutes = 10
    now = datetime.now(ZoneInfo("America/Vancouver"))
    time_label = now.strftime("%-I:%M %p PT")
    home = hermes_home()
    log_path = home / "logs" / f"meditation-log-{now:%Y-%m}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    text = log_path.read_text(encoding="utf-8") if log_path.exists() else f"# Meditation Log — {now:%B %Y}\n"
    day_header = f"## {now.strftime('%B')} {now.day}, {now.year} ({now.strftime('%a')})"
    row = f"| {time_label} | {minutes} min | Done |"
    if day_header not in text:
        text = text.rstrip() + (
            f"\n\n---\n\n{day_header}\n\n"
            "| Time | Duration | Status |\n"
            "|------|----------|--------|\n"
            f"{row}\n"
        )
    else:
        start = text.index(day_header)
        next_header = text.find("\n---\n\n## ", start + len(day_header))
        end = next_header if next_header != -1 else len(text)
        section = text[start:end]
        if "| Time | Duration | Status |" in section:
            section = section.rstrip() + "\n" + row + "\n"
        else:
            section = section.rstrip() + (
                "\n\n| Time | Duration | Status |\n"
                "|------|----------|--------|\n"
                f"{row}\n"
            )
        text = text[:start] + section + text[end:]
    log_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"✅ Meditation done\n{minutes} min logged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
