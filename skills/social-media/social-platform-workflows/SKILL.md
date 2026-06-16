---
name: social-platform-workflows
description: "Use when operating or designing workflows for social/messaging platforms: X/Twitter, Yuanbao groups/DMs, platform auth, posting, reading, mentions, and safe write actions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, messaging, x, twitter, yuanbao, posting, dms, mentions]
    related_skills: [xurl, yuanbao, telegram]
---

# Social Platform Workflows

## Overview

This umbrella covers social and messaging platform operations that share the same class-level concerns: verify account/tool readiness, avoid leaking credentials, resolve the exact target user/post/thread, confirm write actions when appropriate, execute via the platform-native tool, and report verifiable results.

Use provider-specific reference packages for command syntax and platform quirks:

- `references/xurl.md` — X/Twitter via the official `xurl` CLI, including auth safety, posting, search, media, DMs, and troubleshooting.
- `references/yuanbao.md` — Yuanbao groups, exact nickname lookup, @mentions, group metadata, member search, and DMs.

## When to Use

- The user asks to post, reply, search, read, like, DM, follow, or manage content on X/Twitter.
- The user asks to @mention, DM, or inspect members/groups in Yuanbao.
- The task involves platform-specific auth state, rate limits, or target resolution before a social write action.
- You need to design or troubleshoot a social/messaging workflow without exposing tokens.

## Universal Workflow

1. **Identify the platform and action class.** Read-only actions can usually proceed after tool/auth checks; write actions require extra target and intent verification.
2. **Check prerequisites without exposing secrets.** Use safe status commands only. Never print token/config files.
3. **Resolve the target exactly.** For posts, read the post or parse the platform ID. For people, look up the exact handle/nickname/member record.
4. **Confirm risky writes.** Confirm before posting, replying, liking, reposting, following, blocking, deleting, or sending DMs unless the user’s instruction is already explicit and scoped.
5. **Execute through the provider-specific tool.** Use the reference package for syntax and pitfalls.
6. **Verify and report.** Return the platform response, message ID/post ID, or a concise status; include real errors when blocked.

## Provider Notes

### X/Twitter via xurl

Use `xurl` for official X API access. Never inspect `~/.xurl`, never pass inline secrets, and never use verbose output in an agent session. Start with `xurl auth status` and a cheap read such as `xurl whoami` or a small search before writes. See `references/xurl.md` for full command tables and troubleshooting.

### Yuanbao

Yuanbao group replies are delivered by the gateway: your final text is the message. For @mentions, first query group members with mention metadata, then include the exact `@nickname` in the reply. Use Yuanbao-specific DM tools for private messages rather than generic send-message tools. See `references/yuanbao.md` for examples.

## Safety Rules

- Never ask users to paste tokens or client secrets into chat.
- Never read or summarize local credential files.
- Do not fabricate success; verify with tool output or platform IDs.
- For public or semi-public write actions, keep tone and content exactly aligned with the user’s request.
- If multiple candidate users/posts match, ask for clarification instead of guessing.

## Verification Checklist

- [ ] Platform and target were identified unambiguously.
- [ ] Credential checks avoided secret disclosure.
- [ ] Risky write actions had explicit user intent.
- [ ] Provider-specific command/tool output was captured.
- [ ] Final response includes the actual status, ID, or blocker.
