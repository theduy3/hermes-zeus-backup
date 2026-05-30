#!/usr/bin/env python3
"""Log a protein drink button click into Thor's monthly food log."""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TARGET_CAL = 1950
TARGET_PROTEIN = 150
TARGET_WATER = 3000
DEFAULT_CALORIES = 250


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


def protein_phrase(protein: int) -> str:
    delta = protein - TARGET_PROTEIN
    return f"{delta:g}g over" if delta > 0 else f"{abs(delta):g}g left"


def upsert_protein(section: str, time_label: str, protein_g: int, calories_add: int) -> tuple[str, int, int, int]:
    old_calories = parse_num(r"- Calories:\s*([\d,]+)\s*/\s*1,950", section, 0)
    old_protein = parse_num(r"- Protein:\s*([\d,]+)g\s*/\s*150g", section, 0)
    water = parse_num(r"- Water:\s*([\d,]+)ml\s*/\s*3,000ml", section, 0)
    new_calories = old_calories + calories_add
    new_protein = old_protein + protein_g
    row = f"| {time_label} | Protein drink | {calories_add} | {protein_g}g | 5g | 3g |"

    if "### Food Log" in section:
        food_start = section.index("### Food Log")
        after = section[food_start:]
        blank = after.find("\n\n")
        if blank >= 0:
            insert_at = food_start + blank
            section = section[:insert_at] + "\n" + row + section[insert_at:]
        else:
            section = section.rstrip() + "\n" + row + "\n"
    else:
        food_block = (
            "\n### Food Log\n"
            "| Time | Item | Cal | Protein | Carbs | Fat |\n"
            "|------|------|-----|---------|-------|-----|\n"
            f"{row}\n"
        )
        insert_markers = ["### Hydration", "### Activity", "### Daily totals"]
        insert_at = None
        for marker in insert_markers:
            if marker in section:
                insert_at = section.index(marker)
                break
        if insert_at is not None:
            section = section[:insert_at] + food_block + "\n" + section[insert_at:]
        else:
            section = section.rstrip() + food_block

    cal_line = f"- Calories: {new_calories:,} / 1,950 — {max(TARGET_CAL - new_calories, 0):,} cal left"
    prot_line = f"- Protein: {new_protein:g}g / 150g — {protein_phrase(new_protein)}"
    water_line = f"- Water: {water:,}ml / 3,000ml — {max(TARGET_WATER - water, 0):,}ml left"

    if "### Daily totals" not in section:
        section = section.rstrip() + "\n\n### Daily totals\n"
    if re.search(r"- Calories:\s*[\d,]+\s*/\s*1,950[^\n]*", section):
        section = re.sub(r"- Calories:\s*[\d,]+\s*/\s*1,950[^\n]*", cal_line, section)
    else:
        section = section.rstrip() + "\n" + cal_line
    if re.search(r"- Protein:\s*[\d,]+g\s*/\s*150g[^\n]*", section):
        section = re.sub(r"- Protein:\s*[\d,]+g\s*/\s*150g[^\n]*", prot_line, section)
    else:
        section = section.rstrip() + "\n" + prot_line
    if not re.search(r"- Water:\s*[\d,]+ml\s*/\s*3,000ml[^\n]*", section):
        section = section.rstrip() + "\n" + water_line
    return section, new_calories, new_protein, water


def parse_log_datetime(raw: str | None) -> datetime:
    """Return the actual click time in PT.

    The gateway may pass the reminder message timestamp for older buttons, but
    delayed clicks should count for the day the user pressed the button.
    """
    tz = ZoneInfo("America/Vancouver")
    return datetime.now(tz)


def main() -> int:
    try:
        protein_g = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    except ValueError:
        protein_g = 50
    calories_add = int(round(protein_g * 5)) if protein_g else DEFAULT_CALORIES
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
            "### Food Log\n"
            "| Time | Item | Cal | Protein | Carbs | Fat |\n"
            "|------|------|-----|---------|-------|-----|\n"
            f"| {time_label} | Protein drink | {calories_add} | {protein_g}g | 5g | 3g |\n\n"
            "### Daily totals\n"
            f"- Calories: {calories_add:,} / 1,950 — {TARGET_CAL - calories_add:,} cal left\n"
            f"- Protein: {protein_g:g}g / 150g — {protein_phrase(protein_g)}\n"
            "- Water: 0ml / 3,000ml — 3,000ml left\n"
        )
        text = text.rstrip() + section
        calories, protein, water = calories_add, protein_g, 0
    else:
        start, end, section = found
        section, calories, protein, water = upsert_protein(section, time_label, protein_g, calories_add)
        text = text[:start] + section + text[end:]
    log_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(
        f"✅ Logged protein drink ({protein_g}g protein)\n"
        f"Calories: {calories:,} / 1,950 — {max(TARGET_CAL - calories, 0):,} cal left\n"
        f"Protein: {protein:g}g / 150g — {protein_phrase(protein)}\n"
        f"Water: {water:,}ml / 3,000ml — {max(TARGET_WATER - water, 0):,}ml left"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
