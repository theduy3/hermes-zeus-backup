#!/usr/bin/env python3
"""Remove visible task sections from main theduyvault Daily Briefings.

Scope: /vault/Daily/YYYY-MM-DD.md only. Leaves *-investment.md, *-tonight.md,
CLAUDE.md, and other non-main daily files untouched.

This is for the user's standing preference that main Daily Briefings should not
show task sections or task checkboxes. It preserves personal briefing content
such as Moon Phase, Horoscope, Weather, quote, and Generated timestamp.
"""
from pathlib import Path
import re

ROOT = Path('/vault/Daily')
TASK_HEAD_RE = re.compile(r'^## (Overdue|Due Today|This Week(?: .*?)?|Next Week|Later / No Date)\b', re.M)
CHECKBOX_RE = re.compile(r'^- \[[ xX]\] ', re.M)


def clean_daily(path: Path) -> bool:
    text = path.read_text(errors='ignore')
    original = text

    # Normal path: canonical daily files put task sections between Moon Phase and Horoscope.
    if '## Moon Phase' in text and '## Horoscope' in text:
        moon = text.find('## Moon Phase')
        horo = text.find('## Horoscope', moon)
        sep = text.find('\n---', moon, horo)
        if sep != -1:
            sep_end = text.find('\n', sep + 1)
            if sep_end == -1:
                sep_end = sep + len('\n---')
            text = text[:sep_end].rstrip() + '\n\n' + text[horo:].lstrip()

    # Fallback: remove any remaining task-heading block through next non-task major section.
    while TASK_HEAD_RE.search(text):
        m = TASK_HEAD_RE.search(text)
        start = m.start()
        candidates = [
            text.find('\n## Horoscope', start),
            text.find('\n## Weather Forecast', start),
            text.find('\n*Generated:', start),
        ]
        candidates = [idx for idx in candidates if idx != -1]
        end = min(candidates) if candidates else len(text)
        text = text[:start].rstrip() + '\n\n' + text[end:].lstrip()

    text = text.lstrip('\n')
    text = re.sub(r'(?m)^[ \t]+$', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\n---\n\s*---\n', '\n---\n', text)
    text = text.rstrip() + '\n'

    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> None:
    files = sorted(p for p in ROOT.glob('????-??-??.md') if re.fullmatch(r'\d{4}-\d{2}-\d{2}\.md', p.name))
    modified = [p for p in files if clean_daily(p)]
    remaining_headings = []
    remaining_checkboxes = []
    for p in files:
        text = p.read_text(errors='ignore')
        if TASK_HEAD_RE.search(text):
            remaining_headings.append(str(p))
        if CHECKBOX_RE.search(text):
            remaining_checkboxes.append(str(p))
    print(f'main_daily_files {len(files)}')
    print(f'modified {len(modified)}')
    print(f'remaining_task_headings {len(remaining_headings)}')
    print(f'remaining_task_checkboxes {len(remaining_checkboxes)}')
    for p in remaining_headings:
        print('HEADING', p)
    for p in remaining_checkboxes:
        print('CHECKBOX', p)


if __name__ == '__main__':
    main()
