---
name: productivity-office-automation
description: "Use when operating productivity and office systems from Hermes: Airtable, Google Workspace, Notion, maps/geocoding, PDF/OCR/document processing, PowerPoint decks, and Teams meeting pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, office, documents, spreadsheets, google-workspace, notion, airtable, pdf, powerpoint, teams]
    related_skills: []
---

# Productivity and Office Automation

## Overview

This umbrella covers external productivity applications and document workflows. The former per-service packages are preserved under `references/source-packages/` with scripts/templates intact.

## When to Use

- Work with Airtable, Google Workspace, Notion, or Teams meeting summaries.
- Geocode, route, or inspect places/timezones.
- Extract OCR/text from PDFs/scans or edit PDF text.
- Create/read/edit PowerPoint decks.

## Service Map

- **Airtable:** REST records, formulas, filters, upserts.
- **Google Workspace:** Gmail, Calendar, Drive, Docs, Sheets via `gws`/Python bridge.
- **Notion:** pages, databases/data sources, blocks, markdown, Workers.
- **Maps:** OSM/OSRM geocode, POIs, routes, timezone/location-pin workflows.
- **PDF/OCR:** nano-pdf edits and OCR/document extraction.
- **PowerPoint:** create, read, edit, validate, and export `.pptx` decks.
- **Teams pipeline:** meeting summaries, replay/status, Microsoft Graph subscription management.

## Verification Checklist

- [ ] Target service/account/resource identified.
- [ ] Credentials and tool availability checked.
- [ ] For writes, read back the changed record/document/deck when possible.
