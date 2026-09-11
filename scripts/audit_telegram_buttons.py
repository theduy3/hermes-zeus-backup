#!/usr/bin/env python3
"""Audit Hermes profile Telegram buttons. Empty stdout is silent; this always prints."""
from __future__ import annotations

import ast
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

HOME = Path(os.environ.get("HERMES_HOME", "/home/hermes/.hermes"))
if HOME.name in {"zeus", "catthew", "thor", "wiki", "charles", "finance", "butter"}:
    HOME = HOME.parent.parent
PROFILES = HOME / "profiles"
ADAPTER = HOME / "hermes-agent" / "plugins" / "platforms" / "telegram" / "adapter.py"
HANDLERS = HOME / "hermes-agent" / "plugins" / "platforms" / "telegram" / "profile_buttons.py"
KNOWN = ("zt", "ztm", "delay", "del", "dl", "ct", "ctm", "wl", "wlm", "wlb")
STOCK = ("mp", "mpg", "mpv", "mm", "mc", "mb", "mx", "mg", "cp", "gt", "ea", "sc", "cl", "update_prompt")
CB_RE = re.compile(
    r"""callback_data["']?\s*[:=]\s*(?:f)?(?:"""
    r"""["']([^"']+)["']"""
    r""")""",
    re.I,
)


def prefix_of(raw: str) -> str:
    text = raw.strip()
    if text.startswith("f"):
        text = text[1:]
    text = text.strip("\"'")
    head = text.split(":", 1)[0].strip()
    return head


def scan_scripts() -> dict[str, set[str]]:
    found: dict[str, set[str]] = defaultdict(set)
    roots = [PROFILES, HOME / "scripts"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".py", ".sh"} or path.name.startswith("_"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "callback_data" not in text:
                continue
            profile = "home"
            try:
                rel = path.relative_to(PROFILES)
                profile = rel.parts[0]
            except ValueError:
                pass
            for match in CB_RE.finditer(text):
                pref = prefix_of(match.group(1))
                if pref and pref not in STOCK and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", pref):
                    found[profile].add(pref)
    return found


def adapter_text() -> str:
    try:
        return ADAPTER.read_text(encoding="utf-8")
    except OSError:
        return ""


def routed_prefixes(src: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r'["\']([A-Za-z][A-Za-z0-9_-]*):["\']', src):
        found.add(match.group(1))
    return found


def gateway_homes() -> dict[str, list[tuple[int, float]]]:
    """profile-or-default -> [(pid, start_epoch), ...]"""
    out: dict[str, list[tuple[int, float]]] = defaultdict(list)
    proc = Path("/proc")
    if not proc.exists():
        return out
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cmd = (entry / "cmdline").read_bytes().replace(b"\x00", b" ").decode("utf-8", "replace")
        except OSError:
            continue
        if "hermes" not in cmd or "gateway run" not in cmd:
            continue
        try:
            env = (entry / "environ").read_bytes().split(b"\x00")
        except OSError:
            continue
        home = ""
        for item in env:
            if item.startswith(b"HERMES_HOME="):
                home = item.decode("utf-8", "replace").split("=", 1)[1]
                break
        label = "default"
        if "/profiles/" in home:
            label = Path(home).name
        try:
            start = entry.stat().st_ctime
        except OSError:
            start = 0.0
        out[label].append((int(entry.name), start))
    return out


def main() -> int:
    fails: list[str] = []
    warns: list[str] = []
    lines: list[str] = []
    senders = scan_scripts()
    src = adapter_text()
    routed = routed_prefixes(src) if src else set()
    needed = set(KNOWN)
    for prefs in senders.values():
        needed |= prefs

    if not ADAPTER.exists():
        fails.append("telegram adapter.py missing")
    if not HANDLERS.exists():
        fails.append("profile_buttons.py missing (hermes update likely wiped handlers)")
    else:
        try:
            ast.parse(HANDLERS.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            fails.append(f"profile_buttons.py syntax error: {exc}")
        body = HANDLERS.read_text(encoding="utf-8")
        if "async def handle_task_card" not in body:
            fails.append("handle_task_card missing")
        if "async def handle_wellness" not in body:
            fails.append("handle_wellness missing")

    if src:
        if "handle_task_card" not in src or "handle_wellness" not in src:
            fails.append("adapter.py no longer dispatches profile button handlers")
        missing = sorted(p for p in needed if p not in routed and p not in STOCK)
        if missing:
            fails.append("unrouted prefixes: " + ", ".join(f"{p}:" for p in missing))
    else:
        fails.append("could not read adapter.py")

    gates = gateway_homes()
    button_profiles = sorted({p for p in senders if p != "home"} | {"zeus", "catthew", "thor"})
    for profile in button_profiles:
        if profile not in gates:
            fails.append(f"{profile} gateway not running")

    adapter_mtime = ADAPTER.stat().st_mtime if ADAPTER.exists() else 0
    handler_mtime = HANDLERS.stat().st_mtime if HANDLERS.exists() else 0
    newest = max(adapter_mtime, handler_mtime)
    for profile, procs in sorted(gates.items()):
        if profile not in button_profiles and profile != "default":
            continue
        oldest = min(start for _, start in procs)
        if newest and oldest and newest > oldest + 5:
            warns.append(f"{profile} gateway older than handler files — restart to load buttons")

    # Import smoke without touching live registries.
    if HANDLERS.exists() and "handle_task_card" in HANDLERS.read_text(encoding="utf-8"):
        agent_root = str(HOME / "hermes-agent")
        if agent_root not in sys.path:
            sys.path.insert(0, agent_root)
        try:
            from plugins.platforms.telegram.profile_buttons import handle_task_card, handle_wellness  # noqa: F401
        except Exception as exc:
            fails.append(f"handler import failed: {exc}")

    status = "FAIL" if fails else "PASS"
    lines.append(f"Telegram button audit: {status}")
    lines.append("Sunday check of Zeus/Catthew/Thor task and wellness buttons.")
    if senders:
        lines.append("")
        lines.append("Senders:")
        for profile in sorted(senders):
            prefs = ", ".join(f"{p}:" for p in sorted(senders[profile]))
            alive = "up" if (profile in gates or (profile == "home" and "default" in gates)) else "DOWN"
            lines.append(f"  {profile} [{alive}] {prefs}")
    if fails:
        lines.append("")
        lines.append("Failures:")
        lines.extend(f"  - {item}" for item in fails)
    if warns:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"  - {item}" for item in warns)
    if not fails and not warns:
        lines.append("")
        lines.append("All discovered button prefixes are routed and the three button profiles are connected.")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
