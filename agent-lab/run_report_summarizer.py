import os
from datetime import date

TODAY = date.today()
REPORT_PATH = f"reports/summary_{TODAY}.md"

# Data extracted from the three fungi_check reports
reports = [
    {
        "date": "2026-06-05",
        "total_flagged": 3,
        "rules": {
            "Missing species_name": 1,
            "Future date": 1,
            "Missing substrate": 0,
            "Exact duplicates": 0,
            "Species name format": 2,
            "Invalid site": 1,
            "Invalid observer": 0,
        },
        # (row, site, observer) from flag tables where both fields were visible
        "flagged_rows": [
            (2,  "Los Amigos River Bank", "Maria Lopez"),   # empty species
            (8,  "Cocha Cashu Trail A",   "Maria Lopez"),   # future date
            (7,  "pantano plot 3",        None),            # invalid site
            (3,  None,                   None),             # species format
            (5,  None,                   None),             # species format
        ],
    },
    {
        "date": "2026-06-08",
        "total_flagged": 5,
        "rules": {
            "Missing species_name": 2,
            "Future date": 0,
            "Missing substrate": 1,
            "Exact duplicates": 1,
            "Species name format": 1,
            "Invalid site": 0,
            "Invalid observer": 1,
        },
        "flagged_rows": [
            (3,  "Los Amigos River Bank", "Maria Lopez"),   # empty species
            (7,  "Pantano Plot 3",        "Maria Lopez"),   # empty species
            (5,  "Cocha Cashu Trail A",   "Celil Acar"),    # missing substrate
            (2,  "Cocha Cashu Trail A",   "Celil Acar"),    # duplicate
            (9,  "Cocha Cashu Trail A",   "Celil Acar"),    # duplicate
            (4,  None,                   None),             # species format
            (6,  None,                   "maria lopez"),    # invalid observer
        ],
    },
    {
        "date": "2026-06-10",
        "total_flagged": 10,
        "rules": {
            "Missing species_name": 1,
            "Future date": 1,
            "Missing substrate": 1,
            "Exact duplicates": 1,
            "Species name format": 3,
            "Invalid site": 1,
            "Invalid observer": 1,
        },
        "flagged_rows": [
            (11, "Cocha Cashu Trail A",   "Maria Lopez"),   # empty species
            (12, "Los Amigos River Bank", "Celil Acar"),    # future date
            (13, "Pantano Plot 3",        "Maria Lopez"),   # missing substrate
            (1,  "Cocha Cashu Trail A",   "Celil Acar"),    # duplicate
            (14, "Cocha Cashu Trail A",   "Celil Acar"),    # duplicate
            (2,  None,                   None),             # species format
            (3,  None,                   None),             # species format
            (4,  None,                   None),             # species format
            (5,  "los amigos river bank", None),            # invalid site
            (6,  None,                   "celil acar"),     # invalid observer
        ],
    },
]

# --- Normalisation maps: invalid variant -> canonical name ---
SITE_CANON = {
    "los amigos river bank": "Los Amigos River Bank",
    "pantano plot 3":        "Pantano Plot 3",
}
OBSERVER_CANON = {
    "maria lopez": "Maria Lopez",
    "celil acar":  "Celil Acar",
}

def canon_site(s):
    return SITE_CANON.get(s, s) if s else s

def canon_observer(o):
    return OBSERVER_CANON.get(o, o) if o else o

# --- Aggregate rule counts ---
rule_totals = {}
rule_fires = {}   # how many reports each rule fired in
for r in reports:
    for rule, count in r["rules"].items():
        rule_totals[rule] = rule_totals.get(rule, 0) + count
        if count > 0:
            rule_fires[rule] = rule_fires.get(rule, 0) + 1

rules_ranked = sorted(rule_totals.items(), key=lambda x: x[1], reverse=True)

# --- Aggregate site counts (normalised to canonical names) ---
site_counts = {}
for r in reports:
    for _, site, _ in r["flagged_rows"]:
        if site:
            key = canon_site(site)
            site_counts[key] = site_counts.get(key, 0) + 1
sites_ranked = sorted(site_counts.items(), key=lambda x: x[1], reverse=True)

# --- Aggregate observer counts (normalised to canonical names) ---
observer_counts = {}
for r in reports:
    for _, _, observer in r["flagged_rows"]:
        if observer:
            key = canon_observer(observer)
            observer_counts[key] = observer_counts.get(key, 0) + 1
observers_ranked = sorted(observer_counts.items(), key=lambda x: x[1], reverse=True)

# --- Build report ---
lines = []
def w(s=""): lines.append(s)

w("# Fungi Survey Cross-Report Summary")
w()
w(f"**Generated:** {TODAY}  ")
w(f"**Agent:** report_summarizer_v1  ")
w(f"**Reports read:** {len(reports)}")
w()
w("---")
w()
w("## 1. Reports Included")
w()
w("| Report file | Date | Total flagged rows |")
w("|-------------|------|--------------------|")
for r in reports:
    w(f"| fungi_check_{r['date']}.md | {r['date']} | {r['total_flagged']} |")
w()
total_all = sum(r["total_flagged"] for r in reports)
w(f"**Grand total flagged rows across all reports:** {total_all}")
w()
w("---")
w()
w("## 2. Rules Fired — Ranked by Total Rows Flagged")
w()
w("| Rank | Rule | Total rows flagged | Reports it fired in |")
w("|------|----- |--------------------|---------------------|")
for rank, (rule, total) in enumerate(rules_ranked, 1):
    fires = rule_fires.get(rule, 0)
    w(f"| {rank} | {rule} | {total} | {fires} of {len(reports)} |")
w()
w("---")
w()
w("## 3. Per-Report Rule Breakdown")
w()
header = "| Rule | " + " | ".join(r["date"] for r in reports) + " |"
sep    = "|------|" + "|".join(["------"] * len(reports)) + "|"
w(header)
w(sep)
all_rules = [r for r, _ in rules_ranked]
for rule in all_rules:
    row_vals = " | ".join(str(r["rules"][rule]) for r in reports)
    w(f"| {rule} | {row_vals} |")
w()
w("---")
w()
w("## 4. Sites Appearing Most in Flags")
w()
w("*Counts cover flagged rows where the site field was visible in the flag table.*")
w("*Rows from the species name format table are excluded as that table omits the site column.*")
w()
w("| Site | Flagged row appearances |")
w("|------|------------------------|")
for site, count in sites_ranked:
    w(f"| {site} | {count} |")
w()
w("---")
w()
w("## 5. Observers Appearing Most in Flags")
w()
w("*Counts cover flagged rows where the observer field was visible in the flag table.*")
w("*Rows from the species name format and invalid site tables are partially excluded.*")
w()
w("| Observer | Flagged row appearances |")
w("|----------|------------------------|")
for observer, count in observers_ranked:
    w(f"| {observer} | {count} |")
w()
w("---")
w()
w("## 6. Notable Patterns")
w()
w(f"- **Species name format** is the most persistent issue, firing in all {len(reports)} reports "
  f"and accounting for {rule_totals['Species name format']} flagged rows total.")
w(f"- **Cocha Cashu Trail A** is the site most often associated with flagged rows "
  f"({site_counts.get('Cocha Cashu Trail A', 0)} appearances where site was visible).")
w(f"- **Maria Lopez** and **Celil Acar** appear equally in flagged rows "
  f"({observer_counts.get('Maria Lopez', 0)} each where observer was visible).")
w(f"- Observer and site name capitalisation errors recur across reports, suggesting "
  f"a data-entry discipline issue rather than isolated mistakes.")

os.makedirs("reports", exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Summary written to {REPORT_PATH}")


