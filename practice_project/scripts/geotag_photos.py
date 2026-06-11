"""Match JPG photos to GPS coordinates using GPX track timestamps."""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
GPX_FILE = PROJECT_DIR / "00_INBOX/tracks/17_May_2026_12_53_06.gpx"
PHOTOS_DIR = PROJECT_DIR / "00_INBOX/photos_unsorted"
OBSERVATIONS_DIR = PROJECT_DIR / "01_SORTED_OBSERVATIONS"
CAMERA_UTC_OFFSET = 0  # hours — camera clock is UTC
MAX_TIME_DIFF_S = 7200  # 2 hours

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


def build_observation_index(observations_dir):
    """Return {filename: metadata.json path} for every observation folder."""
    index = {}
    for metadata_path in observations_dir.rglob("metadata.json"):
        folder = metadata_path.parent
        for f in folder.iterdir():
            if f.suffix.lower() in (".jpg", ".jpeg"):
                index[f.name] = metadata_path
    return index


def write_gps_to_metadata(metadata_path, lat, lon):
    with open(metadata_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    data["gps_lat"] = round(lat, 7)
    data["gps_lon"] = round(lon, 7)
    with open(metadata_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=4)


def find_closest_trackpoint(photo_dt, trackpoints):
    best_point = None
    best_diff = float("inf")
    for pt in trackpoints:
        diff = abs((photo_dt - pt[0]).total_seconds())
        if diff < best_diff:
            best_diff = diff
            best_point = pt
    return best_point, best_diff


def main():
    trackpoints = parse_gpx_trackpoints(GPX_FILE)
    if not trackpoints:
        print("No track points found in GPX file.")
        return

    track_start = trackpoints[0][0]
    track_end = trackpoints[-1][0]
    print(f"GPX track: {track_start:%Y-%m-%d %H:%M:%S} UTC -> {track_end:%Y-%m-%d %H:%M:%S} UTC")
    print(f"Track points loaded: {len(trackpoints)}")
    print()

    obs_index = build_observation_index(OBSERVATIONS_DIR)

    photos = sorted(
        p for p in PHOTOS_DIR.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")
    )
    print(f"Photos found: {len(photos)}")
    print()

    header = f"{'Filename':<30} {'Lat':>12} {'Lon':>12} {'Diff (s)':>10}"
    print(header)
    print("-" * len(header))

    matched = 0
    skipped = 0

    for photo_path in photos:
        photo_dt = read_exif_datetime(photo_path)

        if photo_dt is None:
            print(f"{photo_path.name:<30} SKIPPED -- no EXIF DateTimeOriginal")
            skipped += 1
            continue

        closest, diff_s = find_closest_trackpoint(photo_dt, trackpoints)

        if diff_s > MAX_TIME_DIFF_S:
            print(f"{photo_path.name:<30} SKIPPED -- {diff_s:.0f}s outside 2-hour track range")
            skipped += 1
            continue

        _, lat, lon = closest
        metadata_path = obs_index.get(photo_path.name)
        if metadata_path:
            write_gps_to_metadata(metadata_path, lat, lon)
            written = f"  -> wrote {metadata_path.relative_to(PROJECT_DIR)}"
        else:
            written = "  -> no observation folder found"
        print(f"{photo_path.name:<30} {lat:>12.7f} {lon:>12.7f} {diff_s:>10.1f}{written}")
        matched += 1

    print()
    print(f"Matched: {matched}  |  Skipped: {skipped}")


if __name__ == "__main__":
    main()
