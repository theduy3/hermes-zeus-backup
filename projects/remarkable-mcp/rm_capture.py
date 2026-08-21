#!/usr/bin/env python3
"""Capture a rendered PNG of a reMarkable page to disk via the remarkable MCP.

The MCP server is stdio; we drive it with a short JSON-RPC handshake and call
remarkable_image, which returns an embedded base64 PNG resource. We decode and
save it. This is the ground-truth stroke image for a planner page — kept
alongside the lossy OCR transcription so an agent can fall back to the
original rather than trusting handwriting interpretation.

Requires: ~/.rmapi token (registered) and `uvx` on PATH.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LAUNCHER = Path("/home/hermes/.hermes/scripts/run-remarkable-mcp.sh")


def _call(doc: str, page: int, timeout: float = 180.0) -> dict | None:
    """Run the MCP server, do initialize + remarkable_image, return the result dict."""
    cmd = ["bash", str(LAUNCHER)]
    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True,
        )
    except Exception as e:
        print(f"launch failed: {e}", file=sys.stderr)
        return None

    def send(obj):
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "rm-capture", "version": "1.0"}}})
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
          "params": {"name": "remarkable_image",
                     "arguments": {"document": doc, "page": page, "output_format": "png"}}})
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if not line or "jsonrpc" not in line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == 2:
            proc.stdin.close()
            proc.terminate()
            return msg.get("result")
    proc.stdin.close()
    proc.terminate()
    return None


def _b64_from_result(result: dict) -> str | None:
    """Pull the first base64 PNG blob out of an MCP tool result."""
    for item in result.get("content", []):
        if item.get("type") == "resource":
            blob = item.get("resource", {}).get("blob")
            if blob:
                return blob
        if item.get("type") == "text":
            try:
                inner = json.loads(item.get("text", ""))
                b = inner.get("resource", {}).get("blob")
                if b:
                    return b
            except Exception:
                pass
    return None


def capture_page(doc: str, page: int, out_path: Path) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    result = _call(doc, page)
    if not result:
        print("no result from remarkable_image", file=sys.stderr)
        return False
    blob = _b64_from_result(result)
    if not blob:
        print("no PNG blob in result", file=sys.stderr)
        return False
    data = base64.b64decode(blob)
    out_path.write_bytes(data)
    return True


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "2026 Planner"
    pg = int(sys.argv[2]) if len(sys.argv) > 2 else 551
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(f"/tmp/rm_p{pg}.png")
    ok = capture_page(d, pg, out)
    print("OK" if ok else "FAIL", out)
