---
name: communication-and-social-clients
description: "Use when operating communication/social clients from Hermes: email via Himalaya, X/Twitter via xurl, and Yuanbao groups/DMs with mention/query workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [email, social-media, messaging, x, twitter, yuanbao]
    related_skills: []
---

# Communication and Social Clients

## Overview

This umbrella covers user-visible communication channels and social clients. Because these tools send messages externally, exact recipient/account confirmation and post-send verification matter.

## When to Use

- Search/read/send email through Himalaya.
- Post/search/DM or use X/Twitter APIs through xurl.
- Send Yuanbao group/DM messages, mention users, or query group/member info.

## Verification Checklist

- [ ] Account/channel/recipient identified unambiguously.
- [ ] Credentials/tool setup checked.
- [ ] External sends only performed when user intent is explicit.
- [ ] Returned message IDs/statuses recorded when available.
