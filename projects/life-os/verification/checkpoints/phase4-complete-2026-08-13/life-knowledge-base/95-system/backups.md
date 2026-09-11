# Backups

Back up `/home/hermes/.hermes/projects/life-os/life-knowledge-base` and `/home/hermes/.hermes/projects/life-os/tracker/data/tracker.sqlite3` with encrypted filesystem snapshots. Secrets are independently stored at `~/.config/life-tracker/secrets.env` with mode 600. Restore files, run `python3 /home/hermes/.hermes/projects/life-os/tracker/tools.py verify`, then restart.
