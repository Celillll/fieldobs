"""
Embed GPS coordinates from metadata.json into EXIF tags of JPG photos
in each observation folder under 01_SORTED_OBSERVATIONS/UNKNOWN/.
Skips photos that already carry GPS EXIF data.
"""

import json
from pathlib import Path

import piexif

BASE = Path(__file__).parent.parent
UNKNOWN_DIR = BASE / "01_SORTED_OBSERVATIONS" / "UNKNOWN"


def decimal_to_dms_rational(degrees: float) -> tuple:
    """Convert decimal degrees to ((d,1),(m,1),(s*100,100)) EXIF rational tuples."""
    degrees = abs(degrees)
    d = int(degrees)
    minutes_float = (degrees - d) * 60
    m = int(minutes_float)
    s = round((minutes_float - m) * 60 * 100)
    return ((d, 1), (m, 1), (s, 100))


def has_gps_data(exif_dict: dict) -> bool:
    gps = exif_dict.get("GPS", {})
    # Tag 1 = GPSLatitudeRef, tag 2 = GPSLatitude
    return bool(gps.get(piexif.GPSIFD.GPSLatitude))


def main() -> None:
    obs_dirs = sorted(d for d in UNKNOWN_DIR.iterdir() if d.is_dir())
    if not obs_dirs:
        print("No observation folders found.")
        return

    total_tagged = 0
    total_skipped = 0

    for obs_dir in obs_dirs:
        metadata_path = obs_dir / "metadata.json"
        if not metadata_path.exists():
            print(f"\n{obs_dir.name}: no metadata.json, skipping folder")
            continue

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        lat = metadata.get("gps_lat")
        lon = metadata.get("gps_lon")
        if lat is None or lon is None:
            print(f"\n{obs_dir.name}: no GPS coords in metadata, skipping folder")
            continue

        jpgs = sorted(p for p in obs_dir.iterdir() if p.suffix.lower() == ".jpg")
        if not jpgs:
            continue

        print(f"\n{obs_dir.name}  [{lat:.6f}, {lon:.6f}]  ({len(jpgs)} photos)")
        for jpg in jpgs:
            try:
                exif_dict = piexif.load(str(jpg))
            except Exception:
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

            if has_gps_data(exif_dict):
                print(f"  SKIP (GPS exists) : {jpg.name}")
                total_skipped += 1
                continue

            exif_dict["GPS"] = {
                piexif.GPSIFD.GPSLatitudeRef:  b"N" if lat >= 0 else b"S",
                piexif.GPSIFD.GPSLatitude:     decimal_to_dms_rational(lat),
                piexif.GPSIFD.GPSLongitudeRef: b"E" if lon >= 0 else b"W",
                piexif.GPSIFD.GPSLongitude:    decimal_to_dms_rational(lon),
            }
            piexif.insert(piexif.dump(exif_dict), str(jpg))
            print(f"  tagged            : {jpg.name}  ({lat:.6f}, {lon:.6f})")
            total_tagged += 1

    print(f"\n=== Summary ===")
    print(f"  Folders processed : {len(obs_dirs)}")
    print(f"  Photos tagged     : {total_tagged}")
    print(f"  Photos skipped    : {total_skipped}")


if __name__ == "__main__":
    main()
