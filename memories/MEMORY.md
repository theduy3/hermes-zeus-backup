Vault /vault/ writable (ext4 rw, hermes:hermes). ALL profiles: default write target is /vault/Inbox/ — dump notes, tasks, summaries there for Obsidian ingest. Not /home/hermes/.
§
On this macOS environment, remindctl is not installed. Apple Reminders can be managed via osascript/AppleScript as a fallback.
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d at 15:00 UTC (8AM PDT). .gitignore: .env, auth.json, logs/, sessions/, cron/output/, cache/, hermes-agent/, venv/, node_modules/. Recovery: clone into ~/.hermes/ + restore .env with DEEPSEEK_API_KEY.
§
Zeus daily briefing jobs: e6711b998b07 info-only, b83af24484d0 tasks-only. Confirmed Montreal/Quebec trip June 8-15, 2026: use Eastern Time for trip-sensitive scheduling/briefings during Montreal window June 9 through return day June 15; switch back to Pacific after return to Vancouver on June 15.
§
Thor wellness Telegram bot profile: token starts 8788503747, profile name "thor", focused on physical health, mental health, and diet/nutrition. SOUL.md set up with evidence-based, warm-but-grounded tone.
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
SalonX Engineer (`salonx-engineer` / Engineer-SalonX) specifically uses `gpt-5.5` via OpenAI Codex for coding
§
Profiles: Telegram=default/alan/mira/turing/zeus/thor/finance/catthew/charles/butter; Discord=3r/charlesbourg/maily/ss. Butter=points/churning.
§
Hermes Docker venv: /home/hermes/.hermes/hermes-agent/venv/ may lack pip. Bootstrap: python3 -m ensurepip --upgrade then python3 -m pip install <pkg>. Use python3 -m pip, not bin/pip.
§
Tesseract OCR 5.5.0 portable at ~/.local/. Deps: libleptonica6/libgif7/libarchive13/libtesseract5. eng.traineddata at ~/.local/share/tessdata/. Env: TESSDATA_PREFIX, LD_LIBRARY_PATH. Pipeline: pymupdf→PNG→tesseract. pymupdf 1.27 in hermes-agent venv.
§
Paperclip on VPS 147.93.116.94 runs in Docker, bound localhost:3100 in container. Host SSH user is root (host lacked hermes); use root SSH tunnel.