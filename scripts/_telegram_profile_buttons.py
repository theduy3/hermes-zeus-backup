"""Cron-sent Telegram task/wellness button callbacks.

Stock Hermes `_handle_callback_query` only routes model-picker, approval, and
gmail-triage prefixes. Profile cron scripts emit `zt:`/`ct:`/`wl:` cards, and
`hermes update` wipes any in-adapter patch. Keep the logic here and dispatch
from adapter.py.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_STALE = {"completed", "done", "cancelled", "canceled", "deleted"}
_VAULT_TASKS = Path("/vault/Tasks/tasks")

_WELLNESS_SCRIPTS = {
    "water": ("log_water_button.py", "Logged {n}ml water"),
    "protein": ("log_protein_button.py", "Logged protein drink"),
    "sitz": ("log_sitz_button.py", "Sitz bath done"),
    "meditation": ("log_meditation_button.py", "Meditation done"),
}


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:
        return {}


def _save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _set_fm(text: str, field: str, value: str) -> str:
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    fm = parts[1]
    pattern = re.compile(rf"^{re.escape(field)}:.*$", re.MULTILINE)
    if pattern.search(fm):
        fm = pattern.sub(f"{field}: {value}", fm, count=1)
    else:
        fm = fm.rstrip("\n") + f"\n{field}: {value}\n"
    return "---" + fm + "---" + parts[2]


def _get_fm(text: str, field: str) -> Optional[str]:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    m = re.search(rf"^{re.escape(field)}:\s*(.*)$", parts[1], re.MULTILINE)
    return m.group(1).strip() if m else None


def _safe_vault_task(path: Path) -> bool:
    try:
        resolved = path.expanduser().resolve()
        root = _VAULT_TASKS.resolve()
        return resolved == root or root in resolved.parents
    except Exception:
        return False


def _check_off_line(text: str, title: str, line_no: Any) -> str:
    lines = text.splitlines()
    needle = title.strip()
    idx = None
    try:
        n = int(line_no)
        if 1 <= n <= len(lines) and needle and needle in lines[n - 1] and "- [ ]" in lines[n - 1]:
            idx = n - 1
    except (TypeError, ValueError):
        pass
    if idx is None:
        for i, line in enumerate(lines):
            if needle and needle in line and "- [ ]" in line:
                idx = i
                break
    if idx is None:
        return text
    lines[idx] = lines[idx].replace("- [ ]", "- [x]", 1)
    out = "\n".join(lines)
    return out + ("\n" if text.endswith("\n") else "")


def _task_keyboard(digest: str, flavor: str):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    if flavor == "drip":
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("Done", callback_data=f"zt:{digest}"),
            InlineKeyboardButton("Delay", callback_data=f"delay:{digest}"),
            InlineKeyboardButton("Delete", callback_data=f"del:{digest}"),
        ]])
    if flavor == "catthew":
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Done", callback_data=f"ct:{digest}"),
            InlineKeyboardButton("More", callback_data=f"ctm:{digest}"),
        ]])
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Done", callback_data=f"zt:{digest}"),
        InlineKeyboardButton("More", callback_data=f"ztm:{digest}"),
    ]])


def _wellness_keyboard(kind: str, amount: str, *, more: bool):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    labels = {
        "water": f"✅ Log {amount}ml",
        "protein": "✅ Log protein drink",
        "sitz": "✅ Done",
        "meditation": f"✅ Log {amount} min",
    }
    log_label = labels.get(kind, "✅ Log")
    if more:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(log_label, callback_data=f"wl:{kind}:{amount}"),
            InlineKeyboardButton("◀ Back", callback_data=f"wlb:{kind}:{amount}"),
        ]])
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(log_label, callback_data=f"wl:{kind}:{amount}"),
        InlineKeyboardButton("More", callback_data=f"wlm:{kind}:{amount}"),
    ]])


async def handle_task_card(adapter, query, data: str, cb: Dict[str, Any]) -> None:
    if not await adapter._callback_authorized(query, cb, "⛔ You are not authorized to act on this task card."):
        return
    from hermes_constants import get_hermes_home

    home = get_hermes_home()
    registry_path = home / "task_buttons" / "registry.json"
    catthew_tasks = home / "tasks.md"

    if data.startswith("dl:"):
        parts = data.split(":", 2)
        digest = parts[1] if len(parts) > 1 else ""
        try:
            offset_days = int(parts[2]) if len(parts) > 2 else 0
        except ValueError:
            offset_days = 0
        await _delay_offset(adapter, query, registry_path, digest, offset_days)
        return

    digest = data.split(":", 1)[1] if ":" in data else ""
    reg = _load_json(registry_path)
    entry = reg.get(digest)
    if not entry:
        await query.answer(text="This task card has expired.")
        return
    title = entry.get("title") or entry.get("text") or "Task"
    file_path = Path(str(entry.get("file_path") or ""))

    if data.startswith(("ztm:", "ctm:")):
        source = entry.get("source") or ""
        due = entry.get("due_date") or entry.get("date") or ""
        details = f"{title}"
        if source:
            details += f"\nSource: {source}"
        if due:
            details += f"\nDue: {due}"
        flavor = "catthew" if data.startswith("ctm:") else "daily"
        await query.answer()
        try:
            await query.edit_message_text(text=details, reply_markup=_task_keyboard(digest, flavor))
        except Exception as exc:
            logger.error("[%s] task-card more failed: %s", adapter.name, exc)
        return

    if data.startswith("delay:"):
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        try:
            await query.answer()
            await query.edit_message_text(
                text=f"⏰ {title} — delay by:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("+1 day", callback_data=f"dl:{digest}:1"),
                    InlineKeyboardButton("+3 days", callback_data=f"dl:{digest}:3"),
                    InlineKeyboardButton("+1 week", callback_data=f"dl:{digest}:7"),
                ]]),
            )
        except Exception as exc:
            logger.error("[%s] task-card delay prompt failed: %s", adapter.name, exc)
        return

    if data.startswith("del:"):
        try:
            if file_path.as_posix() not in ("", ".") and _safe_vault_task(file_path) and file_path.exists():
                file_path.unlink()
            reg.pop(digest, None)
            _save_json(registry_path, reg)
            await query.answer(text="Deleted")
            try:
                await query.edit_message_text(text=f"🗑 Deleted — {title}", reply_markup=None)
            except Exception:
                pass
        except Exception as exc:
            logger.error("[%s] task-card delete failed: %s", adapter.name, exc)
            await query.answer(text="Could not delete.")
        return

    if data.startswith(("zt:", "ct:")):
        await _mark_done(adapter, query, registry_path, reg, digest, entry, file_path, catthew_tasks, title, data.startswith("ct:"))
        return
    await query.answer(text="Unknown task action.")


async def _delay_offset(adapter, query, registry_path: Path, digest: str, offset_days: int) -> None:
    reg = _load_json(registry_path)
    entry = reg.get(digest)
    if not entry:
        await query.answer(text="This task card has expired.")
        return
    file_path = Path(str(entry.get("file_path") or ""))
    title = entry.get("title") or entry.get("text") or "Task"
    existing = ""
    if file_path.as_posix() not in ("", ".") and _safe_vault_task(file_path) and file_path.exists():
        try:
            existing = file_path.read_text(encoding="utf-8")
        except Exception:
            existing = ""
    status = (_get_fm(existing, "status") or str(entry.get("status") or "")).lower()
    if status in _STALE:
        await query.answer(text=f"Already {status} — no change made.")
        return
    used_today = False
    try:
        base_date = date.fromisoformat(str(entry.get("due_date") or ""))
    except ValueError:
        base_date = date.today()
        used_today = True
    new_due = (base_date + timedelta(days=offset_days)).isoformat()
    suffix = " (couldn't read original due date, offset from today)" if used_today else ""
    try:
        if existing:
            file_path.write_text(_set_fm(existing, "due_date", new_due), encoding="utf-8")
        entry["due_date"] = new_due
        entry["status"] = "delayed"
        reg[digest] = entry
        _save_json(registry_path, reg)
        await query.answer(text=f"⏰ Delayed to {new_due}{suffix}")
        try:
            await query.edit_message_text(text=f"⏰ {title} — delayed to {new_due}{suffix}", reply_markup=None)
        except Exception:
            pass
    except Exception as exc:
        logger.error("[%s] task-card delay-offset failed: %s", adapter.name, exc)
        await query.answer(text="Could not update the task file.")


async def _mark_done(adapter, query, registry_path, reg, digest, entry, file_path, catthew_tasks, title, is_catthew) -> None:
    try:
        if is_catthew:
            kind = str(entry.get("kind") or "task")
            if kind != "event" and catthew_tasks.exists():
                text = catthew_tasks.read_text(encoding="utf-8")
                updated = _check_off_line(text, title, entry.get("line"))
                if updated != text:
                    catthew_tasks.write_text(updated, encoding="utf-8")
                    entry["source_updated"] = True
        elif file_path.as_posix() not in ("", ".") and _safe_vault_task(file_path) and file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
            status = (_get_fm(existing, "status") or "").lower()
            if status in _STALE:
                await query.answer(text=f"Already {status} — no change made.")
                return
            text = _set_fm(existing, "status", "completed")
            text = _set_fm(text, "completed_date", date.today().isoformat())
            text = text.replace("- [ ] ", "- [x] ", 1)
            file_path.write_text(text, encoding="utf-8")
            entry["source_updated"] = True
        entry["status"] = "done"
        entry["done_at"] = datetime.now(timezone.utc).isoformat()
        entry["done_by"] = getattr(query.from_user, "first_name", "User")
        reg[digest] = entry
        _save_json(registry_path, reg)
        await query.answer(text="✅ Done")
        try:
            await query.edit_message_text(text=f"✅ {title}", reply_markup=None)
        except Exception:
            pass
    except Exception as exc:
        logger.error("[%s] task-card done failed: %s", adapter.name, exc)
        await query.answer(text="Could not mark done.")


async def handle_wellness(adapter, query, data: str, cb: Dict[str, Any]) -> None:
    if not await adapter._callback_authorized(query, cb, "⛔ You are not authorized to log this."):
        return
    parts = data.split(":")
    if len(parts) < 3:
        await query.answer(text="Invalid wellness data.")
        return
    prefix, kind, amount = parts[0], parts[1], parts[2]
    if kind not in _WELLNESS_SCRIPTS:
        await query.answer(text=f"Unknown log: {kind}")
        return
    original = getattr(query.message, "text", None) or f"{kind} {amount}"
    if prefix == "wlm":
        await query.answer()
        try:
            await query.edit_message_text(text=original, reply_markup=_wellness_keyboard(kind, amount, more=True))
        except Exception:
            try:
                await query.edit_message_reply_markup(reply_markup=_wellness_keyboard(kind, amount, more=True))
            except Exception as exc:
                logger.error("[%s] wellness more failed: %s", adapter.name, exc)
        return
    if prefix == "wlb":
        await query.answer()
        try:
            await query.edit_message_reply_markup(reply_markup=_wellness_keyboard(kind, amount, more=False))
        except Exception as exc:
            logger.error("[%s] wellness back failed: %s", adapter.name, exc)
        return

    from hermes_constants import get_hermes_home
    home = get_hermes_home()
    script_name, _ok = _WELLNESS_SCRIPTS[kind]
    script = home / "scripts" / script_name
    if not script.exists():
        await query.answer(text="❌ Logger missing")
        logger.error("[%s] wellness script missing: %s", adapter.name, script)
        return
    env = os.environ.copy()
    env["HERMES_HOME"] = str(home)
    try:
        proc = await asyncio.create_subprocess_exec(
            str(script), amount,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env)
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            err = (stderr or stdout or b"log failed").decode("utf-8", "replace").strip().splitlines()
            msg = err[-1] if err else "log failed"
            await query.answer(text=f"❌ {msg[:180]}")
            logger.error("[%s] wellness log failed kind=%s rc=%s stderr=%s", adapter.name, kind, proc.returncode, stderr)
            return
        summary = (stdout.decode("utf-8", "replace").strip().splitlines() or ["✅ Logged"])[0]
        await query.answer(text=summary[:180])
        try:
            await query.edit_message_text(text=summary, reply_markup=None)
        except Exception:
            pass
        logger.info("[%s] wellness logged kind=%s amount=%s user=%s", adapter.name, kind, amount, getattr(query.from_user, "id", ""))
    except Exception as exc:
        logger.error("[%s] wellness log exception: %s", adapter.name, exc)
        await query.answer(text="❌ Could not log.")
