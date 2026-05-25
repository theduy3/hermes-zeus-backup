Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d at 15:00 UTC (8AM PDT). .gitignore: .env, auth.json, logs/, sessions/, cron/output/, cache/, hermes-agent/, venv/, node_modules/. Recovery: clone into ~/.hermes/ + restore .env with DEEPSEEK_API_KEY.
§
Thor wellness Telegram bot profile: token starts 8788503747, profile name "thor", focused on physical health, mental health, and diet/nutrition. SOUL.md set up with evidence-based, warm-but-grounded tone.
§
All Hermes profiles use deepseek-v4-pro via deepseek provider (api.deepseek.com, NOT openrouter). Config: model.provider=deepseek, model.base_url=https://api.deepseek.com, providers.deepseek={api_base:https://api.deepseek.com, env_key:DEEPSEEK_API_KEY}. When cloning profiles, model config may inherit openrouter settings — must fix to deepseek after clone.
§
Platform mapping: Telegram=default(orch), alan, mira, turing, zeus, thor, finance. Discord=3r(Ongles Rivieres), charlesbourg(Ongles Charlesbourg), maily(Ongles Maily), ss(Sans Souci). Entrypoint sets HERMES_HOME per profile.
§
User wants running daily totals (calories vs 1,950 target, protein vs 150g target, water vs 3,000ml target) included every time they log food/water.
§
Intermittent fasting: 11AM–6PM eating window (17:7), starting May 19, 2026. Water during fasting window is fine.
§
Weight tracking: CSV at ~/.hermes/profiles/thor/logs/weight-log.csv, graph script at scripts/weight_graph.py. User wants graph regenerated and shown every time they update weight. Historical records: May 11=77.0, May 15=75.4, May 19=75.6 kg.
§
Thor cron scheduling: user expects reminder labels/times to match the visible Pacific clock time on their phone (PDT/PST as applicable). When user is in Quebec, switch wellness reminders to Eastern time if requested.
§
For Thor hydration logs, when user says “glass” or “cup” of water, count it as 500ml unless they specify another amount.