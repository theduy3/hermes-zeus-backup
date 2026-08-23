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
Life OS detailed source of truth: /home/hermes/.hermes/projects/life-os/life-knowledge-base. Before personal-context answers or substantial writes, read agent_rules.md and search this KB; memory is routing only, never the database.
§
§
Finance (Aug 22, 2026): NVDA ~36% of book — cap/diversify, DO NOT ADD. No new AI/semi/correlated exposure: MSFT,AMZN,GOOG,META,NVDA,AVGO,TSLA,ASML,AMD,INTC,NBIS. Charles = triage/watchlist layer ONLY; book of record = Finance profile (no advice here). FX ~1.39 CAD/USD. Income $2,747.50 biweekly net (Ongles Rivieres→CIBC, Thursdays). CAD ~2.7k liquid RESERVED vs cards/tax/loan; free liquidity unreconciled. TD Chequing >=$2,000 by Aug 24 (mortgage). FHSA room = watch item.