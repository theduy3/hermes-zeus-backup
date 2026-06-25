# Situational Awareness 13F / 13G Workflow

Use when the user asks for Situational Awareness LP, Leopold Aschenbrenner fund holdings, or buy / hold / sell updates.

## Durable identifiers

- SEC CIK: `0002045724` for Situational Awareness LP.
- SEC submissions endpoint: `https://data.sec.gov/submissions/CIK0002045724.json`.
- Latest observed filings in this session:
  - 2026-05-18 `13F-HR` accession `0002045724-26-000008`.
  - 2026-05-27 `SCHEDULE 13G` accession `0000935836-26-000303` for Nebius Group.

## Process

1. Fetch SEC submissions JSON for CIK `0002045724` with a User-Agent.
2. Identify latest and prior `13F-HR` accessions.
3. Fetch each filing `index.json` under `https://www.sec.gov/Archives/edgar/data/2045724/{accession_without_dashes}/`.
4. Parse the non-`primary_doc.xml` XML information table.
5. Extract `nameOfIssuer`, `titleOfClass`, `putCall` if present, `value`, and nested `shrsOrPrnAmt/sshPrnamt`.
6. Sort by `value` for a holdings list. Compare latest vs prior by `(issuer, class, putCall)` for buy / add, hold, reduce, and sold-out changes.
7. Separately parse Schedule 13G for beneficial ownership facts. In this session, the Nebius 13G reported 12,410,060 Class A ordinary shares and 5.6% beneficial ownership.

## Pitfalls

- 13F `value` is reported in thousands of dollars in SEC XML. Convert to dollars by multiplying by 1,000 only if presenting absolute dollars. If parsing with raw XML values already as thousands, label clearly.
- Option rows in 13F are not equivalent to cash equity exposure. Keep `Put` and `Call` rows separate from `Stock` rows and avoid saying the fund is simply long or short from notional-style option values.
- Nebius may not appear as a normal 13F row if the key update is a Schedule 13G. Pull 13G/13D filings as well when the user asks about NBIS.
- Reddit / social commentary can help gauge sentiment, but use SEC filings as the source of truth for holdings.

## Watchlist integration

For Duy's Obsidian watchlist, add liquid tickers from the latest holdings to `/vault/System/Stock Watchlist.md` under `Watchlist:` one per line. Verify tickers against a market data source when possible. Skip or flag uncertain tickers rather than inventing them.
