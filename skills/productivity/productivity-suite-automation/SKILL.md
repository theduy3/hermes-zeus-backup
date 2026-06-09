---
name: productivity-suite-automation
description: "Use when automating productivity services and document workflows: Airtable, Google Workspace, Notion, maps/geocoding, PDFs/OCR, PowerPoint, or Teams meeting pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, documents, google-workspace, notion, airtable, maps, pdf, powerpoint, teams]
    related_skills: []
---

# Productivity Suite Automation

## Overview

This umbrella covers API/CLI workflows for common productivity services and document artifacts. Route database, document, spreadsheet, map/geocode, PDF/OCR, deck, and meeting-pipeline requests through this class-level skill, then use the relevant service subsection.

## When to Use

- Airtable records, bases, filters, upserts, or REST API calls.
- Gmail, Calendar, Drive, Docs, Sheets, or Google Workspace automation.
- Notion pages, databases/data sources, blocks, or markdown import/export.
- Maps, geocoding, POIs, routes, or timezones.
- PDF editing/extraction, OCR, or document text extraction.
- PowerPoint deck creation/editing/QA.
- Teams meeting transcript/summary pipeline operations.

## Universal Rules

1. Verify credentials/environment before attempting API mutations.
2. Fetch/list the target object before updating or deleting it.
3. Preserve IDs/URLs returned by APIs and include them in final results.
4. For generated documents/decks, open/read back or render enough output to verify the artifact.

## Service Sections

### Airtable
Use REST/curl for CRUD, filtering, pagination, and upserts. Match field names exactly and handle paginated results.

### Google Workspace
Use `gws` or Python API bridge for Gmail, Calendar, Drive, Docs, and Sheets. Respect OAuth setup and quote Gmail search syntax carefully.

### Notion
Use Notion API or `ntn` CLI. Distinguish databases from data sources for newer API versions and preserve block/property shapes.

### Maps
Use OpenStreetMap/OSRM-style tools for geocoding, POIs, routes, and timezones. Report source and uncertainty for places.

### PDFs and OCR
Choose lightweight extraction first (`pymupdf`/tesseract) and high-quality OCR (`marker-pdf`) when scans/layout require it. Verify extracted text snippets.

### PowerPoint
Use script-based editing/creation, then QA by inspecting slide XML/text or rendering images when possible.

### Teams Meeting Pipeline
Use Hermes CLI pipeline commands to summarize, inspect status, replay jobs, and manage Graph subscriptions. Remember that Graph subscriptions expire.

## Archived Package References

Former narrow skills absorbed into this umbrella are preserved under `references/<old-skill-name>/` with original SKILL.md and support files intact.

## Common Pitfalls

- Mutating the wrong service object because names are not unique.
- Dropping pagination tokens.
- Reporting document edits without read-back verification.
- Forgetting timezones for calendar/routes/meeting work.

## Verification Checklist

- [ ] Credentials and target IDs are verified.
- [ ] API/CLI output is captured.
- [ ] Mutations return concrete handles or read-back confirmation.
