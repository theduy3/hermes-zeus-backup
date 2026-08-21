#!/usr/bin/env python3
"""2026 Planner page map for reMarkable notebook.

Anchors (user-verified):
  p2  = year calendar
  p69 = Week 34  -> 35 + W
  p550 = Aug 19 notes
  p551 = Aug 20 schedule

Formulas (1-based page numbers):
  Year:       2–3          (2 calendar, 3 goals)
  Quarter Q:  2+2Q, 3+2Q   (Q=1..4)  -> pages 4–11
  Month M:    10+2M, 11+2M (M=1..12) -> pages 12–35
  Week W:     35+W         (W=1..53) -> pages 36–88
  Day DOY:    schedule = 89+(DOY-1)*2 ; notes = schedule+1  -> 89–818
  Exercise:   963 (fixed grid)
  Meditation: 964 (fixed grid)
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable


YEAR = 2026  # page geometry for the current bound planner year
EXERCISE_PAGE = 963
MEDITATION_PAGE = 964
YEAR_CALENDAR_PAGE = 2
YEAR_GOALS_PAGE = 3

# Match any notebook whose name contains this token (case-insensitive),
# e.g. "2026 Planner", "2027 Planner", "Planner 2028".
PLANNER_NAME_SUBSTRING = "Planner"


def is_planner_document(name: str | None) -> bool:
    """True if a reMarkable document title should be treated as a yearly planner."""
    if not name:
        return False
    return PLANNER_NAME_SUBSTRING.casefold() in str(name).casefold()


def pick_planner_document(candidates: list[str], *, prefer_year: int | None = None) -> str | None:
    """Pick the best planner notebook from titles.

    Preference order:
      1) contains Planner and the prefer_year (default: YEAR)
      2) contains Planner and the latest 4-digit year found in the title
      3) first title containing Planner
    """
    import re

    planners = [c for c in candidates if is_planner_document(c)]
    if not planners:
        return None
    year = prefer_year if prefer_year is not None else YEAR

    def years_in(title: str) -> list[int]:
        return [int(y) for y in re.findall(r"\b(20\d{2})\b", title)]

    exact = [p for p in planners if year in years_in(p)]
    if exact:
        # Prefer titles that look like "<year> Planner"
        exact.sort(key=lambda t: (0 if re.search(rf"\b{year}\b.*planner|planner.*\b{year}\b", t, re.I) else 1, t))
        return exact[0]

    def max_year(title: str) -> int:
        ys = years_in(title)
        return max(ys) if ys else -1

    planners_sorted = sorted(planners, key=lambda t: (max_year(t), t), reverse=True)
    return planners_sorted[0]


@dataclass(frozen=True)
class DayPages:
    day: date
    doy: int
    schedule: int
    notes: int


def doy(d: date) -> int:
    if d.year != YEAR:
        raise ValueError(f"page map is for {YEAR} only, got {d.year}")
    return d.timetuple().tm_yday


def iso_week(d: date) -> int:
    if d.year != YEAR:
        raise ValueError(f"page map is for {YEAR} only, got {d.year}")
    return int(d.isocalendar().week)


def quarter(d: date) -> int:
    return (d.month - 1) // 3 + 1


def year_pages() -> tuple[int, int]:
    return YEAR_CALENDAR_PAGE, YEAR_GOALS_PAGE


def quarter_pages(q: int) -> tuple[int, int]:
    if q not in range(1, 5):
        raise ValueError(f"quarter must be 1..4, got {q}")
    return 2 + 2 * q, 3 + 2 * q


def month_pages(m: int) -> tuple[int, int]:
    if m not in range(1, 13):
        raise ValueError(f"month must be 1..12, got {m}")
    return 10 + 2 * m, 11 + 2 * m


def week_page(w: int) -> int:
    if w not in range(1, 54):
        raise ValueError(f"week must be 1..53, got {w}")
    return 35 + w


def day_pages(d: date) -> DayPages:
    n = doy(d)
    schedule = 89 + (n - 1) * 2
    return DayPages(day=d, doy=n, schedule=schedule, notes=schedule + 1)


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def layers_for_date(d: date) -> dict:
    """All planner layers relevant to a calendar day."""
    dp = day_pages(d)
    y_cal, y_goals = year_pages()
    q = quarter(d)
    q_a, q_b = quarter_pages(q)
    m_a, m_b = month_pages(d.month)
    w = iso_week(d)
    return {
        "date": d.isoformat(),
        "doy": dp.doy,
        "iso_week": w,
        "quarter": q,
        "year": {"calendar": y_cal, "goals": y_goals},
        "quarter_pages": {"a": q_a, "b": q_b},
        "month_pages": {"a": m_a, "b": m_b},
        "week_page": week_page(w),
        "day": {"schedule": dp.schedule, "notes": dp.notes},
        "habits": {"exercise": EXERCISE_PAGE, "meditation": MEDITATION_PAGE},
    }


def daily_sync_pages(d: date) -> list[dict]:
    """Pages a daily sync should pull (minimal set)."""
    L = layers_for_date(d)
    out = [
        {"role": "day_schedule", "page": L["day"]["schedule"], "date": L["date"]},
        {"role": "day_notes", "page": L["day"]["notes"], "date": L["date"]},
        {"role": "week", "page": L["week_page"], "week": L["iso_week"]},
        {"role": "exercise_grid", "page": EXERCISE_PAGE},
        {"role": "meditation_grid", "page": MEDITATION_PAGE},
    ]
    # Include month/quarter/year goals on Mondays and day-1 of month.
    d0 = parse_date(L["date"]) if isinstance(L["date"], str) else d
    if d0.day == 1 or d0.weekday() == 0:
        out.append({"role": "month_a", "page": L["month_pages"]["a"], "month": d0.month})
        out.append({"role": "month_b", "page": L["month_pages"]["b"], "month": d0.month})
    if d0.day == 1 and d0.month in (1, 4, 7, 10):
        out.append({"role": "quarter_a", "page": L["quarter_pages"]["a"], "quarter": L["quarter"]})
        out.append({"role": "quarter_b", "page": L["quarter_pages"]["b"], "quarter": L["quarter"]})
    if d0.month == 1 and d0.day <= 7:
        out.append({"role": "year_calendar", "page": YEAR_CALENDAR_PAGE})
        out.append({"role": "year_goals", "page": YEAR_GOALS_PAGE})
    return out


def self_check() -> list[str]:
    """Return list of failures; empty means OK."""
    fails: list[str] = []
    # Anchors
    a19 = day_pages(date(2026, 8, 19))
    if (a19.schedule, a19.notes) != (549, 550):
        fails.append(f"Aug19 expected 549/550 got {a19.schedule}/{a19.notes}")
    a20 = day_pages(date(2026, 8, 20))
    if (a20.schedule, a20.notes) != (551, 552):
        # User said p551 = Aug 20 schedule; notes would be 552
        fails.append(f"Aug20 schedule expected 551 got {a20.schedule}")
    if week_page(34) != 69:
        fails.append(f"Week34 expected 69 got {week_page(34)}")
    if year_pages() != (2, 3):
        fails.append("year pages")
    # Range sanity
    if day_pages(date(2026, 1, 1)).schedule != 89:
        fails.append("Jan1 schedule")
    if day_pages(date(2026, 12, 31)).notes != 89 + (365 - 1) * 2 + 1:
        fails.append("Dec31 notes")
    # month/quarter ends
    if month_pages(1) != (12, 13) or month_pages(12) != (34, 35):
        fails.append("month range")
    if quarter_pages(1) != (4, 5) or quarter_pages(4) != (10, 11):
        fails.append("quarter range")
    return fails


def pages_csv(items: Iterable[dict]) -> str:
    return ",".join(str(i["page"]) for i in items)


if __name__ == "__main__":
    import json
    import sys

    fails = self_check()
    if fails:
        print("SELF_CHECK_FAIL", fails, file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        print("OK page_map self-check passed")
        sys.exit(0)
    d = parse_date(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    if d.year != YEAR:
        # allow computing map for 2026 planner even if wall clock differs
        try:
            d = parse_date(sys.argv[1])
        except Exception:
            d = date(YEAR, 8, 20)
    print(json.dumps({"layers": layers_for_date(d), "daily_sync": daily_sync_pages(d)}, indent=2))
