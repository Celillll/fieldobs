# Agent: Report Summarizer v1

## Goal
Read all markdown report files in the reports/ folder and produce a cross-report summary.

## Steps
1. List all files matching reports/fungi_check_*.md
2. For each file, extract:
   - The report date
   - Total flagged rows
   - Which rules fired and how many rows each rule flagged
3. Across all reports, count:
   - Total reports read
   - Which rules fired most often (ranked)
   - Which sites appear most in flags
   - Which observers appear most in flags
4. Write the summary to reports/summary_YYYY-MM-DD.md using today's date

## Output
Write the summary to reports/summary_YYYY-MM-DD.md
Print one terminal line: "Summary written to reports/summary_YYYY-MM-DD.md"
Do not print the full summary to the terminal.

## Rules
- Read only. Do not modify any input or report files.
- Writing to the reports/ folder is permitted.
- If no report files are found, say so clearly and stop.
