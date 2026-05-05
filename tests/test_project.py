from __future__ import annotations

import unittest
from pathlib import Path

from src.data_factory import build_sample_dataset
from src.modeling import run_analysis


class EtaPredictionLastMileTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]

    def test_dataset_factory_creates_files(self) -> None:
        dataset_info = build_sample_dataset(self.base_dir)
        self.assertEqual(dataset_info["dataset_source"], "synthetic_last_mile_eta_dataset")
        self.assertTrue(Path(dataset_info["dataset_path"]).exists())
        self.assertTrue(Path(dataset_info["dataset_reference_path"]).exists())

    def test_analysis_contract(self) -> None:
        report = run_analysis(self.base_dir)
        self.assertEqual(report["dataset_source"], "synthetic_last_mile_eta_dataset")
        self.assertEqual(report["row_count"], 1200)
        self.assertEqual(report["train_row_count"], 960)
        self.assertEqual(report["test_row_count"], 240)
        self.assertIn(report["best_model"], {"linear_regression", "random_forest_regressor"})
        self.assertTrue(Path(report["report_artifact"]).exists())

    def test_best_model_has_reasonable_mae(self) -> None:
        report = run_analysis(self.base_dir)
        self.assertLess(report["best_model_mae"], 5.0)


if __name__ == "__main__":
    unittest.main()
