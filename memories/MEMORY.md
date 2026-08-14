Vault /vault writable. /vault/Inbox is an ingest queue processed by daily cron; use it only for notes meant to be filed/consumed. Keep durable operational artifacts outside Inbox (e.g. ~/.graphify, skills, or Tasks).
§
Thor wellness Telegram bot profile: token starts 8788503747, profile name "thor", focused on physical health, mental health, and diet/nutrition. SOUL.md set up with evidence-based, warm-but-grounded tone.
§
theduylifeos: /Users/theduy/theduylifeos/ — Legal, Finance, Business OptCo (CHARLESBOURG/MAILY/RIVIERES/SS), Business HoldCo, Business Projects, Personal, FAMILY TRUST, Education, Job, Archive, Projects. Sort loose files here.
§
Profiles: Telegram=default/zeus/thor/finance/catthew/charles/butter. Docker profile gateways hardened via venv/bin/hermes wrapper; supervisor ~/.hermes/scripts/profile_gateway_supervisor.sh; watchdog cron 96f28d228fb9.
§
Hermes Docker venv: /home/hermes/.hermes/hermes-agent/venv/ may lack pip. Bootstrap: python3 -m ensurepip --upgrade then python3 -m pip install <pkg>. Use python3 -m pip, not bin/pip.
§
§
§
cronjob tool = DEFAULT profile only; other profiles' jobs are at ~/.hermes/profiles/<p>/cron/jobs.json (edit directly or `hermes cron --profile <p>`). Provider-less cron jobs inherit the profile default provider (openai-codex), so null provider does NOT avoid a Codex-credential block — pin provider explicitly.
§
Life OS detailed source of truth: /home/hermes/.hermes/projects/life-os/life-knowledge-base. Agents must read agent_rules.md/search it before personal-context answers or substantial writes; persistent memory is routing only. Raw cross-device/newsletter captures stay in /vault/Inbox→theduyvault archive; Life OS receives only curated current, source-linked context.
§
config.yaml and .env are write-PROTECTED from patch/write_file tools (security guards reject them). For config.yaml use `hermes config set <key> <value>` (nested keys work, e.g. secrets.command.enabled). For .env edits use terminal python. For security-sensitive credential/env changes (token moves, encryption setup) wait for explicit approval — do NOT proceed on clarify-timeout best-judgment; user stopped an in-flight credential move once.