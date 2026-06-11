# Agent: Fungi Survey Checker v1

## Goal
Read the file at data/test_fungi_survey.csv and produce a plain-text summary.

## Steps
1. Read the CSV file
2. Check that these columns exist: date, site, species_name, substrate, observer, notes
3. Count the total number of rows (not counting the header)
4. List the unique site names found
5. List the unique observer names found
6. Flag any row where species_name is empty

## Additional Checks
7. Flag any row where the date is in the future (after today's date)
8. Flag any row where substrate is empty or missing
9. Flag any row that is an exact duplicate of another row (all fields identical)
10. Flag any row where species_name does not follow the format: first word capitalized, second word lowercase (e.g. "Amanita muscaria"). Flag if all lowercase, all uppercase, or only one word.
11. Flag any row where site is not an exact match to one of the known sites: "Cocha Cashu Trail A", "Los Amigos River Bank", "Pantano Plot 3". Flag any variation in spelling or capitalization.
12. Flag any row where observer is not an exact match to one of the known observers: "Celil Acar", "Maria Lopez". Flag any variation in spelling or capitalization.

## Output
Write the full report to a file at reports/fungi_check_YYYY-MM-DD.md where YYYY-MM-DD is today's date.
Use markdown formatting in the report.
After writing the file, print one line to the terminal: "Report written to reports/fungi_check_YYYY-MM-DD.md"
Do not print the full report to the terminal.

## Rules
- Read only. Do not modify input data files. Writing to the reports/ folder is permitted.
- If the file does not exist, say so clearly and stop.
- If a required column is missing, name which one and stop.
- Create the reports/ folder if it does not exist.
