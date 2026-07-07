# Value Line Selection & Opinion PDF ingest

Use this when the user uploads a Value Line `Selection & Opinion` PDF such as `report-3.pdf` and asks to ingest it.

## Trigger

- PDF text includes `Value Line Selection & Opinion`.
- Usually 10–12 pages with sections such as `The Value Line View`, `Model Portfolios`, `Federal Reserve Data`, `Market Monitor`, `Value Line Asset Allocation Model`, and `Stock Market Averages`.

## Required outputs

1. Copy the PDF to `/vault/Attachments/` using source-aligned naming:
   - `YYYY-MM-DD - Value Line Selection and Opinion <Issue Date>.<ext>`
   - Example: `2026-07-07 - Value Line Selection and Opinion July 10 2026.pdf`
2. Create a source archive in `/vault/Sources/`:
   - `YYYY-MM-DD - Value Line Selection and Opinion <Issue Date>.md`
   - Include `original_filename` if the uploaded filename was generic/random, e.g. `report-3.pdf`.
   - Include full extracted text by page under `## Extracted Text`.
3. Create/update a semantic market note in `/vault/Notes/`:
   - `Stock Market Today <Issue Date>.md`
   - Use `type: entity`, tags `finance`, `investing`, `market-analysis`, `macro`, `value-line`.
   - Include summary, key points, index snapshot table, rates/money/breadth signals, market interpretation, and related links.
4. Update `[[Economic Indicators]]` with the relevant macro/breadth/rates datapoints.
5. Update `[[15 Finance & Economics MOC]]` under `## Finance & Markets` or the most relevant issue/date section.
6. Regenerate or patch `System/wiki-index.md` and append `System/wiki-log.md`.

## Data to extract

Prefer source-grounded numbers over prose paraphrase. Capture, when present:

- GDP growth/revisions
- PCE/core PCE inflation
- Fed Funds target, prime rate, SOFR
- Treasury yields: 3-month, 1-year, 5-year, 10-year, 30-year
- Stock index levels and weekly/12-month changes
- Value Line Geometric / Arithmetic indexes
- Market breadth: new highs/new lows
- Sentiment/valuation: put/call ratio, median P/E, dividend yield, bond yield minus earnings yield
- Value Line Asset Allocation Model stock/bond/cash percentages
- Risk framing: AI capex/private-credit risk, oil/geopolitical shock, election seasonality, sector rotations

## Link/routing expectations

- Link the new market note to prior `Stock Market Today ...` notes when it continues the same macro thread.
- Link to `[[Economic Indicators]]`, `[[Monetary Policy]]`, `[[Intermarket Relationships Across Asset Classes]]`, `[[Crash Indicators]]`, and any durable theme such as `[[AI as Investment Megatrend Framing]]` when supported by the source.
- For Value Line macro/market PDFs, `Economic Indicators` should list newest additions above older newsletter/Economist additions when editing structure allows.

## Verification

Before replying, verify:

- Source archive exists and includes `original_filename` for generic upload names.
- Attachment exists in `/vault/Attachments/`.
- Inbox staging file is removed or Inbox is otherwise clean.
- New/updated note appears in `System/wiki-index.md`.
- `Economic Indicators` and `15 Finance & Economics MOC` contain exact new issue/date references.
- `wiki-log.md` contains an ingest entry for the issue.
