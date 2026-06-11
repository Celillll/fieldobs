import os
import re
import glob
from datetime import date

TODAY = date.today()
REPORT_PATH = f"reports/summary_{TODAY}.md"

RULES = [
    "Missing species",
    "Future date",
    "Missing substrate",
    "Exact duplicates",
    "Species name format",
    "Invalid site",
    "Invalid observer",
]

# ── Find all fungi check reports ─────────────────────────────────────────────
report_files = sorted(glob.glob("reports/fungi_check_*.md"))

if not report_files:
    print("ERROR: No fungi_check_*.md files found in reports/")
    exit(1)

# ── Parse each report ─────────────────────────────────────────────────────────
reports = []

for path in report_files:
    filename = os.path.basename(path)
    # Extract date from filename: fungi_check_2026-06-11.md
    m = re.search(r'fungi_check_(\d{4}-\d{2}-\d{2})\.md', filename)
    report_date = m.group(1) if m else filename

    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Extract total flagged rows
    total_match = re.search(r'\*\*Total flagged rows\*\*\s*\|\s*\*\*(\d+)\*\*', content)
    total_flagged = int(total_match.group(1)) if total_match else 0

    # Extract per-rule counts from Flags Summary table
    rule_counts = {}
    for rule in RULES:
        pattern = re.escape(rule) + r'\s*\|\s*(\d+)'
        m = re.search(pattern, content)
        rule_counts[rule] = int(m.group(1)) if m else 0

    reports.append({
        "date": report_date,
        "filename": filename,
        "total_flagged": total_flagged,
        "rules": rule_counts,
    })

# ── Aggregate across reports ──────────────────────────────────────────────────
rule_totals = {rule: sum(r["rules"].get(rule, 0) for r in reports) for rule in RULES}
rule_fires  = {rule: sum(1 for r in reports if r["rules"].get(rule, 0) > 0) for rule in RULES}
rules_ranked = sorted(rule_totals.items(), key=lambda x: x[1], reverse=True)

# ── Build report ──────────────────────────────────────────────────────────────
os.makedirs("reports", exist_ok=True)

lines = []
def w(s=""): lines.append(s)

w("# Fungi Survey Cross-Report Summary")
w()
w(f"**Generated:** {TODAY}")
w(f"**Agent:** report_summarizer_v1")
w(f"**Reports read:** {len(reports)}")
w()
w("---")
w()
w("## 1. Reports Included")
w()
w("| Report file | Date | Total flagged rows |")
w("|-------------|------|--------------------|")
for r in reports:
    w(f"| {r['filename']} | {r['date']} | {r['total_flagged']} |")
w()
grand_total = sum(r["total_flagged"] for r in reports)
w(f"**Grand total flagged rows across all reports:** {grand_total}")
w()
w("---")
w()
w("## 2. Rules Fired - Ranked by Total Rows Flagged")
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
for rule, _ in rules_ranked:
    row_vals = " | ".join(str(r["rules"].get(rule, 0)) for r in reports)
    w(f"| {rule} | {row_vals} |")
w()
w("---")
w()
w("## 4. Notable Patterns")
w()
top_rule = rules_ranked[0][0] if rules_ranked else "none"
top_count = rules_ranked[0][1] if rules_ranked else 0
top_fires = rule_fires.get(top_rule, 0)
w(f"- **{top_rule}** is the most common issue: {top_count} flagged row(s) across {top_fires} of {len(reports)} report(s).")

persistent = [rule for rule, _ in rules_ranked if rule_fires.get(rule, 0) == len(reports) and len(reports) > 1]
if persistent:
    w(f"- Rules firing in every report: {', '.join(persistent)}.")

zero_rules = [rule for rule, total in rule_totals.items() if total == 0]
if zero_rules:
    w(f"- No issues found for: {', '.join(zero_rules)}.")

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Summary written to {REPORT_PATH}")
