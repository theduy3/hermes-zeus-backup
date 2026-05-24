Vault in Docker: ro at /vault/. Cron workers need bind mounts in docker-compose.yml. Cron jobs toolsets ["web","memory","skills","terminal","file"].
§
All Hermes profiles use deepseek-v4-pro via deepseek provider (api.deepseek.com, NOT openrouter). Config: model.provider=deepseek, model.base_url=https://api.deepseek.com, providers.deepseek={api_base:https://api.deepseek.com, env_key:DEEPSEEK_API_KEY}. When cloning profiles, model config may inherit openrouter settings — must fix to deepseek after clone.
§
Platform mapping: Telegram=default(orch), alan, mira, turing, zeus, thor, finance. Discord=3r(Ongles Rivieres), charlesbourg(Ongles Charlesbourg), maily(Ongles Maily), ss(Sans Souci). Entrypoint sets HERMES_HOME per profile.
