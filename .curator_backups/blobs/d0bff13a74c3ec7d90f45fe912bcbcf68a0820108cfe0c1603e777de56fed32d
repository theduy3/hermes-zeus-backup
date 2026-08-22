# Codex gpt-5.5 auto-compaction notice

Use when the user replies to this startup/gateway notice and asks to "fix this issue":

```text
ℹ Codex gpt-5.5 caps context at 272K, so auto-compaction was raised to 85% (from 50%) to use more of the window before summarizing.
Opt back out: hermes config set compression.codex_gpt55_autoraise false
```

## Interpretation

The notice is informational, not a model failure. In this user's Hermes setup, treat "fix this" as: keep the better 85% compaction threshold, but stop the repeated opt-out notice.

## Repair pattern

1. Inspect relevant `config.yaml` files for `compression:` blocks:
   - default: `~/.hermes/config.yaml`
   - profiles: `~/.hermes/profiles/<profile>/config.yaml`
2. For default and actively used profiles, set:
   ```yaml
   compression:
     threshold: 0.85
     codex_gpt55_autoraise: false
   ```
   Preserve the rest of each `compression:` block.
3. Back up config files before scripted edits.
4. Verify with a minimal startup/chat run and grep for the notice text. Passing condition: no `Codex gpt-5.5 caps context` notice appears.
5. If gateway processes are long-lived, restart affected gateways only if the user needs the change to apply immediately to already-running sessions.

## Pitfalls

- Do not just set `codex_gpt55_autoraise: false` while leaving `threshold: 0.5`; that silently reverts to early compaction at ~136K.
- Do not edit only the default profile when the alert came from a profile gateway; apply the same pair to the profile that emitted it, and commonly all active Telegram profiles for consistency.
- Do not patch the protected bundled `hermes-agent` skill for this; record operational repair patterns here unless editing source code behavior is explicitly requested.
