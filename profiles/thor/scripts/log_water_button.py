#!/usr/bin/env python3
"""Log a 500ml water button click into Thor's monthly food log."""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TARGET_CAL = 1950
TARGET_PROTEIN = 150
TARGET_WATER = 3000


def hermes_home() -> Path:
    import os
    return Path(os.environ.get("HERMES_HOME", "/home/hermes/.hermes/profiles/thor"))


def day_header(dt: datetime) -> str:
    return f"## {dt.strftime('%B')} {dt.day}, {dt.year} ({dt.strftime('%a')})"


def split_section(text: str, header: str):
    start = text.find(header)
    if start < 0:
        return None
    next_match = re.search(r"\n---\n\n## ", text[start + len(header):])
    if next_match:
        end = start + len(header) + next_match.start()
    else:
        next_header = re.search(r"\n## ", text[start + len(header):])
        end = start + len(header) + next_header.start() if next_header else len(text)
    return start, end, text[start:end]


def parse_num(pattern: str, text: str, default: int = 0) -> int:
    m = re.search(pattern, text)
    if not m:
        return default
    return int(m.group(1).replace(",", ""))


def upsert_water(section: str, time_label: str, amount: int) -> tuple[str, int, int, int]:
    old_water = parse_num(r"- Water:\s*([\d,]+)ml\s*/\s*3,000ml", section, 0)
    new_water = old_water + amount
    calories = parse_num(r"- Calories:\s*([\d,]+)\s*/\s*1,950", section, 0)
    protein = parse_num(r"- Protein:\s*([\d,]+)g\s*/\s*150g", section, 0)
    row = f"| {time_label} | Water | {amount}ml |"

    if "### Hydration" in section:
        hyd_start = section.index("### Hydration")
        after = section[hyd_start:]
        # Insert before the first blank line after the hydration block.
        blank = after.find("\n\n")
        if blank >= 0:
            insert_at = hyd_start + blank
            section = section[:insert_at] + "\n" + row + section[insert_at:]
        else:
            section = section.rstrip() + "\n" + row + "\n"
    else:
        hyd_block = (
            "\n### Hydration\n"
            "| Time | Item | Amount |\n"
            "|------|------|--------|\n"
            f"{row}\n"
        )
        if "### Daily totals" in section:
            idx = section.index("### Daily totals")
            section = section[:idx] + hyd_block + "\n" + section[idx:]
        else:
            section = section.rstrip() + hyd_block

    water_line = f"- Water: {new_water:,}ml / 3,000ml — {max(TARGET_WATER - new_water, 0):,}ml left"
    if re.search(r"- Water:\s*[\d,]+ml\s*/\s*3,000ml[^\n]*", section):
        section = re.sub(r"- Water:\s*[\d,]+ml\s*/\s*3,000ml[^\n]*", water_line, section)
    else:
        if "### Daily totals" not in section:
            section = section.rstrip() + "\n\n### Daily totals\n"
            section += f"- Calories: {calories:,} / 1,950 — {max(TARGET_CAL - calories, 0):,} cal left\n"
            section += f"- Protein: {protein:g}g / 150g — {max(TARGET_PROTEIN - protein, 0):g}g left\n"
        section = section.rstrip() + "\n" + water_line + "\n"
    return section, calories, protein, new_water


def parse_log_datetime(raw: str | None) -> datetime:
    """Return the reminder message datetime in PT, falling back to now."""
    tz = ZoneInfo("America/Vancouver")
    if raw:
        try:
            dt = datetime.fromisoformat(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(tz)
        except ValueError:
            pass
    return datetime.now(tz)


def main() -> int:
    try:
        amount = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    except ValueError:
        amount = 500
    log_dt = parse_log_datetime(sys.argv[2] if len(sys.argv) > 2 else None)
    time_label = log_dt.strftime("%-I:%M %p PT")
    home = hermes_home()
    log_path = home / "logs" / f"food-log-{log_dt:%Y-%m}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    text = log_path.read_text(encoding="utf-8") if log_path.exists() else f"# Thor Food & Measurement Log — {log_dt:%B %Y}\n"
    header = day_header(log_dt)
    found = split_section(text, header)
    if found is None:
        section = (
            f"\n---\n\n{header}\n\n"
            "### Hydration\n"
            "| Time | Item | Amount |\n"
            "|------|------|--------|\n"
            f"| {time_label} | Water | {amount}ml |\n\n"
            "### Daily totals\n"
            "- Calories: 0 / 1,950 — 1,950 cal left\n"
            "- Protein: 0g / 150g — 150g left\n"
            f"- Water: {amount:,}ml / 3,000ml — {TARGET_WATER - amount:,}ml left\n"
        )
        text = text.rstrip() + section
        calories, protein, water = 0, 0, amount
    else:
        start, end, section = found
        section, calories, protein, water = upsert_water(section, time_label, amount)
        text = text[:start] + section + text[end:]
    log_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    cal_left = TARGET_CAL - calories
    protein_delta = protein - TARGET_PROTEIN
    protein_phrase = f"{protein_delta:g}g over" if protein_delta > 0 else f"{abs(protein_delta):g}g left"
    print(
        f"✅ Logged {amount}ml water\n"
        f"Water: {water:,}ml / 3,000ml — {max(TARGET_WATER - water, 0):,}ml left\n"
        f"Calories: {calories:,} / 1,950 — {max(cal_left, 0):,} cal left\n"
        f"Protein: {protein:g}g / 150g — {protein_phrase}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
