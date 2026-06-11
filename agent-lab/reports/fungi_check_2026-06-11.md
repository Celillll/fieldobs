# Fungi Survey Check Report

**File:** data/test_fungi_survey.csv  
**Date of check:** 2026-06-11  
**Agent:** fungi_survey_checker_v1

---

## 1. Column Check

All required columns present. ✓

---

## 2. Summary

| Metric | Value |
|--------|-------|
| Total rows (excluding header) | 1 |
| Unique sites (raw) | 1 |
| Unique observers (raw) | 1 |

---

## 3. Unique Sites Found

- lln *(invalid - see Section 10)*

---

## 4. Unique Observers Found

- jknln *(invalid - see Section 11)*

---

## 5. Rows with Empty species

| Row | timestamp | site | observer | notes |
|-----|-----------|------|----------|-------|
| 1 | 2026-06-11T16:23:06 | lln | jknln |  |

---

## 6. Rows with Future Date (after today)

None.

---

## 7. Rows with Empty or Missing substrate

| Row | timestamp | site | species | observer |
|-----|-----------|------|---------|----------|
| 1 | 2026-06-11T16:23:06 | lln |  | jknln |

---

## 8. Exact Duplicate Rows

None.

---

## 9. Species Name Format Issues

Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).

None.

---

## 10. Invalid Site Names

Known valid sites: `Cocha Cashu Trail A`, `Los Amigos River Bank`, `Pantano Plot 3`

| Row | site (as recorded) | Issue |
|-----|--------------------|-------|
| 1 | lln | Does not match a known site |

---

## 11. Invalid Observer Names

Known valid observers: `Celil Acar`, `Maria Lopez`

| Row | observer (as recorded) | Issue |
|-----|------------------------|-------|
| 1 | jknln | Does not match a known observer |

---

## 12. Flags Summary

| Check | Issues Found |
|-------|-------------|
| Missing species | 1 row(s) |
| Future date | 0 row(s) |
| Missing substrate | 1 row(s) |
| Exact duplicates | 0 pair(s) |
| Species name format | 0 row(s) |
| Invalid site | 1 row(s) |
| Invalid observer | 1 row(s) |
| **Total flagged rows** | **1** |
