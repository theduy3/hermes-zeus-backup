#!/usr/bin/env python3
"""Read the annotation/stroke layer of planner grid pages via remarkable MCP."""
import base64, json, subprocess, sys, time

LAUNCHER = "/home/hermes/.hermes/scripts/run-remarkable-mcp.sh"

def call(doc, page, timeout=180.0):
    proc = subprocess.Popen(["bash", LAUNCHER], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    def send(o):
        proc.stdin.write(json.dumps(o) + "\n"); proc.stdin.flush()
    send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}})
    send({"jsonrpc":"2.0","method":"notifications/initialized"})
    send({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"remarkable_read","arguments":{"document":doc,"content_type":"annotations","include_ocr":True,"page":page}}})
    deadline = time.time()+timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line: break
        line=line.strip()
        if not line or "jsonrpc" not in line: continue
        try: msg=json.loads(line)
        except: continue
        if msg.get("id")==2:
            proc.stdin.close(); proc.terminate()
            return msg.get("result")
    proc.stdin.close(); proc.terminate()
    return None

for pg in (963, 964):
    print(f"\n========== p{pg} annotation/ocr read ==========")
    r = call("2026 Planner", pg)
    if not r:
        print("NO RESULT"); continue
    txt = ""
    for item in r.get("content", []):
        if item.get("type")=="text":
            txt += item.get("text","")
    # Show a trimmed window around any mark-like content
    print(txt[:1500])
