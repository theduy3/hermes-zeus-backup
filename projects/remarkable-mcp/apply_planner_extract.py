#!/usr/bin/env python3
"""Apply a structured extract from the 2026 Planner into vault + Life OS.

Hardening applied (2026-08-20):
  A. IDEMPOTENCY — each page is written inside a delimited block
     <!-- rm:NNN --> ... <!-- /rm:NNN --> in the daily mirror. Re-running
     overwrites only the blocks for pages present in THIS extract (last-write-
     wins per page). Pages not in this run are left untouched. Handwriting
     transcription is non-deterministic, so a page is a snapshot, mirrored as a
     snapshot — never deduped/appended.
  B. HABIT GRIDS (p963/p964) — NOT auto-parsed. A confirm gate requires an
     explicit --confirm-habits (or habits_confirmed:true) before any Life OS
     habit write. Until then, marks are recorded in the mirror as UNCONFIRMED
     and low confidence, and nothing is written to Life OS.
  C. PNG GROUND TRUTH — each page block can carry a `png:` relative path to the
     rendered stroke image, so an agent can fall back to the original instead of
     trusting lossy OCR. Set capture_pngs:true to fetch them live.
  D. CONFIDENCE — per-page + overall confidence in frontmatter. Habit extractions
     are forced to confidence:low and Life OS events are flagged estimated.

Authority rules (Life OS migration plan):
  - /vault/Tasks/ = dated task authority
  - Life OS Markdown = health/habit observations + strategic goals context
  - Never invent values; only write fields present in the extract JSON

Input JSON schema (pages array is preferred; legacy flat fields are mapped):
{
  "date": "YYYY-MM-DD",
  "source_document": "2026 Planner",
  "confidence": "high|medium|low",
  "pages": [
    {"page": 551, "role": "day_schedule", "text": "...", "png": null,
     "confidence": "high", "capture": false},
    {"page": 963, "role": "exercise_grid",
     "text": "Aug 14, 17, 18, 19 (read from grid, UNCONFIRMED)",
     "png": null, "confidence": "low"},
    ...
  ],
  "tasks": [{"title": "...", "done": false, "due": "YYYY-MM-DD", "notes": "..."}],
  "goals":  [{"title": "...", "area": "health", "status": "active", "note": "..."}],
  "exercise": {"done": true, "minutes": 45, "note": "gym legs"},
  "meditation": {"done": true, "minutes": 10, "note": "breath"},
  "capture_pngs": false,
  "habits_confirmed": false,
  "dry_run": false
}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(os.environ.get("THE_DUY_VAULT", "/vault"))
PLAN_DIR = VAULT / "Tasks" / "planning" / "remarkable"
ASSETS_DIR = PLAN_DIR / "assets"
TASKS_DIR = VAULT / "Tasks" / "tasks"
LIFE_TRACKER = Path("/home/hermes/.hermes/projects/life-os/tracker")
STATE_DIR = Path.home() / ".hermes" / "projects" / "remarkable-mcp" / "state"


# --------------------------------------------------------------------------
# Delimited-block idempotency
# --------------------------------------------------------------------------
def block_re(key: str) -> re.Pattern:
    return re.compile(
        r"<!--\s*rm:" + re.escape(key) + r"\s*-->.*?<!--\s*/rm:" + re.escape(key) + r"\s*-->",
        re.DOTALL,
    )


def replace_blocks(content: str, updates: dict[str, str]) -> str:
    """Replace each keyed block in `content` (or append if absent)."""
    for key, block in updates.items():
        pat = block_re(key)
        if pat.search(content):
            content = pat.sub(lambda m: block, content, count=1)
        else:
            content = content.rstrip() + "\n\n" + block + "\n"
    return content


def render_block(key: str, title: str, text: str | None, png_rel: str | None,
                 confidence: str | None) -> str:
    lines = [f"<!-- rm:{key} -->", f"## Page {title}"]
    if confidence:
        lines.append(f"confidence: {confidence}")
    if png_rel:
        lines.append(f"png: {png_rel}")
    lines.append("")
    lines.append((text or "_no extract_").rstrip())
    lines.append(f"<!-- /rm:{key} -->")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60] or "item"


def write_text(path: Path, content: str, dry: bool) -> None:
    if dry:
        print(f"DRY write {path} ({len(content)} bytes)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE {path}")


def split_frontmatter(content: str) -> tuple[str, str]:
    if content.startswith("---\n"):
        end = content.find("\n---\n", 1)
        if end != -1:
            return content[: end + 5], content[end + 5 :]
    return "", content


def build_pages(data: dict) -> list[dict]:
    """Return a list of page dicts from the preferred `pages` array or legacy flat fields."""
    pages = data.get("pages")
    if pages:
        return pages
    out: list[dict] = []
    if data.get("day_schedule_text"):
        out.append({"page": 551, "role": "day_schedule", "text": data["day_schedule_text"]})
    if data.get("day_notes_text"):
        out.append({"page": 552, "role": "day_notes", "text": data["day_notes_text"]})
    raw = data.get("raw_ocr") or {}
    if raw.get("963") or data.get("exercise"):
        out.append({"page": 963, "role": "exercise_grid", "text": raw.get("963"),
                    "confidence": "low"})
    if raw.get("964") or data.get("meditation"):
        out.append({"page": 964, "role": "meditation_grid", "text": raw.get("964"),
                    "confidence": "low"})
    return out


# --------------------------------------------------------------------------
# Rendering the daily mirror
# --------------------------------------------------------------------------
AUTHORITY = (
    "\n## Authority\n"
    "- Dated tasks authority: `/vault/Tasks/`\n"
    "- Health/habit observations: Life OS `30-health/`\n"
    "- Strategic goals context: Life OS `70-goals/`\n"
    "- This file is a sourced mirror of the reMarkable planner extract only.\n"
    "- Per-page blocks (<!-- rm:NNN -->) are snapshots; re-runs overwrite in place.\n"
)


def render_frontmatter(data: dict, habits_confirmed: bool, conf: str) -> str:
    pages = build_pages(data)
    pages_read = data.get("pages_read") or [p["page"] for p in pages]
    return "\n".join([
        "---",
        "type: remarkable-planner-sync",
        f"date: {data['date']}",
        f"source_document: {data.get('source_document', 'Planner')}",
        f"pages_read: {json.dumps(pages_read)}",
        f"confidence: {conf}",
        f"habits_confirmed: {str(habits_confirmed).lower()}",
        f"synced_at: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "tags: [remarkable, planner, sync]",
        "---",
    ])


def render_tasks_block(tasks: list[dict], date: str) -> str:
    lines = ["## Tasks from planner"]
    if not tasks:
        lines.append("_none extracted_")
    for t in tasks:
        mark = "x" if t.get("done") else " "
        due = t.get("due") or date
        title = t.get("title") or "untitled"
        extra = f" — {t['notes']}" if t.get("notes") else ""
        lines.append(f"- [{mark}] {title} (due {due}){extra}")
    return render_block("tasks", "Tasks", "\n".join(lines), None, None)


def render_goals_block(goals: list[dict]) -> str:
    lines = ["## Goals from planner"]
    if not goals:
        lines.append("_none extracted_")
    for g in goals:
        lines.append(
            f"- {g.get('title')} | area={g.get('area')} status={g.get('status')} | {g.get('note') or ''}"
        )
    return render_block("goals", "Goals", "\n".join(lines), None, None)


# --------------------------------------------------------------------------
# Life OS writes (gated by habit confirmation)
# --------------------------------------------------------------------------
def run_thor(data: dict, dry: bool, habits_confirmed: bool) -> str | None:
    ex = data.get("exercise") or {}
    if not ex:
        return None
    if ex.get("minutes") is None and not ex.get("note") and ex.get("done") is not True:
        return None
    if not habits_confirmed:
        print("HABIT GATE: exercise unconfirmed — skipping Life OS write")
        return "gated:exercise"
    cmd = [
        sys.executable,
        str(LIFE_TRACKER / "thor_log.py"),
        "--date", data["date"],
        "--event-id", f"thor-rm-{data['date']}",
    ]
    if ex.get("minutes") is not None:
        cmd += ["--exercise-minutes", str(int(ex["minutes"]))]
    note_parts = []
    if ex.get("done") is True:
        note_parts.append("exercise done (remarkable planner grid)")
    elif ex.get("done") is False:
        note_parts.append("exercise not done (remarkable planner grid)")
    if ex.get("note"):
        note_parts.append(str(ex["note"]))
    note_parts.append("source=remarkable-2026-planner")
    cmd += ["--note", "; ".join(note_parts)]
    if dry:
        print("DRY", " ".join(cmd))
        return "dry:thor"
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return f"thor_error:{r.returncode}"
    return "thor_ok"


def run_meditation(data: dict, dry: bool, habits_confirmed: bool, conf: str) -> str | None:
    med = data.get("meditation") or {}
    if not med:
        return None
    if med.get("minutes") is None and not med.get("note") and med.get("done") is not True:
        return None
    if not habits_confirmed:
        print("HABIT GATE: meditation unconfirmed — skipping Life OS write")
        return "gated:meditation"
    sys.path.insert(0, str(LIFE_TRACKER))
    import life_store as s  # noqa

    payload = {"source": "remarkable-2026-planner"}
    if med.get("minutes") is not None:
        payload["meditation_minutes"] = int(med["minutes"])
    if med.get("done") is True:
        payload["meditation_done"] = True
    elif med.get("done") is False:
        payload["meditation_done"] = False
    if med.get("note"):
        payload["note"] = str(med["note"])
    event_id = f"med-rm-{data['date']}"
    estimated = (conf == "low")
    if dry:
        print("DRY life_store health observation", event_id, payload, "estimated=", estimated)
        return "dry:med"
    try:
        rec = s.write(
            "health", "observation", data["date"], payload,
            event_id=event_id, source_ids=("remarkable_planner",), estimated=estimated,
        )
        print(f"OK meditation event {rec['id']}")
        return "med_ok"
    except Exception as e:
        print(f"meditation write error: {e}", file=sys.stderr)
        return f"med_error:{e}"


def run_goals(data: dict, dry: bool) -> list[str]:
    out = []
    for g in data.get("goals") or []:
        title = (g.get("title") or "").strip()
        if not title:
            continue
        gid = g.get("id") or f"goal-rm-{slug(title)}"
        cmd = [
            sys.executable, str(LIFE_TRACKER / "life_log.py"),
            "--date", data["date"], "--kind", "goal", "--id", gid, "--title", title,
            "--source", f"remarkable-2026-planner:{data['date']}",
        ]
        if g.get("area"):
            cmd += ["--area", str(g["area"])]
        if g.get("status"):
            cmd += ["--status", str(g["status"])]
        if g.get("note"):
            cmd += ["--note", str(g["note"])]
        if dry:
            print("DRY", " ".join(cmd))
            out.append(f"dry:{gid}")
            continue
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            out.append(f"err:{gid}")
        else:
            out.append(f"ok:{gid}")
    return out


def maybe_create_tasks(data: dict, dry: bool) -> list[str]:
    created = []
    d = data["date"]
    for t in data.get("tasks") or []:
        title = (t.get("title") or "").strip()
        if not title or t.get("done"):
            continue
        if t.get("skip_vault_task"):
            continue
        fn = f"rm-planner-{d}-{slug(title)}.md"
        path = TASKS_DIR / fn
        if path.exists():
            created.append(f"exists:{path}")
            continue
        due = t.get("due") or d
        body = "\n".join([
            "---", "type: task", f"due_date: {due}",
            "tags: [remarkable-planner, synced]", "status: pending",
            "source: remarkable-2026-planner", "---",
            f"# {title}", "", t.get("notes") or "", "",
            f"Imported from reMarkable 2026 Planner extract for {d}.",
            f"See also: [[Tasks/planning/remarkable/{d}]]", "",
        ])
        write_text(path, body, dry)
        created.append(str(path))
    return created


# --------------------------------------------------------------------------
# Habit confirmation gate
# --------------------------------------------------------------------------
def confirm_habit_marks(data: dict) -> None:
    """Print the habit marks read from the grids so the user can verify them."""
    marks = []
    ex = data.get("exercise") or {}
    med = data.get("meditation") or {}
    if ex.get("note"):
        marks.append(f"exercise: {ex['note']}")
    if med.get("note"):
        marks.append(f"meditation: {med['note']}")
    # also surface any grid page text
    for p in build_pages(data):
        if p.get("role") in ("exercise_grid", "meditation_grid") and p.get("text"):
            marks.append(f"p{p['page']} ({p['role']}): {p['text']}")
    print("\n=== HABIT MARKS READ FROM GRID (verify on device before confirming) ===")
    if marks:
        for m in marks:
            print("  -", m)
    else:
        print("  (none)")
    print("  To write these to Life OS, re-run with --confirm-habits or set habits_confirmed:true.")
    print("=== end ===\n")


# --------------------------------------------------------------------------
# PNG capture (C)
# --------------------------------------------------------------------------
def capture_pngs_for_pages(data: dict, pages: list[dict], dry: bool) -> None:
    if not data.get("capture_pngs"):
        return
    try:
        from rm_capture import capture_page
    except Exception as e:
        print(f"PNG capture skipped (module error: {e})", file=sys.stderr)
        return
    doc = data.get("source_document") or "2026 Planner"
    d = data["date"]
    for p in pages:
        if p.get("png"):
            continue  # already have a path
        if not p.get("capture", True):
            continue
        out = ASSETS_DIR / d / f"{p['page']}.png"
        rel = f"assets/{d}/{p['page']}.png"
        if dry:
            print(f"DRY capture p{p['page']} -> {out}")
            p["png"] = rel
            continue
        try:
            ok = capture_page(doc, p["page"], out)
            if ok:
                p["png"] = rel
                print(f"CAPTURED p{p['page']} -> {out}")
            else:
                print(f"capture failed p{p['page']}", file=sys.stderr)
        except Exception as e:
            print(f"capture error p{p['page']}: {e}", file=sys.stderr)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, help="path to extract JSON or - for stdin")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-tasks", action="store_true")
    ap.add_argument("--no-lifeos", action="store_true")
    ap.add_argument("--confirm-habits", action="store_true",
                    help="Allow Life OS habit writes (only after verifying marks)")
    ap.add_argument("--no-capture", action="store_true", help="skip PNG capture even if requested")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.json == "-" else Path(args.json).read_text(encoding="utf-8")
    data = json.loads(raw)
    if args.dry_run:
        data["dry_run"] = True
    dry = bool(data.get("dry_run") or args.dry_run)
    if args.no_capture:
        data["capture_pngs"] = False

    if "date" not in data:
        print("ERROR: extract.date required", file=sys.stderr)
        return 2
    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        print("ERROR: bad date", file=sys.stderr)
        return 2

    habits_confirmed = bool(data.get("habits_confirmed") or args.confirm_habits)

    pages = build_pages(data)
    overall_conf = data.get("confidence", "unknown")

    # B: print habit marks for verification
    if any(p.get("role") in ("exercise_grid", "meditation_grid") for p in pages) or \
       data.get("exercise") or data.get("meditation"):
        confirm_habit_marks(data)

    # C: capture PNGs (mutates p["png"])
    if not args.no_capture:
        capture_pngs_for_pages(data, pages, dry)

    # A: build per-page blocks
    blocks: dict[str, str] = {}
    for p in pages:
        key = str(p["page"])
        png = p.get("png")
        conf = p.get("confidence") or overall_conf
        if p.get("role") in ("exercise_grid", "meditation_grid") and not habits_confirmed:
            conf = "low"
            note = "\n(UNCONFIRMED — awaiting device verification; not written to Life OS)"
            text = (p.get("text") or "") + note
        else:
            text = p.get("text")
        blocks[key] = render_block(
            key, f"{p.get('role', 'page')} (p{p['page']})", text, png, conf
        )
    blocks["tasks"] = render_tasks_block(data.get("tasks") or [], data["date"])
    blocks["goals"] = render_goals_block(data.get("goals") or [])

    # Merge into existing daily mirror (per-page overwrite)
    plan_path = PLAN_DIR / f"{data['date']}.md"
    existing = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    fm, body = split_frontmatter(existing)
    new_body = replace_blocks(body, blocks)
    if "## Authority" not in new_body:
        new_body = new_body.rstrip() + AUTHORITY
    new_fm = render_frontmatter(data, habits_confirmed, overall_conf)
    final = new_fm + "\n" + new_body + "\n"
    write_text(plan_path, final, dry)

    created = [] if args.no_tasks else maybe_create_tasks(data, dry)
    life: dict = {}
    if not args.no_lifeos:
        life["thor"] = run_thor(data, dry, habits_confirmed)
        life["meditation"] = run_meditation(data, dry, habits_confirmed, overall_conf)
        life["goals"] = run_goals(data, dry)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        "date": data["date"], "plan_path": str(plan_path), "tasks": created,
        "lifeos": life, "pages_read": [p["page"] for p in pages],
        "confidence": overall_conf, "habits_confirmed": habits_confirmed,
        "dry_run": dry, "applied_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    state_path = STATE_DIR / f"apply-{data['date']}.json"
    if not dry:
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
