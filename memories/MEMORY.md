Vault /vault/ writable (ext4 rw, hermes:hermes). ALL profiles: default write target is /vault/Inbox/ — dump notes, tasks, summaries there for Obsidian ingest. Not /home/hermes/.
§
On this macOS environment, remindctl is not installed. Apple Reminders can be managed via osascript/AppleScript as a fallback.
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d at 15:00 UTC (8AM PDT). .gitignore: .env, auth.json, logs/, sessions/, cron/output/, cache/, hermes-agent/, venv/, node_modules/. Recovery: clone into ~/.hermes/ + restore .env + auth.json (openai-codex OAuth).
§
Thor wellness Telegram bot profile: token starts 8788503747, profile name "thor", focused on physical health, mental health, and diet/nutrition. SOUL.md set up with evidence-based, warm-but-grounded tone.
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
SalonX Engineer (`salonx-engineer` / Engineer-SalonX) specifically uses `gpt-5.5` via OpenAI Codex for coding
§
Profiles: Telegram=default/zeus/thor/finance/catthew/charles/butter. Docker profile gateways hardened via venv/bin/hermes wrapper; supervisor ~/.hermes/scripts/profile_gateway_supervisor.sh; watchdog cron 96f28d228fb9.
§
Hermes Docker venv: /home/hermes/.hermes/hermes-agent/venv/ may lack pip. Bootstrap: python3 -m ensurepip --upgrade then python3 -m pip install <pkg>. Use python3 -m pip, not bin/pip.
§
Tesseract OCR 5.5.0 portable at ~/.local/. Deps: libleptonica6/libgif7/libarchive13/libtesseract5. eng.traineddata at ~/.local/share/tessdata/. Env: TESSDATA_PREFIX, LD_LIBRARY_PATH. Pipeline: pymupdf→PNG→tesseract. pymupdf 1.27 in hermes-agent venv.
§
Paperclip on VPS 147.93.116.94 runs in Docker, bound localhost:3100 in container. Host SSH user is root (host lacked hermes); use root SSH tunnel.
§
§
§
§
Active travel context: destination unspecified destination; timezone America/Vancouver (PDT); set 2026-07-05. Apply trip-sensitive schedules, briefings, reminders, dates, and local-time wording across all profiles until Duy changes it.
