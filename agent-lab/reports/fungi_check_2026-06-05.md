# Fungi Survey Check Report

**File:** data/test_fungi_survey.csv  
**Date of check:** 2026-06-05  
**Agent:** fungi_survey_checker_v1

---

## 1. Column Check

All required columns present: `date`, `site`, `species_name`, `substrate`, `observer`, `notes` ✓

---

## 2. Summary

| Metric | Value |
|--------|-------|
| Total rows (excluding header) | 10 |
| Unique sites (raw) | 4 |
| Unique observers (raw) | 2 |

---

## 3. Unique Sites Found

- Cocha Cashu Trail A
- Los Amigos River Bank
- Pantano Plot 3
- pantano plot 3 *(invalid — see Section 10)*

---

## 4. Unique Observers Found

- Celil Acar
- Maria Lopez

---

## 5. Rows with Empty species_name

| Row | date | site | observer | notes |
|-----|------|------|----------|-------|
| 2 | 2024-07-15 | Los Amigos River Bank | Maria Lopez | too small to identify |

---

## 6. Rows with Future Date (after today)

| Row | date | site | species_name | observer | notes |
|-----|------|------|--------------|----------|-------|
| 8 | 2030-05-01 | Cocha Cashu Trail A | Amanita phalloides | Maria Lopez | future observation |

---

## 7. Rows with Empty or Missing substrate

None.

---

## 8. Exact Duplicate Rows

None.

---

## 9. Species Name Format Issues

Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).

| Row | species_name | Issue |
|-----|--------------|-------|
| 3 | hygrocybe conica | All lowercase |
| 5 | Pholiota | Single word only |

---

## 10. Invalid Site Names

Known valid sites: `Cocha Cashu Trail A`, `Los Amigos River Bank`, `Pantano Plot 3`

| Row | site (as recorded) | Issue |
|-----|--------------------|-------|
| 7 | pantano plot 3 | Does not match a known site |

---

## 11. Invalid Observer Names

Known valid observers: `Celil Acar`, `Maria Lopez`

None.

---

## 12. Flags Summary

| Check | Issues Found |
|-------|-------------|
| Missing species_name | 1 row(s) |
| Future date | 1 row(s) |
| Missing substrate | 0 row(s) |
| Exact duplicates | 0 pair(s) |
| Species name format | 2 row(s) |
| Invalid site | 1 row(s) |
| Invalid observer | 0 row(s) |
| **Total flagged rows** | **3** |
