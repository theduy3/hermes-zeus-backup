#!/usr/bin/env bash
# Hermes stdio launcher for SamMorrowDrums/remarkable-mcp (cloud via ~/.rmapi).
# Read-only by default so Telegram Q&A cannot delete/move library items.
#
# FIX: the underlying package prints a PyMuPDF/fitz deprecation warning to
# STDOUT. MCP stdio uses stdout for JSON-RPC, so that stray line corrupts the
# protocol and Hermes marks the server "degraded"/"parked". We filter the
# warning from stdout while preserving the server's real stderr logs.
set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
uvx --from git+https://github.com/SamMorrowDrums/remarkable-mcp \
  remarkable-mcp --read-only "$@" \
  2> >(cat >&2) \
  | grep --line-buffered -vE "warning: The \`fitz\` API is deprecated"
