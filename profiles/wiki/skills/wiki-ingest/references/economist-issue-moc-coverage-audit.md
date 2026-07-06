# Economist issue MOC coverage audit

Use after ingesting a full *The Economist* issue with article-level Notes, especially when matching the June 6 2026 issue structure.

## Goal
Every numbered article extract in `Sources/<Issue> Articles/00-index.md` should map to an ingested `/vault/Notes` page, and those Notes pages should be discoverable through:
1. `MOCs/The Economist MOC.md` under the issue date; and
2. the relevant section/domain MOC, when that section has a domain MOC.

MOCs must link semantic Notes pages, not raw numbered source files such as `[[08-letters...]]`.

## Audit steps
1. Parse `00-index.md` lines of the form `NN. [[source-extract]] ... → [[Semantic Note]]`.
2. Count distinct source sections. A normal issue may have about 18 sections, including format sections such as `The world this week`, `Leaders`, `Letters`, `By Invitation`, `Essay`, and `Obituary`.
3. Verify every mapped `[[Semantic Note]]` exists under `/vault/Notes`.
4. Verify every mapped note appears in `The Economist MOC` under the issue date.
5. Verify every mapped note appears in an appropriate domain MOC when one exists.
   - Route `United States`, `The Americas`, `Asia`, `China`, `Middle East & Africa`, `Europe`, `Britain`, `International`, `Business`, `Finance & Economics`, `Science & Technology`, and `Culture` to their section MOCs.
   - Route `Leaders`, `Essay`, `By Invitation`, and `Obituary` to the domain MOC implied by the article topic.
   - `Letters` can remain issue-indexed in `The Economist MOC` only unless the letters source contains a durable domain-specific theme worth a separate domain note.
6. Search readable MOCs for raw numbered links matching `[[NN-...]]` in the issue date section. There should be zero.
7. Check date ordering in each touched MOC: newest issue sections first (for example July 4 → June 27 → June 6 → May 30).

## Root-owned MOC repair pattern
If a MOC is root-owned but the directory is writable:
- If the file is readable, load current content, insert the issue-date section, then replace via a temp file and `cp --remove-destination` so the result is owned by `hermes`.
- If a MOC is unreadable but git-clean, recover its current tracked content with `git -c safe.directory=/vault -C /vault show HEAD:'MOCs/<Name>.md'`, patch that content, then replace via `cp --remove-destination`.
- Do not report coverage complete until a verification script can read the touched MOCs and find the new semantic links.

## Verification output to report
- Article count and distinct section count.
- Missing semantic Notes count.
- Missing `The Economist MOC` links count.
- Missing domain-MOC links count, with any intentional exceptions (for example Letters issue-only).
- Raw numbered MOC links count.
- Any still-unreadable/root-owned MOCs and exact `chown` command.