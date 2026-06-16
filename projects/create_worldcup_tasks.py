from pathlib import Path
import re

base = Path('/vault/Tasks/tasks')
base.mkdir(parents=True, exist_ok=True)

def kebab(s):
    s = s.lower().replace("côte", "cote")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip('-')

items = [
    ("Follow World Cup: France vs Senegal", "2026-06-16", "12:00 PDT", "Group I", "New York/New Jersey Stadium", "Marquee France opener; Senegal is a strong opponent."),
    ("Follow World Cup: Argentina vs Algeria", "2026-06-16", "18:00 PDT", "Group J", "Kansas City Stadium", "Argentina group-stage marquee match."),
    ("Follow World Cup: Portugal vs Congo DR", "2026-06-17", "10:00 PDT", "Group K", "Houston Stadium", "Portugal opener / marquee match."),
    ("Follow World Cup: England vs Croatia", "2026-06-17", "13:00 PDT", "Group L", "Dallas Stadium", "Big European matchup."),
    ("Follow Korea Republic: Mexico vs Korea Republic", "2026-06-18", "18:00 PDT", "Group A", "Guadalajara Stadium", "Korea team match. Mexico host-nation atmosphere; likely must-watch."),
    ("Follow World Cup: USA vs Australia", "2026-06-19", "12:00 PDT", "Group D", "Seattle Stadium", "USA host-nation match."),
    ("Follow World Cup: Brazil vs Haiti", "2026-06-19", "18:00 PDT", "Group C", "Philadelphia Stadium", "Brazil group-stage match."),
    ("Follow World Cup: Netherlands vs Sweden", "2026-06-20", "10:00 PDT", "Group F", "Houston Stadium", "Strong European matchup."),
    ("Follow World Cup: Germany vs Côte d'Ivoire", "2026-06-20", "13:00 PDT", "Group E", "Toronto Stadium", "Germany opener / marquee match."),
    ("Follow World Cup: Spain vs Saudi Arabia", "2026-06-21", "09:00 PDT", "Group H", "Atlanta Stadium", "Spain group-stage match."),
    ("Follow World Cup: Argentina vs Austria", "2026-06-22", "10:00 PDT", "Group J", "Dallas Stadium", "Argentina second group match."),
    ("Follow World Cup: England vs Ghana", "2026-06-23", "13:00 PDT", "Group L", "Boston Stadium", "England group-stage match."),
    ("Follow World Cup: Switzerland vs Canada", "2026-06-24", "12:00 PDT", "Group B", "BC Place Vancouver", "Canada match in Vancouver."),
    ("Follow World Cup: Scotland vs Brazil", "2026-06-24", "15:00 PDT", "Group C", "Miami Stadium", "Brazil vs Scotland marquee group match."),
    ("Follow Korea Republic: South Africa vs Korea Republic", "2026-06-24", "18:00 PDT", "Group A", "Monterrey Stadium", "Korea team match; possible qualification decider."),
    ("Check Korea Republic knockout schedule", "2026-06-25", "After Group A ends", "Korea Republic", "TBD", "Check whether Korea advanced and which knockout match to follow: 2A vs 2B on Jun 28, 1A vs 3CEFHI on Jun 30, or possible 3A slot."),
    ("Follow World Cup: Türkiye vs USA", "2026-06-25", "19:00 PDT", "Group D", "Los Angeles Stadium", "USA host-nation match."),
    ("Follow World Cup: Norway vs France", "2026-06-26", "12:00 PDT", "Group I", "Boston Stadium", "France group-stage match with Norway."),
    ("Follow World Cup: Uruguay vs Spain", "2026-06-26", "17:00 PDT", "Group H", "Guadalajara Stadium", "Elite group-stage matchup."),
    ("Follow World Cup: Colombia vs Portugal", "2026-06-27", "16:30 PDT", "Group K", "Miami Stadium", "Likely Group K decider; marquee matchup."),
    ("Follow Korea Republic possible Round of 32: 2A vs 2B", "2026-06-28", "12:00 PDT", "Round of 32", "Los Angeles Stadium", "If Korea finishes 2nd in Group A, this is the likely knockout match."),
    ("Follow Korea Republic possible Round of 32: 1A vs 3CEFHI", "2026-06-30", "18:00 PDT", "Round of 32", "Mexico City Stadium", "If Korea finishes 1st in Group A, this is the likely knockout match."),
    ("Follow World Cup Semifinal 1", "2026-07-14", "12:00 PDT", "Semifinal", "Dallas Stadium", "World Cup semifinal."),
    ("Follow World Cup Semifinal 2", "2026-07-15", "12:00 PDT", "Semifinal", "Atlanta Stadium", "World Cup semifinal."),
    ("Follow World Cup Final", "2026-07-19", "12:00 PDT", "Final", "New York/New Jersey Stadium", "World Cup final."),
]

created=[]; skipped=[]
for title, due, time, stage, location, note in items:
    fn = base / f"{kebab(title)}.md"
    if fn.exists():
        skipped.append(str(fn))
        continue
    content = f"""---\ntype: task\ndue_date: {due}\ntags: [personal, world-cup, soccer]\nstatus: pending\n---\n# {title}\n\nKickoff: {due} {time}\nStage: {stage}\nLocation: {location}\n\n{note}\n\nSource checked: FixtureDownload FIFA World Cup 2026 feed, times converted to America/Vancouver/Pacific.\n"""
    fn.write_text(content, encoding='utf-8')
    created.append(str(fn))

missing=[p for p in created if not Path(p).exists()]
print(f"created={len(created)} skipped_existing={len(skipped)} missing={len(missing)}")
for p in created:
    print(p)
if skipped:
    print('SKIPPED')
    for p in skipped:
        print(p)
if missing:
    raise SystemExit('Missing files: '+repr(missing))
