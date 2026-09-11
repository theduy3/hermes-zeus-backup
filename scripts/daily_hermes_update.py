#!/usr/bin/env python3
"""Daily Hermes update at 1:20am Vancouver.

Silent when already current and buttons are intact.
Telegram stdout only when an update ran, buttons had to be restored, or something failed.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path(os.environ.get("HERMES_HOME", "/home/hermes/.hermes"))
if HOME.name in {"zeus", "catthew", "thor", "wiki", "charles", "finance", "butter"}:
    HOME = HOME.parent.parent
HERMES = Path("/home/hermes/.local/bin/hermes")
AGENT = HOME / "hermes-agent"
ADAPTER = AGENT / "plugins" / "platforms" / "telegram" / "adapter.py"
HANDLERS = AGENT / "plugins" / "platforms" / "telegram" / "profile_buttons.py"
HANDLER_BACKUP = HOME / "scripts" / "_telegram_profile_buttons.py"
DISPATCH = '''        if data.startswith(("zt:", "ztm:", "delay:", "del:", "dl:", "ct:", "ctm:")):
            from plugins.platforms.telegram.profile_buttons import handle_task_card
            await handle_task_card(self, query, data, cb)
            return
        if data.startswith(("wl:", "wlm:", "wlb:")):
            from plugins.platforms.telegram.profile_buttons import handle_wellness
            await handle_wellness(self, query, data, cb)
            return
'''
ANCHOR = """            if data.startswith(prefix):
                await handler(query, data, cb)
                return
"""


def run(args: list[str], timeout: int = 900) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HERMES_HOME"] = str(HOME)
    return subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", env=env, timeout=timeout,
    )


def strip_noise(text: str) -> str:
    keep = []
    for line in (text or "").splitlines():
        if "mixed sys.modules" in line or "hermes update" in line and "did not restart" in line:
            continue
        if line.startswith("  Gateways may still") or line.startswith("  Run `hermes update`"):
            continue
        keep.append(line)
    return "\n".join(keep).strip()


def update_available(check_out: str) -> bool:
    low = check_out.lower()
    return "update available" in low or "commits behind" in low


def buttons_ok() -> bool:
    if not ADAPTER.exists() or not HANDLERS.exists():
        return False
    src = ADAPTER.read_text(encoding="utf-8")
    body = HANDLERS.read_text(encoding="utf-8")
    return "handle_task_card" in src and "handle_wellness" in src and "async def handle_task_card" in body


def restore_buttons() -> list[str]:
    did = []
    if HANDLER_BACKUP.exists():
        HANDLERS.parent.mkdir(parents=True, exist_ok=True)
        if not HANDLERS.exists() or HANDLERS.read_text(encoding="utf-8") != HANDLER_BACKUP.read_text(encoding="utf-8"):
            shutil.copy2(HANDLER_BACKUP, HANDLERS)
            did.append("restored profile_buttons.py")
    if ADAPTER.exists():
        src = ADAPTER.read_text(encoding="utf-8")
        if "handle_task_card" not in src:
            idx = src.find(ANCHOR)
            if idx == -1:
                did.append("could not reinsert button dispatch (anchor missing)")
            else:
                insert_at = idx + len(ANCHOR)
                src = src[:insert_at] + DISPATCH + src[insert_at:]
                ADAPTER.write_text(src, encoding="utf-8")
                did.append("reinserted Telegram button dispatch")
    return did


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore-only", action="store_true")
    args = parser.parse_args()
    notes: list[str] = []
    failed = False

    if not args.restore_only:
        try:
            check = run([str(HERMES), "update", "--check"], timeout=180)
        except subprocess.TimeoutExpired:
            print("Hermes update check timed out.")
            return 0
        check_out = strip_noise(check.stdout or "")
        if not update_available(check_out):
            restored = restore_buttons()
            if restored:
                print("Hermes already current. Button handlers needed a repair:\n- " + "\n- ".join(restored))
            return 0
        try:
            upd = run([str(HERMES), "update", "--yes"], timeout=1200)
        except subprocess.TimeoutExpired:
            restore_buttons()
            print("Hermes update timed out after 20 minutes. Button handlers were re-checked.")
            return 0
        out = strip_noise(upd.stdout or "")
        if upd.returncode != 0:
            failed = True
            notes.append("update command failed")
        else:
            notes.append("Hermes updated")
        if out:
            tail = "\n".join(out.splitlines()[-12:])
            notes.append(tail)

    restored = restore_buttons()
    notes.extend(restored)
    if not buttons_ok():
        failed = True
        notes.append("Done/More button handlers still missing after restore")

    if args.restore_only and not notes:
        return 0

    status = "FAIL" if failed else "OK"
    print(f"Daily Hermes update: {status}")
    for item in notes:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
