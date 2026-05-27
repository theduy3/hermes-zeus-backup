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
User registered portfolio P/L snapshot (prices 2026-05-22 close; cash from 2026-05-19): total ~$199.07k CAD; cash ~$92.68k (46.6%); holdings MV ~$106.39k vs cost ~$63.70k, open P/L +$42.69k CAD (+67.0%). Accounts: WS RRSP ~$155.17k (holdings P/L +$40.78k), FHSA ~$17.50k (VFV.TO +$1.21k), Questrade Spousal RRSP ~$6.40k (holdings P/L +$0.69k), Questrade RSP cash $20k. Shares: FIG27, GOOG15, META11, NVDA241, PLTR3, RACE21, VFV.TO33. NVDA MV ~$71.69k CAD (~36.0% of registered).