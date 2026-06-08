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
User weekly finance context as of 2026-06-07 PT: registered portfolio cash ~$92.7k (~46.6%); NVDA ~$71.7k (~36.0% total portfolio / ~67.0% invested holdings). Key risks: high cash drag, NVDA/single-stock + tech/AI factor concentration, USD/CAD FX exposure. Near-term admin risk is payments rather than investing: multiple credit card payment tasks Jun 8–27; pending card closures, portfolio update, Laviestella taxes/strata PAD, Ongles Rivieres year-end tax package, Jun 25 SS rent PAD, Jun 11 RBC Avion→BA Avios 30% bonus deadline. Cash constraints: payroll $2,748 biweekly; rent $2,000/month. No confirmed near-term registered withdrawal need or trades recorded.