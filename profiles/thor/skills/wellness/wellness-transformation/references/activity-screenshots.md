# Processing Activity Screenshots

When the user sends a screenshot of their activity tracker (Google Fit, Apple Health, Strava, etc.):

## Workflow

1. **Try vision first** — if the current model supports vision/image inputs, use it directly.
2. **Fall back to OCR** — use tesseract (if available) or other OCR tools to extract text.
3. **Parse the numbers** — activity screenshots typically show: steps, distance (km), active calories, move minutes, heart points.
4. **Log to the daily food/activity log** under the Activity section.

## Common Activity Tracker Layouts

### Google Fit
```
[Steps Count]
Heart Pts | Steps
[cal] Cal | [km] km | [min] Move Min
```

### Apple Health / Fitness
```
[Steps Count] Steps
[km] km | [cal] Cal | [min] min
```

## What to Log

- Steps (primary)
- Distance (km)
- Move/active minutes
- Heart points (Google Fit)
- Active calories (if shown)

Keep it brief in the log — one line under `### Activity` in the daily section.
