# Fungi Survey Check Report

**File:** data/test_fungi_survey.csv  
**Date of check:** 2026-06-08  
**Agent:** fungi_survey_checker_v1

---

## 1. Column Check

All required columns present: `date`, `site`, `species_name`, `substrate`, `observer`, `notes` ✓

---

## 2. Summary

| Metric | Value |
|--------|-------|
| Total rows (excluding header) | 12 |
| Unique sites (raw) | 3 |
| Unique observers (raw) | 3 |

---

## 3. Unique Sites Found

- Cocha Cashu Trail A
- Los Amigos River Bank
- Pantano Plot 3

---

## 4. Unique Observers Found

- Celil Acar
- Maria Lopez
- maria lopez *(invalid — see Section 11)*

---

## 5. Rows with Empty species_name

| Row | date | site | observer | notes |
|-----|------|------|----------|-------|
| 3 | 2024-09-03 | Los Amigos River Bank | Maria Lopez | unidentified |
| 7 | 2024-09-06 | Pantano Plot 3 | Maria Lopez | too degraded to identify |

---

## 6. Rows with Future Date (after today)

None.

---

## 7. Rows with Empty or Missing substrate

| Row | date | site | species_name | observer |
|-----|------|------|--------------|----------|
| 5 | 2024-09-05 | Cocha Cashu Trail A | Laccaria amethystina | Celil Acar |

---

## 8. Exact Duplicate Rows

Rows 2 and 9 are identical:

| Field | Value |
|-------|-------|
| date | 2024-09-03 |
| site | Cocha Cashu Trail A |
| species_name | Russula emetica |
| substrate | leaf litter |
| observer | Celil Acar |
| notes | bright red cap |

---

## 9. Species Name Format Issues

Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).

| Row | species_name | Issue |
|-----|--------------|-------|
| 4 | CORTINARIUS VIOLACEUS | All uppercase |

---

## 10. Invalid Site Names

Known valid sites: `Cocha Cashu Trail A`, `Los Amigos River Bank`, `Pantano Plot 3`

None.

---

## 11. Invalid Observer Names

Known valid observers: `Celil Acar`, `Maria Lopez`

| Row | observer (as recorded) | Issue |
|-----|------------------------|-------|
| 6 | maria lopez | Does not match a known observer |

---

## 12. Flags Summary

| Check | Issues Found |
|-------|-------------|
| Missing species_name | 2 row(s) |
| Future date | 0 row(s) |
| Missing substrate | 1 row(s) |
| Exact duplicates | 1 pair(s) |
| Species name format | 1 row(s) |
| Invalid site | 0 row(s) |
| Invalid observer | 1 row(s) |
| **Total flagged rows** | **5** |
