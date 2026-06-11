# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A training lab for testing Claude agents that validate and summarise fungi survey field data. It is not connected to any real field deployment — `data/` contains only test CSVs.

- Do not place real field data in the `data/` folder.
- Do not mix training files with real research data.

## Running the scripts

```powershell
# Step 1 — validate the survey CSV and produce a per-day check report
python run_fungi_check.py

# Step 2 — aggregate all check reports into a cross-report summary
python run_report_summarizer.py
```

Both scripts write to `reports/` (created automatically) and print one confirmation line. Neither takes CLI arguments. No third-party dependencies — standard library only (`csv`, `os`, `datetime`).

## Architecture

Each agent is defined as a plain-markdown spec in `agents/` and implemented as a standalone Python script in the project root:

| Spec | Script | Reads | Writes |
|------|--------|-------|--------|
| `agents/fungi_survey_checker_v1.md` | `run_fungi_check.py` | `data/test_fungi_survey.csv` | `reports/fungi_check_YYYY-MM-DD.md` |
| `agents/report_summarizer_v1.md` | `run_report_summarizer.py` | `reports/fungi_check_*.md` | `reports/summary_YYYY-MM-DD.md` |

The scripts do **not** call any LLM — they are reference implementations showing what an agent is expected to produce.

## Known issues to fix before real use

- Both scripts use a hardcoded `TODAY = date(2026, 6, 10)` — replace with `date.today()` before production use.
- Valid sites and observers are hardcoded in `run_fungi_check.py` — update these when adding new sites or team members.

## Valid sites and observers

**Sites:** Cocha Cashu Trail A, Los Amigos River Bank, Pantano Plot 3  
**Observers:** Celil Acar, Maria Lopez

## Species name format

`Genus species` — first word capitalised, second word lowercase. Example: `Amanita muscaria`

## Input data

Place a CSV at `data/test_fungi_survey.csv` with columns: `date`, `site`, `species_name`, `substrate`, `observer`, `notes`. The `data/` folder is currently empty (test files are created as needed).
