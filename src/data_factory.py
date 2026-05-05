from __future__ import annotations

import csv
import json
from pathlib import Path
from random import Random
from typing import Dict, List


PUBLIC_DATASET_REFERENCE = {
    "primary_reference": {
        "name": "NYC TLC Trip Record Data",
        "url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        "role": "Public trip-duration and mobility data used here as a proxy reference for travel-time prediction patterns.",
    },
    "notes": [
        "The runtime dataset is synthetic and adapted to a last-mile delivery setting.",
        "The project focuses on ETA prediction rather than route optimization.",
    ],
}


def _write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_sample_dataset(base_dir: Path, row_count: int = 1200) -> Dict[str, str]:
    rng = Random(42)
    rows: List[Dict[str, object]] = []
    for index in range(row_count):
        distance_km = round(1.2 + (index % 9) * 0.7 + rng.uniform(0.0, 1.5), 2)
        prep_time_min = round(8 + (index % 6) * 2.4 + rng.uniform(0.0, 4.0), 2)
        courier_wait_min = round(1.5 + (index % 5) * 0.9 + rng.uniform(0.0, 2.0), 2)
        peak_hour = 1 if index % 6 in (0, 1) else 0
        rainy_weather = 1 if index % 8 == 0 else 0
        stacked_order = 1 if index % 7 == 0 else 0

        travel_time_min = (
            5.5
            + (distance_km * 3.1)
            + prep_time_min * 0.45
            + courier_wait_min * 0.9
            + (3.8 if peak_hour else 0.0)
            + (2.6 if rainy_weather else 0.0)
            + (4.1 if stacked_order else 0.0)
            + rng.uniform(-2.5, 2.5)
        )

        rows.append(
            {
                "delivery_id": f"ETA-{index + 1:05d}",
                "distance_km": distance_km,
                "prep_time_min": prep_time_min,
                "courier_wait_min": courier_wait_min,
                "peak_hour": peak_hour,
                "rainy_weather": rainy_weather,
                "stacked_order": stacked_order,
                "actual_eta_min": round(max(12.0, travel_time_min), 2),
            }
        )

    raw_dir = base_dir / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = raw_dir / "last_mile_deliveries.csv"
    reference_path = raw_dir / "public_dataset_reference.json"
    _write_csv(dataset_path, rows)
    reference_path.write_text(json.dumps(PUBLIC_DATASET_REFERENCE, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "dataset_source": "synthetic_last_mile_eta_dataset",
        "dataset_path": str(dataset_path),
        "dataset_reference_path": str(reference_path),
    }
