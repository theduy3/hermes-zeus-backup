Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
Hermes backup: repo theduy3/hermes-zeus-backup; cron 12e5ce30563d daily 15:00 UTC. Excludes secrets/logs/sessions/cache/venv/node_modules. Recovery: clone to ~/.hermes/ and restore .env DEEPSEEK_API_KEY.
§
Zeus daily briefing (e6711b998b07) runs at 6:15AM Pacific local cron (currently 13:15 UTC during PDT) after Catthew's family briefing. Catthew posts to group chat, Zeus reads Catthew's output then delivers personal briefing via Telegram.
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
All Hermes profiles use deepseek-v4-pro via deepseek provider (api.deepseek.com, NOT openrouter). Config: model.provider=deepseek, model.base_url=https://api.deepseek.com, providers.deepseek={api_base:https://api.deepseek.com, env_key:DEEPSEEK_API_KEY}. When cloning profiles, model config may inherit openrouter settings — must fix to deepseek after clone.
§
Profiles: Telegram default(orch), zeus, alan, mira, turing, thor, finance, charles, catthew; Discord 3r/charlesbourg/maily/ss. Catthew/finance/Charles/Thor report to Zeus; finance+Charles trade knowledge weekly Sat 11PM Pacific.
§
Morning pipeline: Catthew briefs family group at 6:00AM Pacific; Zeus sends Daily Info at 6:15 and Tasks-only checkbox briefing at 6:17, reading Catthew output + Obsidian/tasks + finance/Charles reminders.
§
If Duy has an upcoming/current trip to Quebec/East Coast, Zeus should trigger Hermes Orchestrator (default profile) to switch timezone context from Pacific to Eastern for trip-sensitive scheduling/briefings, then switch back after return.
§
VN food sources: T&T Garden Burnaby (236)660-0515 groceries/prepared. Spot prawns: 604-802-5538 <$23/lb or boat Bayview Richmond 604-760-5376/778-961-2666 $25/lb. Clams/oysters: Costco Burnaby Still Creek $62/100 clams, oysters $55-75/100.