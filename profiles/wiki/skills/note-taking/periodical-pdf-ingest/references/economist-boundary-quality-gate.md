# Economist boundary quality gate

Use this reference after bulk-ingesting a full *Economist* issue.

## Lesson

A full issue can pass structural checks while still having bad article-boundary slicing. During the July 18 2026 issue ingest, a sample note for `Kevin Warsh Fed Force Five` initially began with the tail of the preceding China austerity article because both appeared on the same PDF page and the extraction window started before the true `Fed force 5` heading.

## Required spot-check

After generating article-level notes and MOCs:

1. Find articles whose source pages are shared with a prior/next article.
2. Read 3-5 generated Notes from shared pages, especially short columns and Finance/Business pages.
3. Verify the `## Briefing` begins from the intended article heading or first paragraph.
4. Check that `## Concrete Details` are not mostly chart fragments or previous-article facts.
5. If any sample is contaminated, repair boundary slicing before finalizing.

## Good final verification includes

- article count excluding `00-index.md`;
- missing notes count;
- missing `## Briefing` count;
- raw numbered source links in MOCs count;
- duplicate date blocks in numbered MOCs;
- newest-first MOC ordering;
- semantic spot-check passed for shared-page samples.
