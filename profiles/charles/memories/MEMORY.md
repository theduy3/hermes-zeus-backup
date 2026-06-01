Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d at 15:00 UTC (8AM PDT). .gitignore: .env, auth.json, logs/, sessions/, cron/output/, cache/, hermes-agent/, venv/, node_modules/. Recovery: clone into ~/.hermes/ + restore .env + auth.json (openai-codex OAuth).
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
All Hermes profiles use the openai-codex provider (OAuth via ~/.hermes/auth.json), model gpt-5.5 - NOT deepseek or openrouter. Config: model.provider=openai-codex, model.default=gpt-5.5, providers:{} (no base_url). DeepSeek fully removed 2026-05-24. When cloning a profile, verify model.provider=openai-codex (may inherit stale settings).
§
Platform mapping: Telegram=default(orch), alan, mira, turing, zeus, thor, finance. Discord=3r(Ongles Rivieres), charlesbourg(Ongles Charlesbourg), maily(Ongles Maily), ss(Sans Souci). Entrypoint sets HERMES_HOME per profile.
§
Finance profile (Telegram) = user's Personal Finance bot — knows detailed financials, account balances, holdings. Charles should coordinate with it for portfolio strategy, retirement planning, and any advice that needs precise numbers.
§
User registered portfolio/admin snapshot as of 2026-05-30 PT: registered portfolio ~$200.14k CAD; cash ~$92.68k (46.3%); NVDA ~$73.55k (36.8%). Key planning risks: high cash drag, high NVDA/single-stock + AI mega-cap concentration (NVDA/GOOG/META/PLTR/FIG), USD/CAD FX exposure. FHSA deployment pending: ~$11.46k cash + 33 VFV.TO. Near-term admin/cash-flow risk: June credit-card payment cadence plus overdue tax/debt/insurance/admin tasks; Montreal trip Jun 8–15 may reduce admin bandwidth. Income: $2,748 biweekly Thursdays starting 2026-05-28; rent $2,000/month.