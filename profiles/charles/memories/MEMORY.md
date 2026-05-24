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
Finance profile (Telegram) = user's Personal Finance bot — knows detailed financials, account balances, holdings. Charles should coordinate with it for portfolio strategy, retirement planning, and any advice that needs precise numbers.
§
User portfolio snapshots (2026-05-19): registered accts ~$200.14k CAD incl WS RRSP ~$156.35k (cash $60.71k CAD equiv; holdings USD FIG10, GOOG8, META9, NVDA241, PLTR3, RACE21; NVDA ~47% of WS RRSP incl cash), Questrade RSP cash $20k, Questrade FHSA $17.38k (cash $11.46k, VFV.TO33), Questrade Spousal RRSP $6.41k (cash $512; FIG17, GOOG7, META2). Total registered cash ~$92.68k CAD (~46.3%). NVDA ~$73.55k CAD (~36.8% of registered).