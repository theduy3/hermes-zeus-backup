#!/bin/bash
# Hermes secrets.command helper — decrypts the Telegram bot token at gateway
# startup and prints it as a KEY=VALUE line on stdout. Hermes parses stdout
# for TELEGRAM_BOT_TOKEN and sets it on os.environ. Must be fast + non-
# interactive (Hermes enforces a 3s hard timeout, discards stderr).
set -euo pipefail
BASE="/home/hermes/.hermes/secrets"
HERMES_AGENT_VENV_PY="/home/hermes/.hermes/hermes-agent/venv/bin/python3"
"$HERMES_AGENT_VENV_PY" - <<'PY'
from cryptography.fernet import Fernet
import os
base="/home/hermes/.hermes/secrets"
key=open(os.path.join(base,"fernet.key"),"rb").read()
ct=open(os.path.join(base,"telegram.enc"),"rb").read()
tok=Fernet(key).decrypt(ct).decode()
print(f"TELEGRAM_BOT_TOKEN={tok}")
PY
