# Related-section vs. outbound-link verification

## Context
A 20-page wiki-lint batch was selected using a custom `low-related` heuristic that counted only links inside `## Related`. Several pages already had natural, semantically relevant body links, so the heuristic over-selected them as low-outbound candidates.

## Durable rule
- Treat `## Related` as a semantic-review surface, **not** the sole outbound-link metric.
- For selection diagnostics, count all resolved wiki links in both frontmatter and body, then separately inspect `## Related` for quality.
- A sparse clipping with one genuine neighbor may remain low-outbound; do not add generic links merely to satisfy a section-local count.

## Provenance normalization guard
Rewriting YAML can make an existing quoted source wikilink visible to canonical health scans. Before/after frontmatter serialization, resolve each `sources:` wikilink. If it has no target, preserve the source title/URL as quoted plain provenance rather than a dangling `[[wikilink]]`; do not create a placeholder source page.

## Verification additions
After a helper rewrites frontmatter:
1. Run the canonical vault health script before and after mutation.
2. Attribute any newly detected broken target to the touched file.
3. Repair a dangling `sources:` target as plain provenance, regenerate index/log, and rerun the frozen-batch verification.
