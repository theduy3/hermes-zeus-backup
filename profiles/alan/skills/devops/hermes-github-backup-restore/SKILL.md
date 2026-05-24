---
name: hermes-github-backup-restore
description: Restore Hermes Agent from a GitHub backup after VPS corruption or fresh deployment. Covers cloning the private backup repo, restoring secrets, and re-establishing the nightly sync cron job.
version: 1.0.0
---

# Hermes GitHub Backup & Restore

Disaster recovery for Hermes Agent: nightly backup to a private GitHub repo, and the restore procedure to get a fresh Hermes online in minutes.

## Backup Architecture

- **Cron job**: `nightly-hermes-github-backup` fires daily at 15:00 UTC (8 AM PDT / 7 AM PST)
- **Schedule**: `0 15 * * *` — macOS system timezone handles DST automatically, no VPS UTC offset logic needed
- **What's backed up**: `~/.hermes/` minus secrets — skills, memory, config templates, plugins, and any custom files
- **What's excluded** (.gitignore): `.env`, `auth.json`, `*.pem`, `*.key`, `logs/`, `sessions/`, `audio_cache/`, `cron/output/`, `hermes-agent/` (upstream source, can re-clone), `__pycache__/`, `venv/`, `.venv/`, `node_modules/`, `cache/`, `tmp/`
- **Repo**: private, token-scoped to `repo` (read+write) only

---

## Disaster Recovery: Restore Hermes from Backup

### Prerequisites

- A fresh VPS (or a clean Hermes install)
- The private repo URL: `https://github.com/theduy3/hermes-zeus-backup`
- A GitHub token scoped to `repo` (stored separately — not in the backup)

### Steps

#### 1. Install Hermes

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

This creates the `~/.hermes/` directory skeleton.

#### 2. Clone the backup over the skeleton

```bash
cd ~/.hermes
git init
git remote add origin https://<YOUR_GITHUB_TOKEN>@github.com/theduy3/hermes-zeus-backup.git
git fetch origin main
git reset --hard origin/main
```

This replaces the skeleton `~/.hermes/` with the backed-up skills, memory, and config.

#### 3. Restore secrets

Create `~/.hermes/.env` with the required API keys. This file is NEVER in the backup — you must have a secure copy elsewhere (password manager, encrypted USB, etc.).

Minimum required:
```
GITHUB_TOKEN=ghp_...    # For the nightly sync to push
OPENAI_API_KEY=sk-...   # Or whichever provider you use
```

#### 4. Re-establish the nightly sync cron job

Once Hermes is running, tell it:

> "Schedule a nightly sync to my GitHub backup repo. Push everything in ~/.hermes/ except secrets to https://github.com/theduy3/hermes-zeus-backup.git at midnight Central. GITHUB_TOKEN is in .env."

Or run the cron creation manually: `hermes cron create "0 5 * * *"` with the sync prompt.

#### 5. Verify

- Check `hermes skills list` — all skills should be present
- Check `hermes cron list` — the nightly backup job should be scheduled
- Run a manual sync: `hermes cron run <job_id>` for the backup job

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Push fails with 403 | Token expired or wrong scope | Regenerate token with `repo` scope |
| No changes synced | Nothing changed since last push | Normal — the job reports "No changes to sync" |
| Cron fires but no push | Container can't reach GitHub | Check network; token may need `repo` scope |
| Secrets committed | .gitignore missing or wrong | Rebuild .gitignore from template above; amend last commit |

## .gitignore Template

```
# NEVER COMMIT — contains tokens, API keys, secrets
.env
auth.json
*.pem
*.key
credentials/

# NEVER COMMIT — extracted git tokens
.git-credentials

# LARGE / VOLATILE
logs/
sessions/
audio_cache/
cron/output/
hermes-agent/
__pycache__/
*.pyc
venv/
.venv/
node_modules/

# TEMP / CACHE
cache/
tmp/
```
