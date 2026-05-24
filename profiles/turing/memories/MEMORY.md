Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d at 15:00 UTC (8AM PDT). .gitignore: .env, auth.json, logs/, sessions/, cron/output/, cache/, hermes-agent/, venv/, node_modules/. Recovery: clone into ~/.hermes/ + restore .env with DEEPSEEK_API_KEY.
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
All Hermes profiles use deepseek-v4-pro via deepseek provider (api.deepseek.com, NOT openrouter). Config: model.provider=deepseek, model.base_url=https://api.deepseek.com, providers.deepseek={api_base:https://api.deepseek.com, env_key:DEEPSEEK_API_KEY}. When cloning profiles, model config may inherit openrouter settings — must fix to deepseek after clone.
§
Platform mapping: Telegram=default(orch), alan, mira, turing, zeus, thor, finance. Discord=3r(Ongles Rivieres), charlesbourg(Ongles Charlesbourg), maily(Ongles Maily), ss(Sans Souci). Entrypoint sets HERMES_HOME per profile.
§
Hermes Docker venv: /home/hermes/.hermes/hermes-agent/venv/ may lack pip. Bootstrap: python3 -m ensurepip --upgrade then python3 -m pip install <pkg>. Use python3 -m pip, not bin/pip.
§
Tesseract OCR 5.5.0 portable at ~/.local/. Deps: libleptonica6/libgif7/libarchive13/libtesseract5. eng.traineddata at ~/.local/share/tessdata/. Env: TESSDATA_PREFIX, LD_LIBRARY_PATH. Pipeline: pymupdf→PNG→tesseract. pymupdf 1.27 in hermes-agent venv.
