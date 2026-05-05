from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

from .data_factory import build_sample_dataset


FEATURES = ["distance_km", "prep_time_min", "courier_wait_min", "peak_hour", "rainy_weather", "stacked_order"]


def _read_rows(path: str) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def _to_xy(rows: List[Dict[str, str]]) -> Tuple[List[List[float]], List[float]]:
    x = [[float(row[feature]) for feature in FEATURES] for row in rows]
    y = [float(row["actual_eta_min"]) for row in rows]
    return x, y


def _split_rows(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    split_index = int(len(rows) * 0.8)
    return rows[:split_index], rows[split_index:]


def _evaluate(name: str, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    abs_errors = [abs(actual - pred) for actual, pred in zip(y_true, y_pred)]
    p90_error = sorted(abs_errors)[int(0.9 * len(abs_errors)) - 1]
    return {
        "name": name,
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "rmse": round(float(mse ** 0.5), 4),
        "p90_abs_error": round(float(p90_error), 4),
    }


def run_analysis(base_dir: Path) -> Dict[str, object]:
    dataset_info = build_sample_dataset(base_dir)
    rows = _read_rows(dataset_info["dataset_path"])
    train_rows, test_rows = _split_rows(rows)
    x_train, y_train = _to_xy(train_rows)
    x_test, y_test = _to_xy(test_rows)

    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)
    linear_pred = list(linear_model.predict(x_test))
    linear_metrics = _evaluate("linear_regression", y_test, linear_pred)

    rf_model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=3)
    rf_model.fit(x_train, y_train)
    rf_pred = list(rf_model.predict(x_test))
    rf_metrics = _evaluate("random_forest_regressor", y_test, rf_pred)

    best_model = linear_metrics if linear_metrics["mae"] <= rf_metrics["mae"] else rf_metrics

    report = {
        "dataset_source": dataset_info["dataset_source"],
        "row_count": len(rows),
        "train_row_count": len(train_rows),
        "test_row_count": len(test_rows),
        "baseline_model": linear_metrics,
        "candidate_model": rf_metrics,
        "best_model": best_model["name"],
        "best_model_mae": best_model["mae"],
        "best_model_rmse": best_model["rmse"],
        "best_model_p90_abs_error": best_model["p90_abs_error"],
    }

    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    report_path = processed_dir / "eta_prediction_report.json"
    report["report_artifact"] = str(report_path)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
