"""
Group geotagged photos into observation folders by 2-minute time gaps within each survey.
"""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
CSV_PATH = BASE / "03_DATA" / "geotagged_results.csv"
INBOX = BASE / "00_INBOX" / "photos_unsorted"
OUT_BASE = BASE / "01_SORTED_OBSERVATIONS" / "UNKNOWN"
GAP_THRESHOLD = 120  # seconds


def survey_folder(survey_name: str, date_str: str) -> Path:
    """Map 'Survey 1' + '2026-06-12' -> 'Survey 1, 12.06.26' subfolder."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    suffix = dt.strftime("%d.%m.%y")
    return INBOX / f"{survey_name}, {suffix}"


def load_rows() -> dict[str, list[dict]]:
    """Return rows keyed by survey, sorted by photo_time."""
    surveys: dict[str, list[dict]] = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            row["_dt"] = datetime.strptime(row["photo_time"], "%Y-%m-%d %H:%M:%S")
            surveys.setdefault(row["survey"], []).append(row)
    for rows in surveys.values():
        rows.sort(key=lambda r: r["_dt"])
    return surveys


def split_groups(rows: list[dict]) -> list[list[dict]]:
    """Split a sorted list of rows into groups separated by > GAP_THRESHOLD seconds."""
    groups: list[list[dict]] = []
    current: list[dict] = [rows[0]]
    for prev, cur in zip(rows, rows[1:]):
        gap = (cur["_dt"] - prev["_dt"]).total_seconds()
        if gap > GAP_THRESHOLD:
            groups.append(current)
            current = [cur]
        else:
            current.append(cur)
    groups.append(current)
    return groups


def main() -> None:
    OUT_BASE.mkdir(parents=True, exist_ok=True)
    surveys = load_rows()

    obs_counter = 0
    survey_stats: dict[str, int] = {}
    total_photos = 0

    for survey_name in sorted(surveys):
        rows = surveys[survey_name]
        groups = split_groups(rows)
        survey_stats[survey_name] = len(groups)

        # Derive source folder from survey name + date of first photo
        first_date = rows[0]["_dt"].strftime("%Y-%m-%d")
        src_folder = survey_folder(survey_name, first_date)

        for group in groups:
            obs_counter += 1
            first = group[0]
            obs_date = first["_dt"].strftime("%Y-%m-%d")
            obs_id = f"OBS_{obs_counter:03d}"
            folder_name = f"{obs_id}_{obs_date}"
            obs_dir = OUT_BASE / folder_name
            obs_dir.mkdir(parents=True, exist_ok=True)

            photo_names = []
            for row in group:
                fname = row["filename"]
                src = src_folder / fname
                if src.exists():
                    shutil.copy2(src, obs_dir / fname)
                else:
                    print(f"  WARNING: source not found: {src}")
                photo_names.append(fname)

            metadata = {
                "observation_id": obs_id,
                "date": obs_date,
                "category": "UNKNOWN",
                "species": "unknown",
                "gps_lat": float(first["lat"]),
                "gps_lon": float(first["lon"]),
                "photo_count": len(group),
                "photos": photo_names,
            }
            (obs_dir / "metadata.json").write_text(
                json.dumps(metadata, indent=4), encoding="utf-8"
            )
            total_photos += len(group)

    print("\n=== Observation grouping summary ===")
    for survey_name, count in survey_stats.items():
        print(f"  {survey_name}: {count} groups")
    print(f"  Total groups : {obs_counter}")
    print(f"  Total photos : {total_photos}")


if __name__ == "__main__":
    main()
