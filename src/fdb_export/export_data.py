"""
Export the IPBlock dataset from the Fraud Dataset Benchmark to CSV.

This script downloads the IPBlock dataset from Kaggle via the Fraud Dataset
Benchmark library (Amazon Science) and saves the train and test partitions
to FraudDetection/data/raw/.

Run once, from the .fdb environment, before executing the FraudDetection
notebooks:

    python -m src.fdb_export.export_data

Requirements:
  - A Kaggle account with valid API credentials configured (~/.kaggle/kaggle.json).
  - The .fdb environment installed (see requirements/fdb.txt).
"""

from pathlib import Path

import pandas as pd
from fdb.datasets import FraudDatasetBenchmark


def main():
    # Paths: this file lives at <repo_root>/src/fdb_export/export_data.py,
    # so the repo root is two parents up.
    root_repo = Path(__file__).resolve().parents[2]
    out_dir = root_repo / "FraudDetection" / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Output directory:", out_dir)

    # Download from Kaggle on first run
    print("Loading FraudDatasetBenchmark (first run: download from Kaggle)...")

    obj = FraudDatasetBenchmark(
        key='ipblock',
        load_pre_downloaded=False,
        delete_downloaded=False,
        add_random_values_if_real_na={
            "EVENT_TIMESTAMP": True,
            "LABEL_TIMESTAMP": True,
            "ENTITY_TYPE": True,
            "ENTITY_ID": True,
            "EVENT_ID": True
        }
    )

    # DataFrames
    df_train = obj.train.copy()
    df_test = obj.test.copy()
    df_test_labels = obj.test_labels.copy()

    # Save train
    train_path = out_dir / "ipblock_train.csv"
    df_train.to_csv(train_path, index=False)
    print("Saved:", train_path)

    # Save test features
    test_path = out_dir / "ipblock_test_features.csv"
    df_test.to_csv(test_path, index=False)
    print("Saved:", test_path)

    # Save test labels
    labels_path = out_dir / "ipblock_test_labels.csv"
    df_test_labels.to_csv(labels_path, index=False)
    print("Saved:", labels_path)

    print("\nExport complete. Your dataset is ready in", out_dir)


if __name__ == "__main__":
    main()
