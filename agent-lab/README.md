# Agent Lab - Fungi Survey Pipeline

## What this is
A data quality pipeline for Amazon field surveys.
Not connected to real field data - this is a training and testing space.

## How to use

### Step 1 - Add your CSV
Copy your exported CSV from the field form into the data/ folder.
The script automatically uses the most recently modified CSV.

### Step 2 - Run the checker
    python run_fungi_check.py
Output: reports/fungi_check_YYYY-MM-DD.md

### Step 3 - Run the summarizer
    python run_report_summarizer.py
Output: reports/summary_YYYY-MM-DD.md

## Field form
Live at: https://Celillll.github.io/fieldobs/field_form.html

## Valid sites
- Cocha Cashu Trail A
- Los Amigos River Bank
- Pantano Plot 3

## Valid observers
- Celil Acar
- Maria Lopez

## Files
| File | Purpose |
|------|---------|
| run_fungi_check.py | Validates survey CSV, writes dated report |
| run_report_summarizer.py | Reads all reports, writes cross-survey summary |
| agents/fungi_survey_checker_v1.md | Spec for the checker agent |
| agents/report_summarizer_v1.md | Spec for the summarizer agent |
| data/ | Drop your exported CSVs here |
| reports/ | All generated reports go here |

## Known issues
- Valid sites and observers are hardcoded in run_fungi_check.py
- Update VALID_SITES and VALID_OBSERVERS when adding new sites or team members
