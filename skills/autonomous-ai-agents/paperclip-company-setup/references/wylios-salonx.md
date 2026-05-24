# Wylios / SalonX Paperclip setup reference

Session-specific reference for setting up a SaaS company in Paperclip with Hermes agents and a minimal Discord operating bridge.

## Business context captured

- Company: Wylios
- Product: SalonX
- Positioning: premium SaaS; becoming a POS with terminal payment
- Market: Quebec, Canada, US
- Languages: English, French, Vietnamese, Khmer
- First buyers: independent salons, multi-location salons, Vietnamese-owned salons, franchises
- Stage: MVP
- 30-day goal: first 10 clients, 2 paid clients
- Unfair advantage: deep nail salon operator knowledge; solves real salon owner pain points

## SalonX product pain points

SalonX is positioned as: “No More Drama. Just a Salon That Runs.”

Core pains:
- queue/turn disputes
- unverifiable tip and commission calculations
- technicians unsure about income received
- void/edit/reopen disputes
- booking confirmations/reminders/no-show handling
- end-of-day cash variance arguments
- client win-back and birthday marketing
- inventory distribution and transfers
- multi-store roles and permissions

Stack shared by user:
- React
- TypeScript
- Supabase
- Vite
- Tailwind CSS

## Generated org shape

Agents:
- Wylios CEO
- SalonX Product Lead
- SalonX GTM Lead
- SalonX Sales Rep
- SalonX Market Researcher
- SalonX Engineer

Projects:
- SalonX 30-Day Launch
- Discord Operations for Wylios

Starter tasks/routines:
- Build SalonX market and competitor map
- Define SalonX ICP, offer, and demo narrative
- Build outreach scripts for first 10 qualified SalonX clients
- Audit SalonX MVP demo readiness
- Verify SalonX repo access and engineering setup
- Design Wylios Discord command center
- Build Paperclip ↔ Discord operating bridge
- Daily SalonX sales outreach routine
- Weekly Wylios pipeline review routine
- Daily Wylios Discord operating loop

## Implementation notes learned

- Paperclip was initialized with `npx --yes paperclipai onboard --yes --bind loopback`.
- Paperclip server ran at `http://127.0.0.1:3100`.
- `hermes_local` was already listed by `/api/adapters` as a built-in adapter; installing `hermes-paperclip-adapter` as a plugin was unnecessary and failed because it was not packaged as a Paperclip plugin manifest.
- Dry-run import command used:
  `npx --yes paperclipai company import /home/hermes/wylios-paperclip --dry-run --yes --json`
- Dry run initially failed because recurring tasks lacked `project: salonx-30-day-launch`.
- Dry run initially warned because agents referenced `hermes-agent` skill but the package did not vendor it; removing those package skill refs cleared warnings.
- Final dry-run result after Discord expansion: errors 0, warnings 0, agents 6, projects 2, issues/routines 10.
- Final import command used:
  `npx --yes paperclipai company import /home/hermes/wylios-paperclip --yes --json | tee /tmp/wylios-import-result.json`
- Import result created company/agents/projects but omitted issues from final summary, so verify issues explicitly with:
  `npx --yes paperclipai issue list --company-id <company-id> --json`
- Use `--company-id`, not `--company`, for `issue list`.
- `issue checkout` command format:
  `npx --yes paperclipai issue checkout WYL-2 --agent-id <agent-id> --json`
- If an issue is created with `--assignee-agent-id`, Paperclip may immediately auto-start it and set status `in_progress` with an execution lock. A follow-up manual `issue checkout` can then return 409 `Issue checkout conflict`; inspect with `issue get <ID> --json` before treating that as failure.
- `issue comment` command format:
  `npx --yes paperclipai issue comment WYL-2 --body "..." --json`
- `issue update` can mark done and add a comment:
  `npx --yes paperclipai issue update WYL-2 --status done --comment "..." --json`
- For blocked routine issues with stranded recovery (e.g. WYL-8), `issue release <ID> --json` can clear the lock/status back to a workable state; then `issue update <ID> --status done --assignee-agent-id <agent-id> --comment "..." --json` can finalize the manual resolution.
- SalonX repo access failed from runtime, likely private/inaccessible; future setup should request GitHub access/token or a local checkout path before claiming code-level facts.

## SalonX market / GTM findings from WYL-5

When continuing SalonX 30-day launch work, preserve this positioning:

- Do not position SalonX v1 as a booking/POS replacement.
- Position it as the internal operating system / operations ERP for high-volume nail salons.
- Sharp tagline: “Booking software gets customers in. SalonX helps you run the salon once they arrive.”
- Best wedge: fair queue + technician assignment + ticket lifecycle + tips/commission + daily closeout.
- Primary ICP: independent or 2-10 location nail salons with 6-25 technicians, high walk-in volume, manual tickets/whiteboards/spreadsheets/POS exports, complex tips/commission/payroll, and multilingual staff.
- First paid pilot: 30-Day Salon Operations Control Pilot, roughly $500 up to 15 techs or $750 for 16-25 techs, credited to subscription if converted.
- Proof points to collect: closeout time reduction, tip/commission calculation time reduction, ticket tracking coverage, queue/turn disputes reduced, owner confidence/remote visibility.
- Competitor frame: Square/Clover/Lightspeed are POS/payment systems to complement; Fresha/Booksy/Vagaro/GlossGenius/Mindbody/Mangomint/Boulevard/Phorest are booking/client-management-first; NailSoft is closest vertical threat.
- Quebec-first lead sources: Google Maps, Yelp, YellowPages/PagesJaunes, Facebook/Instagram, booking marketplace surfaces, then enterprise registries for enrichment.
- First prospect geography: Montréal/Laval/Brossard/Longueuil first, then GTA, Orange County CA, Houston, Falls Church/Annandale, San Jose/Milpitas, Vancouver/Richmond, Calgary/Edmonton.

Canonical WYL-5 report paths used in the session:

```text
/home/hermes/wylios-paperclip/docs/SALONX_MARKET_COMPETITOR_MAP.md
/home/hermes/.paperclip/instances/default/projects/d6d7675b-25a6-46bb-acf5-eb8b7c9a6699/bb191779-cd80-413f-b840-1ffc2ae82585/_default/salonx-market-competitor-map.md
```

Recommended next issue after WYL-5:
Create a verified named first-50 prospect spreadsheet for Quebec-first outreach. Unblocker: choose lead-enrichment path — manual Google Maps/Yelp, VA, Apify/SerpAPI, or Clay/Apollo-style enrichment.

## Minimal Discord ↔ Paperclip bridge pattern

For the first working bridge, do not start with a native Discord slash-command bot. Use this path:

Discord user → Hermes Discord gateway profile → terminal helper script → Paperclip CLI/API → Paperclip issue/comment/checkout → Hermes local agent.

In this session, a company-local helper script was created:

```bash
/home/hermes/wylios-paperclip/scripts/wylios-paperclip.py
```

It pinned Wylios IDs and wrapped:
- `company`
- `agents`
- `list`
- `get WYL-N`
- `create --title ... --description ... --agent ... --project ...`
- `comment WYL-N --body ... [--resume]`
- `checkout WYL-N --agent ...`
- `release WYL-N`
- `done WYL-N --comment ... [--agent ...]`

Smoke tests used:

```bash
chmod +x /home/hermes/wylios-paperclip/scripts/wylios-paperclip.py
/home/hermes/wylios-paperclip/scripts/wylios-paperclip.py company >/tmp/wylios-bridge-company-smoke.json
/home/hermes/wylios-paperclip/scripts/wylios-paperclip.py list >/tmp/wylios-bridge-issues-smoke.json
/home/hermes/wylios-paperclip/scripts/wylios-paperclip.py get WYL-13
```

Observed results:
- company smoke test returned Wylios
- issue list smoke test returned 7 normal issues

Docs were written to:

```bash
/home/hermes/wylios-paperclip/docs/DISCORD_BRIDGE.md
```

After smoke testing, WYL-2 was updated to `done` with a comment describing:
- helper path
- docs path
- smoke-test results
- limitation: not a native Discord slash-command bot yet

## User-facing output pattern

Keep final reports terse:
- issue status
- created script/doc paths
- smoke-test result
- direct commands to use
- known limitation only if actionable
