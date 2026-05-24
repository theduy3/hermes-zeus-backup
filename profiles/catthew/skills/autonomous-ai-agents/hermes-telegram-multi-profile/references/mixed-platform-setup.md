# Mixed-platform multi-profile setup (Telegram + Discord)

Pattern used to create 8 profiles (4 new Telegram, 4 existing migrated to Discord) in one session.

## Phase 1: Create profiles

```bash
for p in zeus alan mira turing; do hermes profile create "$p" --clone; done
```

`--clone` inherits config, .env, SOUL.md, and skills from default. Each gets isolated memory/sessions.

## Phase 2: Write SOUL.md for each specialist

| Profile | Role | Key traits |
|---------|------|------------|
| zeus | Personal assistant | Warm, terse, practical; not orchestrator/researcher/writer/debugger |
| alan | Research specialist | Evidence-first, skeptical, source-annotated, confidence-scored |
| mira | Writer | Audience-aware, clear, structured; outline→draft→polish |
| turing | Debugger/engineer | Direct, commands-first, reproduce-before-fix, one-change-at-a-time |
| default | Orchestrator | Plans, decomposes, delegates, synthesizes; knows the team |

## Phase 3: Configure .env for each profile

Use Python to safely patch tokens — never round-trip .env through grep/sed that could truncate or redact values.

### Telegram profiles

```python
for name, token in {"zeus": "TOKEN", "alan": "TOKEN", "mira": "TOKEN", "turing": "TOKEN"}.items():
    # Set TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS
    # Clear any DISCORD_BOT_TOKEN / DISCORD_ALLOWED_USERS
```

### Discord profiles (migrating from Telegram)

```python
for name, token in {"maily": "TOKEN", "charlesbourg": "TOKEN", "3r": "TOKEN", "ss": "TOKEN"}.items():
    # Comment out TELEGRAM_BOT_TOKEN / TELEGRAM_ALLOWED_USERS
    # Set DISCORD_BOT_TOKEN, DISCORD_ALLOWED_USERS
```

## Phase 4: Set model for all profiles

```python
for name in profiles:
    config["model"]["default"] = "deepseek-v4-pro"
    config["provider"]["default"] = "deepseek"
```

## Phase 5: Install and verify gateways

```bash
# Install all
for p in zeus alan mira turing maily charlesbourg 3r ss; do
  hermes -p "$p" gateway install --force
done

# Wait 10s then verify
for p in zeus alan mira turing; do
  grep "✓ telegram" ~/.hermes/profiles/$p/logs/gateway.log | tail -1
done

# Discord: validate tokens FIRST with REST API, then check logs
for p in maily charlesbourg 3r ss; do
  grep "$(date +%Y-%m-%d)" ~/.hermes/profiles/$p/logs/gateway.log | grep -E "✓ discord|✗ discord"
done
```

## Pitfalls

1. **`--clone` .env has placeholder tokens** — must explicitly set real tokens after cloning
2. **Discord timed out = bad token** — validate with curl, NOT Python urllib (urllib returns false HTTP 403/1010 for valid tokens)
3. **Old gateway logs mislead** — always filter by today's date
4. **Cross-platform token leakage** — when a Telegram profile becomes Discord, clear the old TELEGRAM_BOT_TOKEN
5. **Model must be set per profile** — the clone inherits the parent model, update explicitly
