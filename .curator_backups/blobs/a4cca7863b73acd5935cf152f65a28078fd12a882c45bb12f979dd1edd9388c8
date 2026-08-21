# Verifying the reMarkable MCP stdio channel

Goal: confirm the launcher emits clean JSON-RPC on stdout (no stray
`warning:` lines) and that the server reports its tools.

## 1. The launcher must filter the fitz warning
The package prints this to STDOUT on every launch via uvx:
```
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
```
That line is NOT JSON, so Hermes's MCP client throws
`Failed to parse JSONRPC message from server` and parks the server.
The reference launcher `scripts/run-remarkable-mcp.sh` pipes stdout through
`grep -vE "warning: The \`fitz\` API is deprecated"`.

Quick check that stdout is clean (server exits on EOF from /dev/null, so this
only proves no startup-time noise — use step 2 for the full handshake):
```bash
export PATH="$HOME/.local/bin:$PATH"
timeout 30 bash /home/hermes/.hermes/scripts/run-remarkable-mcp.sh </dev/null 2>/dev/null | cat -A | head -3
# expect: no line beginning with "warning:"
```

## 2. Full handshake probe (feed from a FILE, not an inline heredoc)
NOTE: this agent's command parser blocks inline heredocs and `while-read`
loops. Write the handshake to a file first, then redirect it in.

Create `/tmp/rm_handshake.jsonl`:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

Run and classify:
```bash
export PATH="$HOME/.local/bin:$PATH"
timeout 35 bash /home/hermes/.hermes/scripts/run-remarkable-mcp.sh < /tmp/rm_handshake.jsonl > /tmp/rm_out.txt 2> /tmp/rm_err.txt
echo "exit=$?  out_bytes=$(wc -c </tmp/rm_out.txt)"
grep -c '^warning:' /tmp/rm_out.txt   # expect 0
grep -c jsonrpc       /tmp/rm_out.txt   # expect 2 (initialize result + tools/list)
```
A healthy result: `stray_warnings=0`, `json_lines=2`, and the `tools/list`
response lists 8 tools (`remarkable_browse`, `remarkable_search`,
`remarkable_read`, `remarkable_recent`, `remarkable_status`,
`remarkable_image`, `remarkable_export`, `remarkable_canvas`).

## 3. Token validity (no secret printing)
The `tools/list` (or `remarkable_status`) succeeding proves the `~/.rmapi`
cloud token is live. If it fails with an auth error, register once:
`remarkable-mcp --register <ONE_TIME_CODE>` from the reMarkable account,
which writes the token.
