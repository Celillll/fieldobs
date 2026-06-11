# Fungi Survey Check Report

**File:** data\field_test_observations.csv  
**Date of check:** 2026-06-11  
**Agent:** fungi_survey_checker_v1

---

## 1. Column Check

All required columns present. âœ“

---

## 2. Summary

| Metric | Value |
|--------|-------|
| Total rows (excluding header) | 15 |
| Unique sites (raw) | 2 |
| Unique observers (raw) | 1 |

---

## 3. Unique Sites Found

- Cocha Cashu Trail A
- Los amigos river bank *(invalid - see Section 10)*

---

## 4. Unique Observers Found

- Celil Acar

---

## 5. Rows with Empty species

| Row | timestamp | site | observer | notes |
|-----|-----------|------|----------|-------|
| 13 | 2026-06-11T11:38:00 | Cocha Cashu Trail A | Celil Acar | Unknown herb |

---

## 6. Rows with Future Date (after today)

None.

---

## 7. Rows with Empty or Missing substrate

| Row | timestamp | site | species | observer |
|-----|-----------|------|---------|----------|
| 3 | 2026-06-11T08:45:00 | Cocha Cashu Trail A | Heliconia bihai | Celil Acar |
| 6 | 2026-06-11T09:35:00 | Cocha Cashu Trail A | Cecropia peltata | Celil Acar |
| 13 | 2026-06-11T11:38:00 | Cocha Cashu Trail A |  | Celil Acar |
| 14 | 2026-06-11T11:55:00 | Cocha Cashu Trail A | Lentinus tigrinus | Celil Acar |

---

## 8. Exact Duplicate Rows

None.

---

## 9. Species Name Format Issues

Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).

| Row | species | Issue |
|-----|---------|-------|
| 11 | amanita muscaria | All lowercase |

---

## 10. Invalid Site Names

Known valid sites: `Cocha Cashu Trail A`, `Los Amigos River Bank`, `Pantano Plot 3`

| Row | site (as recorded) | Issue |
|-----|--------------------|-------|
| 12 | Los amigos river bank | Does not match a known site |

---

## 11. Invalid Observer Names

Known valid observers: `Celil Acar`, `Maria Lopez`

None.

---

## 12. Flags Summary

| Check | Issues Found |
|-------|-------------|
| Missing species | 1 row(s) |
| Future date | 0 row(s) |
| Missing substrate | 4 row(s) |
| Exact duplicates | 0 pair(s) |
| Species name format | 1 row(s) |
| Invalid site | 1 row(s) |
| Invalid observer | 0 row(s) |
| **Total flagged rows** | **6** |
