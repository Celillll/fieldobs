"""Match JPG photos to GPS coordinates using GPX track timestamps."""

import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

CAMERA_UTC_OFFSET = -5  # camera is Peru local time; subtract 5 h to get UTC
MAX_TIME_DIFF_S = 7200  # 2 hours

SURVEYS = [
    {
        "name": "Survey 1",
        "photos_dir": PROJECT_DIR / "00_INBOX/photos_unsorted/Survey 1, 12.06.26",
        "gpx_file": PROJECT_DIR / "00_INBOX/tracks/12_Jun_2026_07_20_38.gpx",
    },
    {
        "name": "Survey 2",
        "photos_dir": PROJECT_DIR / "00_INBOX/photos_unsorted/Survey 2, 13.06.26",
        "gpx_file": PROJECT_DIR / "00_INBOX/tracks/13_Jun_2026_09_06_59.gpx",
    },
]

OUTPUT_CSV = PROJECT_DIR / "03_DATA/geotagged_results.csv"

GPX_NS = {"gpx": "http://www.topografix.com/GPX/1/1"}
EXIF_TAG_DATETIME_ORIGINAL = 36867
EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def parse_gpx_trackpoints(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    points = []
    for trkpt in root.findall(".//gpx:trkpt", GPX_NS):
        lat = float(trkpt.get("lat"))
        lon = float(trkpt.get("lon"))
        time_str = trkpt.find("gpx:time", GPX_NS).text
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        points.append((dt, lat, lon))
    points.sort(key=lambda p: p[0])
    return points


def read_exif_datetime(photo_path):
    try:
        img = Image.open(photo_path)
        exif = img._getexif()
        if not exif:
            return None
        raw = exif.get(EXIF_TAG_DATETIME_ORIGINAL)
        if not raw:
            return None
        dt = datetime.strptime(raw, EXIF_DATETIME_FORMAT)
        return dt.replace(tzinfo=timezone(timedelta(hours=CAMERA_UTC_OFFSET)))
    except Exception:
        return None


def find_closest_trackpoint(photo_dt, trackpoints):
    best_point = None
    best_diff = float("inf")
    for pt in trackpoints:
        diff = abs((photo_dt - pt[0]).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_point = pt
    return best_point, best_diff


def process_survey(survey, rows):
    name = survey["name"]
    photos_dir = survey["photos_dir"]
    gpx_file = survey["gpx_file"]

    trackpoints = parse_gpx_trackpoints(gpx_file)
    if not trackpoints:
        print(f"[{name}] No track points found in {gpx_file.name}")
        return

    track_start = trackpoints[0][0]
    track_end = trackpoints[-1][0]
    print(f"[{name}] GPX: {track_start:%Y-%m-%d %H:%M:%S} UTC -> {track_end:%Y-%m-%d %H:%M:%S} UTC  ({len(trackpoints)} points)")

    photos = sorted(p for p in photos_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    print(f"[{name}] Photos found: {len(photos)}")
    print()

    header = f"  {'Filename':<25} {'Lat':>12} {'Lon':>12} {'Diff (s)':>10}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    matched = skipped = 0
    for photo_path in photos:
        photo_dt = read_exif_datetime(photo_path)

        if photo_dt is None:
            print(f"  {photo_path.name:<25} SKIPPED -- no EXIF DateTimeOriginal")
            skipped += 1
            continue

        closest, diff_s = find_closest_trackpoint(photo_dt, trackpoints)

        if diff_s > MAX_TIME_DIFF_S:
            print(f"  {photo_path.name:<25} SKIPPED -- {diff_s:.0f}s outside 2-hour range")
            skipped += 1
            continue

        gpx_dt, lat, lon = closest
        print(f"  {photo_path.name:<25} {lat:>12.7f} {lon:>12.7f} {diff_s:>10.1f}")
        rows.append({
            "filename": photo_path.name,
            "survey": name,
            "lat": round(lat, 7),
            "lon": round(lon, 7),
            "diff_seconds": round(diff_s, 1),
            "photo_time": photo_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "gpx_time": gpx_dt.strftime("%Y-%m-%d %H:%M:%S"),
        })
        matched += 1

    print()
    print(f"  [{name}] Matched: {matched}  |  Skipped: {skipped}")
    print()


def main():
    rows = []
    for survey in SURVEYS:
        process_survey(survey, rows)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["filename", "survey", "lat", "lon", "diff_seconds", "photo_time", "gpx_time"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to {OUTPUT_CSV.relative_to(PROJECT_DIR)}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
