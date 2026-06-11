import csv
import os
from datetime import date

CSV_PATH = "data/test_fungi_survey.csv"
TODAY = date.today()
REPORT_PATH = f"reports/fungi_check_{TODAY}.md"

REQUIRED_COLUMNS = ["date", "site", "species_name", "substrate", "observer", "notes"]
VALID_SITES = {"Cocha Cashu Trail A", "Los Amigos River Bank", "Pantano Plot 3"}
VALID_OBSERVERS = {"Celil Acar", "Maria Lopez"}

if not os.path.exists(CSV_PATH):
    print(f"ERROR: File not found: {CSV_PATH}")
    exit(1)

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames or []
    missing = [c for c in REQUIRED_COLUMNS if c not in headers]
    if missing:
        print(f"ERROR: Missing required column(s): {', '.join(missing)}")
        exit(1)
    rows = list(reader)

total_rows = len(rows)

unique_sites = sorted({r["site"] for r in rows})
unique_observers = sorted({r["observer"] for r in rows})

empty_species = [(i+1, r) for i, r in enumerate(rows) if not r["species_name"].strip()]

future_dates = []
for i, r in enumerate(rows):
    try:
        row_date = date.fromisoformat(r["date"].strip())
        if row_date > TODAY:
            future_dates.append((i+1, r))
    except ValueError:
        pass

empty_substrate = [(i+1, r) for i, r in enumerate(rows) if not r["substrate"].strip()]

seen = {}
duplicates = []
for i, r in enumerate(rows):
    key = tuple(r[c] for c in REQUIRED_COLUMNS)
    if key in seen:
        duplicates.append((seen[key]+1, i+1, r))
    else:
        seen[key] = i

def bad_species_format(name):
    if not name.strip():
        return None
    words = name.strip().split()
    if len(words) < 2:
        return "Single word only"
    if name == name.upper():
        return "All uppercase"
    if name == name.lower():
        return "All lowercase"
    if not (words[0][0].isupper() and words[0][1:].islower() and words[1] == words[1].lower()):
        return "Incorrect capitalisation"
    return None

species_format_issues = []
for i, r in enumerate(rows):
    name = r["species_name"].strip()
    if not name:
        continue
    issue = bad_species_format(name)
    if issue:
        species_format_issues.append((i+1, r, issue))

invalid_sites = [(i+1, r) for i, r in enumerate(rows) if r["site"] not in VALID_SITES]
invalid_observers = [(i+1, r) for i, r in enumerate(rows) if r["observer"] not in VALID_OBSERVERS]

os.makedirs("reports", exist_ok=True)

lines = []
def w(s=""): lines.append(s)

w("# Fungi Survey Check Report")
w()
w(f"**File:** {CSV_PATH}  ")
w(f"**Date of check:** {TODAY}  ")
w("**Agent:** fungi_survey_checker_v1")
w()
w("---")
w()
w("## 1. Column Check")
w()
w("All required columns present: `date`, `site`, `species_name`, `substrate`, `observer`, `notes` ✓")
w()
w("---")
w()
w("## 2. Summary")
w()
w("| Metric | Value |")
w("|--------|-------|")
w(f"| Total rows (excluding header) | {total_rows} |")
w(f"| Unique sites (raw) | {len(unique_sites)} |")
w(f"| Unique observers (raw) | {len(unique_observers)} |")
w()
w("---")
w()
w("## 3. Unique Sites Found")
w()
for s in unique_sites:
    tag = " *(invalid — see Section 10)*" if s not in VALID_SITES else ""
    w(f"- {s}{tag}")
w()
w("---")
w()
w("## 4. Unique Observers Found")
w()
for o in unique_observers:
    tag = " *(invalid — see Section 11)*" if o not in VALID_OBSERVERS else ""
    w(f"- {o}{tag}")
w()
w("---")
w()
w("## 5. Rows with Empty species_name")
w()
if empty_species:
    w("| Row | date | site | observer | notes |")
    w("|-----|------|------|----------|-------|")
    for n, r in empty_species:
        w(f"| {n} | {r['date']} | {r['site']} | {r['observer']} | {r['notes']} |")
else:
    w("None.")
w()
w("---")
w()
w("## 6. Rows with Future Date (after today)")
w()
if future_dates:
    w("| Row | date | site | species_name | observer | notes |")
    w("|-----|------|------|--------------|----------|-------|")
    for n, r in future_dates:
        w(f"| {n} | {r['date']} | {r['site']} | {r['species_name']} | {r['observer']} | {r['notes']} |")
else:
    w("None.")
w()
w("---")
w()
w("## 7. Rows with Empty or Missing substrate")
w()
if empty_substrate:
    w("| Row | date | site | species_name | observer |")
    w("|-----|------|------|--------------|----------|")
    for n, r in empty_substrate:
        w(f"| {n} | {r['date']} | {r['site']} | {r['species_name']} | {r['observer']} |")
else:
    w("None.")
w()
w("---")
w()
w("## 8. Exact Duplicate Rows")
w()
if duplicates:
    for first, second, r in duplicates:
        w(f"Rows {first} and {second} are identical:")
        w()
        w("| Field | Value |")
        w("|-------|-------|")
        for col in REQUIRED_COLUMNS:
            w(f"| {col} | {r[col]} |")
        w()
else:
    w("None.")
w()
w("---")
w()
w("## 9. Species Name Format Issues")
w()
w("Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).")
w()
if species_format_issues:
    w("| Row | species_name | Issue |")
    w("|-----|--------------|-------|")
    for n, r, issue in species_format_issues:
        w(f"| {n} | {r['species_name']} | {issue} |")
else:
    w("None.")
w()
w("---")
w()
w("## 10. Invalid Site Names")
w()
w(f"Known valid sites: {', '.join(f'`{s}`' for s in sorted(VALID_SITES))}")
w()
if invalid_sites:
    w("| Row | site (as recorded) | Issue |")
    w("|-----|--------------------|-------|")
    for n, r in invalid_sites:
        w(f"| {n} | {r['site']} | Does not match a known site |")
else:
    w("None.")
w()
w("---")
w()
w("## 11. Invalid Observer Names")
w()
w(f"Known valid observers: {', '.join(f'`{o}`' for o in sorted(VALID_OBSERVERS))}")
w()
if invalid_observers:
    w("| Row | observer (as recorded) | Issue |")
    w("|-----|------------------------|-------|")
    for n, r in invalid_observers:
        w(f"| {n} | {r['observer']} | Does not match a known observer |")
else:
    w("None.")
w()
w("---")
w()
w("## 12. Flags Summary")
w()
w("| Check | Issues Found |")
w("|-------|-------------|")
w(f"| Missing species_name | {len(empty_species)} row(s) |")
w(f"| Future date | {len(future_dates)} row(s) |")
w(f"| Missing substrate | {len(empty_substrate)} row(s) |")
w(f"| Exact duplicates | {len(duplicates)} pair(s) |")
w(f"| Species name format | {len(species_format_issues)} row(s) |")
w(f"| Invalid site | {len(invalid_sites)} row(s) |")
w(f"| Invalid observer | {len(invalid_observers)} row(s) |")
total_flagged = len({n for n, _ in empty_species}
                  | {n for n, _ in future_dates}
                  | {n for n, _ in empty_substrate}
                  | {n for first, second, _ in duplicates for n in (first, second)}
                  | {n for n, _, __ in species_format_issues}
                  | {n for n, _ in invalid_sites}
                  | {n for n, _ in invalid_observers})
w(f"| **Total flagged rows** | **{total_flagged}** |")

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Report written to {REPORT_PATH}")
