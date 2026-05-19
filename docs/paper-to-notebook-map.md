# Paper ↔ notebook map

Detailed mapping between figures, tables, and sections of the paper
*Differential Privacy Strategies for Data Analytics in the Banking Sector*
and the notebooks that produce them.

---

## Section-level alignment

| Paper section | Notebook(s) |
|---|---|
| §3.1 Dataset Description | (descriptive; data lives under each `data/raw/`) |
| §3.2 Data Cleaning | `BankMarketing/notebooks/01_data_cleaning.ipynb` |
| §3.3 Exploratory Data Analysis | `BankMarketing/notebooks/02_eda.ipynb` and `FraudDetection/notebooks/02_eda.ipynb` |
| §3.4 Data Preprocessing | `BankMarketing/notebooks/03_data_preprocessing.ipynb` |
| §4.1 Feature Selection (Boruta) | `BankMarketing/notebooks/04_non_private_training.ipynb` (Boruta cells) |
| §4.2 Model Selection and Hyperparameter Tuning | `BankMarketing/notebooks/04_non_private_training.ipynb` and `FraudDetection/notebooks/04_non_private_training.ipynb` (grid-search cells) |
| §4.3 Model Evaluation | `BankMarketing/notebooks/04_non_private_training.ipynb` and `FraudDetection/notebooks/04_non_private_training.ipynb` (evaluation cells) |
| §5.1 Data Preparation for LDP | `BankMarketing/notebooks/05_local_dp_training.ipynb` (`convert_numerics_to_categories`, `map_categorical_columns`) |
| §5.2 Direct Encoding | `BankMarketing/notebooks/05_local_dp_training.ipynb` (`apply_de`); `FraudDetection/notebooks/05_local_dp_training.ipynb` (`apply_de`) |
| §6.1 DP-SGD Neural Network Training | `BankMarketing/notebooks/06_central_dp_training.ipynb` and `FraudDetection/notebooks/06_central_dp_training.ipynb` (`create_model`, `train_model`) |
| §6.2 Experimental Setup | Both CDP notebooks (`grid_search_experiments` cells) |
| §6.3 Non-DP Results and Analysis | Heatmap cell #1 in both CDP notebooks + ANOVA cell |
| §6.4 DP Results and Analysis | Heatmap cells #2–#5 in both CDP notebooks + ANOVA cells |

---

## Figure-level alignment

| Figure | Caption | Notebook | Cell |
|---|---|---|---|
| 1 | Private and non-private analytics workflows | (conceptual diagram; not produced by code) | — |
| 2a | Bank Marketing target distribution | `BankMarketing/notebooks/02_eda.ipynb` | target-distribution `countplot` cell |
| 2b | IPBlock target distribution | `FraudDetection/notebooks/02_eda.ipynb` | target-distribution cell (Figure 2b in paper) |
| 3 | LDP — BankMarketing performance vs ε | `BankMarketing/notebooks/05_local_dp_training.ipynb` | `plot_results_with_whiskers(results_de_stats, ...)` cell |
| 4 | LDP — Fraud performance vs ε | `FraudDetection/notebooks/05_local_dp_training.ipynb` | `plot_from_csv(...)` cell |
| 5 | Non-DP ROC AUC heatmaps — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #1 |
| 6 | Non-DP ROC AUC heatmaps — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #1 |
| 7 | DP-SGD ε heatmaps — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #2 |
| 8 | DP-SGD ε heatmaps — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #2 |
| 9 | DP ROC AUC (batch=16, σ=1.1) — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #3 |
| 10 | DP ROC AUC (batch=16, σ=1.1) — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #3 |
| 11 | DP ROC AUC vs σ at full sample — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #4 |
| 12 | DP ROC AUC vs σ at full sample — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #4 |
| 13 | DP ROC AUC vs σ at 10% sample — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #5 (10% sample loop) |
| 14 | DP ROC AUC vs σ at 10% sample — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #5 |
| 15 | DP ROC AUC vs batch size — BankMarketing | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #6 |
| 16 | DP ROC AUC vs batch size — Fraud | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Heatmap section, panel #6 |

---

## Table-level alignment

| Table | Caption | Notebook | Cell |
|---|---|---|---|
| 1 | Baseline non-private NN evaluation metrics | `BankMarketing/notebooks/04_non_private_training.ipynb` + non-DP rows of `FraudDetection/notebooks/06_central_dp_training.ipynb` | evaluation cells |
| 2 | Non-DP ANOVA (BankMarketing) | `BankMarketing/notebooks/06_central_dp_training.ipynb` | ANOVA cell |
| 3 | DP ANOVA (BankMarketing) | `BankMarketing/notebooks/06_central_dp_training.ipynb` | ANOVA cells |
| A.4 (Appendix) | Boruta-selected features | `BankMarketing/notebooks/04_non_private_training.ipynb` | feature selection cell (`X_filtered`) |

---

## Notes

- Figure 1 is a conceptual diagram and is not produced by code.
- The ANOVA tables in the paper aggregate results over the 10 repeats run
  by the grid search. Tables 2 and 3 in the paper are derived from the
  `results/cdp_aggregated_results.csv` produced by the BankMarketing CDP
  notebook.
- The fraud-dataset ANOVA reported textually in the paper (Section 6.4.5)
  is produced inside the FraudDetection CDP notebook.
