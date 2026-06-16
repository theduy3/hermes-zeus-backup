---
name: productivity-platforms
description: "Umbrella for productivity/document platforms: Google Workspace, Airtable, Notion, Obsidian, PDFs/OCR, PowerPoint, Teams meeting pipelines, maps, and location lookups."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, documents, google-workspace, airtable, notion, obsidian, pdf, powerpoint, teams, maps]
---

# Productivity Platforms

Use this umbrella when the task involves common productivity systems, documents, notes, presentations, databases, calendars/email/drive, meeting summaries, PDFs/OCR, or geospatial lookup.

## Platform selection

- Google Workspace: Gmail, Calendar, Drive, Docs, and Sheets via configured CLI/API credentials.
- Airtable: records, bases, tables, filters, CRUD, and upserts through REST.
- Notion: pages, databases, blocks, markdown import/export, and API/CLI workflows.
- Obsidian: local vault read/search/write, daily notes, and durable markdown knowledge work.
- PowerPoint: create/read/edit `.pptx` decks, slides, notes, templates, and Office XML when necessary.
- PDFs/OCR: extract text from PDFs/scans with PyMuPDF or marker-style tools; edit PDFs only through appropriate PDF tooling.
- Teams meeting pipeline: inspect, replay, summarize, and manage Microsoft Graph subscription-backed meeting jobs.
- Maps: geocoding, POIs, routes, timezones, distance, and nearby-place lookups.

## Shared workflow

1. Identify the source system, target system, and credentials/files required.
2. Use platform-specific search/list calls before mutation.
3. Preserve user data structure: folders, vault paths, databases, tables, slides, and metadata.
4. For writes/sends/deletes, make target and content explicit before executing when ambiguity could damage data.
5. Verify the resulting record/file/page/deck/job by reading it back or reporting a concrete ID/path/status.

## Document extraction and transformation

When extracting from documents, retain provenance: source path/URL, extraction tool, page range, and known OCR/formatting limitations.