# Fungi Survey Check Report

**File:** data/test_fungi_survey.csv  
**Date of check:** 2026-06-10  
**Agent:** fungi_survey_checker_v1

---

## 1. Column Check

All required columns present: `date`, `site`, `species_name`, `substrate`, `observer`, `notes` ✓

---

## 2. Summary

| Metric | Value |
|--------|-------|
| Total rows (excluding header) | 14 |
| Unique sites (raw) | 4 |
| Unique observers (raw) | 3 |

---

## 3. Unique Sites Found

- Cocha Cashu Trail A
- Los Amigos River Bank
- Pantano Plot 3
- los amigos river bank *(invalid — see Section 10)*

---

## 4. Unique Observers Found

- Celil Acar
- Maria Lopez
- celil acar *(invalid — see Section 11)*

---

## 5. Rows with Empty species_name

| Row | date | site | observer | notes |
|-----|------|------|----------|-------|
| 11 | 2024-08-15 | Cocha Cashu Trail A | Maria Lopez | unknown specimen |

---

## 6. Rows with Future Date (after today)

| Row | date | site | species_name | observer | notes |
|-----|------|------|--------------|----------|-------|
| 12 | 2031-01-01 | Los Amigos River Bank | Amanita muscaria | Celil Acar | future observation |

---

## 7. Rows with Empty or Missing substrate

| Row | date | site | species_name | observer |
|-----|------|------|--------------|----------|
| 13 | 2024-08-15 | Pantano Plot 3 | Boletus edulis | Maria Lopez |

---

## 8. Exact Duplicate Rows

Rows 1 and 14 are identical:

| Field | Value |
|-------|-------|
| date | 2024-08-12 |
| site | Cocha Cashu Trail A |
| species_name | Marasmius rotula |
| substrate | dead hardwood log |
| observer | Celil Acar |
| notes | fruiting bodies clustered |


---

## 9. Species Name Format Issues

Expected format: first word capitalised, second word lowercase (e.g. `Amanita muscaria`).

| Row | species_name | Issue |
|-----|--------------|-------|
| 2 | amanita muscaria | All lowercase |
| 3 | BOLETUS EDULIS | All uppercase |
| 4 | Marasmius | Single word only |

---

## 10. Invalid Site Names

Known valid sites: `Cocha Cashu Trail A`, `Los Amigos River Bank`, `Pantano Plot 3`

| Row | site (as recorded) | Issue |
|-----|--------------------|-------|
| 5 | los amigos river bank | Does not match a known site |

---

## 11. Invalid Observer Names

Known valid observers: `Celil Acar`, `Maria Lopez`

| Row | observer (as recorded) | Issue |
|-----|------------------------|-------|
| 6 | celil acar | Does not match a known observer |

---

## 12. Flags Summary

| Check | Issues Found |
|-------|-------------|
| Missing species_name | 1 row(s) |
| Future date | 1 row(s) |
| Missing substrate | 1 row(s) |
| Exact duplicates | 1 pair(s) |
| Species name format | 3 row(s) |
| Invalid site | 1 row(s) |
| Invalid observer | 1 row(s) |
| **Total flagged rows** | **10** |
