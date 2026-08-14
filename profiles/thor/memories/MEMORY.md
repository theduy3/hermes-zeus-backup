Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
GitHub backup: repo theduy3/hermes-zeus-backup, cron 12e5ce30563d 15:00 UTC. Restore by cloning into ~/.hermes/ and restoring .env + auth.json (openai-codex OAuth).
§
Thor wellness Telegram bot profile: token starts 8788503747, profile name "thor", focused on physical health, mental health, and diet/nutrition. SOUL.md set up with evidence-based, warm-but-grounded tone.
§
Platform mapping: Telegram=default(orch), alan, mira, turing, zeus, thor, finance. Discord=3r(Ongles Rivieres), charlesbourg(Ongles Charlesbourg), maily(Ongles Maily), ss(Sans Souci). Entrypoint sets HERMES_HOME per profile.
§
User wants running daily totals (calories vs 1,950 target, protein vs 150g target, water vs 3,000ml target) included every time they log food/water.
§
Intermittent fasting: 11AM–6PM eating window (17:7), starting May 19, 2026. Water during fasting window is fine.
§
Weight tracking: CSV at ~/.hermes/profiles/thor/logs/weight-log.csv, graph script at scripts/weight_graph.py. User wants graph regenerated and shown every time they update weight. Historical records: May 11=77.0, May 15=75.4, May 19=75.6 kg.
§
Thor cron current Pacific schedule: water 7AM, 10AM, 1PM, 4PM, 7PM, 10PM; meditation 8:45AM + 10:15PM; protein 2PM; exercise 2:15PM; golf mobility 12:45PM; stretch 8:45PM; weekly measurements Sat 9AM. Buttons reject old-day clicks.
§
For Thor hydration logs, when user says “glass” or “cup” of water, count it as 500ml unless they specify another amount.
§
Perplexity source to remember: https://www.perplexity.ai/search/22bd7ccb-66cf-4bf4-ba19-922cafc3d6d5. Content not fetched here (HTTP 403); ask user for text if needed.
§
§
Active travel context: destination unspecified destination; timezone America/Toronto (EDT); set 2026-08-06. Apply trip-sensitive schedules, briefings, reminders, dates, and local-time wording across all profiles until Duy changes it.
§
Life OS detailed source of truth: /home/hermes/.hermes/projects/life-os/life-knowledge-base. Before personal-context answers or substantial writes, read agent_rules.md and search this KB; memory is routing only, never the database.
