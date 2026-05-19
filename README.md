# Differential Privacy Strategies for Data Analytics in the Banking Sector

Reproducible artifact for the paper:

> **Espinosa, D., Pérez, J. F., & Gauthier-Umaña, V.**
> *Differential Privacy Strategies for Data Analytics in the Banking Sector.*
> Information Sciences, 2026. DOI: `<TODO>`

This repository implements two privacy-preserving workflows on two
banking-related datasets:

| Workflow | Mechanism | Where noise is added | Paper section |
|---|---|---|---|
| Private-data | **Local Differential Privacy (LDP)** via Direct Encoding | At the user level, before collection | §5 |
| Private-model | **Central Differential Privacy (CDP)** via DP-SGD | During model training, by a trusted curator | §6 |

It applies both workflows to (i) the **Bank Marketing** dataset (UCI) and
(ii) the **IPBlock** subset of the Amazon Fraud Dataset Benchmark, and
compares them against non-private baselines.

---

## Table of contents

- [Repository layout](#repository-layout)
- [Paper → notebook map](#paper--notebook-map)
- [Environments: why three?](#environments-why-three)
- [Quickstart](#quickstart)
- [Execution order](#execution-order)
- [Reproducibility](#reproducibility)
- [Data sources and licensing](#data-sources-and-licensing)
- [Citation](#citation)
- [License](#license)

---

## Repository layout

```
differential-privacy-data-analysis/
├── LICENSE                              MIT
├── CITATION.cff                         Citation metadata
├── README.md                            This file
├── .gitignore
│
├── requirements/                        One pinned requirements file per environment
│   ├── cdp.txt                          Central DP (TensorFlow 2.3 + tensorflow-privacy)
│   ├── ldp.txt                          Local DP   (TensorFlow 2.18 + pure-ldp)
│   └── fdb.txt                          Data export (Amazon FDB)
│
├── docs/
│   ├── reproducibility.md               Step-by-step protocol
│   └── paper-to-notebook-map.md         Maps paper figures/tables to notebooks
│
├── src/
│   └── fdb_export/
│       ├── __init__.py
│       └── export_data.py               One-shot IPBlock exporter (uses Amazon FDB)
│
├── BankMarketing/
│   ├── data/
│   │   ├── raw/                         Original UCI files (tracked)
│   │   │   ├── bank-full.csv
│   │   │   └── bank-names.txt
│   │   └── processed/                   Intermediate artifacts (untracked, regenerated)
│   │       ├── bank-cleaned.csv         ← produced by 01
│   │       └── bank-processed.csv       ← produced by 03
│   ├── notebooks/
│   │   ├── 01_data_cleaning.ipynb       §3.2 Data Cleaning
│   │   ├── 02_eda.ipynb                 §3.3 Exploratory Data Analysis
│   │   ├── 03_data_preprocessing.ipynb  §3.4 Data Preprocessing
│   │   ├── 04_non_private_training.ipynb   §4 Non-private baseline
│   │   ├── 05_local_dp_training.ipynb      §5 Private-data workflow (LDP)
│   │   └── 06_central_dp_training.ipynb    §6 Private-model workflow (CDP)
│   ├── figures/                         Generated plots (untracked)
│   └── results/                         Generated CSVs (untracked)
│
└── FraudDetection/
    ├── data/
    │   └── raw/                         IPBlock CSVs (produced by src/fdb_export)
    ├── notebooks/
    │   ├── 02_eda.ipynb                     §3.3 Exploratory Data Analysis (IPBlock)
    │   ├── 04_non_private_training.ipynb    §4 Non-private baseline (Fraud)
    │   ├── 05_local_dp_training.ipynb       §5 applied to fraud detection
    │   └── 06_central_dp_training.ipynb     §6 applied to fraud detection
    ├── figures/                         Generated plots (untracked)
    └── results/                         Generated CSVs (untracked)
```

Numbered notebook prefixes (`01_…`, `02_…`, …) follow the paper's order
and the execution dependency chain. The FraudDetection folder has no
`01_`–`03_` notebooks because the IPBlock data ships pre-cleaned and
pre-split, so the data-cleaning and preprocessing steps
do not apply to it.

---

## Paper → notebook map

See [`docs/paper-to-notebook-map.md`](docs/paper-to-notebook-map.md) for
the full mapping between paper figures/tables/sections and the notebook
cells that produce them.

---

## Environments: why three?

The notebooks span two TensorFlow major versions and cannot be collapsed
into a single environment without breaking reproducibility:

| Env name | Python | TensorFlow | Key extras | Used by |
|---|---|---|---|---|
| `.venv-cdp` | **3.7.9** | 2.3.0 | tensorflow-privacy 0.5.1 (pins old NumPy/sklearn) | `06_central_dp_training.ipynb` (both datasets) |
| `.venv-ldp` | **3.10 or 3.11** | 2.18.0 | Keras 3.8, pure-ldp 1.2 | `04_*`, `05_*` (both datasets) |
| `.venv-fdb` | **3.7.9** | — | autogluon 0.4.2 + h2o (Amazon FDB deps) | `src/fdb_export/export_data.py` (one-shot) |

Notebooks `01_`, `02_`, `03_` (BankMarketing only — pure pandas/sklearn)
run in **any** of the three environments; we recommend `.venv-ldp`.

---

## Quickstart

### 1. Clone

```bash
git clone https://github.com/despinosaa/differential-privacy-data-analysis.git
cd differential-privacy-data-analysis
```

### 2. Build the three virtual environments

Repeat for each environment — match the Python version to the table above:

```bash
python3.<VERSION> -m venv .venv-<ENV>
source .venv-<ENV>/bin/activate           # Windows: .venv-<ENV>\Scripts\activate
pip install --upgrade pip
pip install -r requirements/<ENV>.txt
deactivate
```

### 3. Obtain the IPBlock dataset (one-shot)

You will need a [Kaggle](https://www.kaggle.com) account and a
`~/.kaggle/kaggle.json` API token. Then:

```bash
source .venv-fdb/bin/activate
python -m src.fdb_export.export_data
```

This downloads the IPBlock dataset and writes
`ipblock_train.csv`, `ipblock_test_features.csv`, and
`ipblock_test_labels.csv` to `FraudDetection/data/raw/`.

The Bank Marketing dataset is already included in
`BankMarketing/data/raw/` and does not require download.

---

## Execution order
| # | Env | Notebook | Produces |
|---|---|---|---|
| 0 | `.venv-fdb` | `python -m src.fdb_export.export_data` | `FraudDetection/data/raw/ipblock_*.csv` (run once) |
| 1 | `.venv-ldp` | `BankMarketing/notebooks/01_data_cleaning.ipynb` | `BankMarketing/data/processed/bank-cleaned.csv` |
| 2 | `.venv-ldp` | `BankMarketing/notebooks/02_eda.ipynb` | Figure 2a + EDA plots |
| 3 | `.venv-ldp` | `BankMarketing/notebooks/03_data_preprocessing.ipynb` | `BankMarketing/data/processed/bank-processed.csv` |
| 4 | `.venv-ldp` | `BankMarketing/notebooks/04_non_private_training.ipynb` | Non-private baseline (BankMarketing row of Table 1) |
| 5 | `.venv-ldp` | `BankMarketing/notebooks/05_local_dp_training.ipynb` | Figure 3, LDP results CSV |
| 6 | `.venv-cdp` | `BankMarketing/notebooks/06_central_dp_training.ipynb` | Figures 5, 7, 9, 11, 13, 15; Tables 2–3 |
| 7 | `.venv-ldp` | `FraudDetection/notebooks/02_eda.ipynb` | Figure 2b + complementary EDA plots |
| 8 | `.venv-ldp` | `FraudDetection/notebooks/04_non_private_training.ipynb` | Non-private baseline (Fraud row of Table 1) |
| 9 | `.venv-ldp` | `FraudDetection/notebooks/05_local_dp_training.ipynb` | Figure 4 |
| 10 | `.venv-cdp` | `FraudDetection/notebooks/06_central_dp_training.ipynb` | Figures 6, 8, 10, 12, 14, 16 |

---

## Reproducibility

Full step-by-step protocol, dependency versions, and sources of
non-determinism are documented in
[`docs/reproducibility.md`](docs/reproducibility.md).

Published numbers were produced on an Intel Core 7 150U laptop
(CPU-only, 16 GB RAM, Windows 11). The CDP grid searches take ~20–26 h
per dataset on this hardware; a machine with a CUDA GPU will be
substantially faster.

---

## Data sources and licensing

| Dataset | Source | License | Citation |
|---|---|---|---|
| Bank Marketing | UCI Machine Learning Repository | CC BY 4.0 | Moro, Cortez, and Rita (2014) |
| IPBlock (fraud) | Amazon Fraud Dataset Benchmark | MIT (loader); per-source for raw data | Grover et al. (2022); obtained via Kaggle |

The Amazon Fraud Dataset Benchmark library is fetched at install time from
the upstream repository (pinned to commit `f100cb8`) — see
`requirements/fdb.txt`. No modifications to the upstream library are
required; only our custom export script (`src/fdb_export/export_data.py`)
is provided here.

---

## Citation

If you use this artifact, please cite the paper:

```bibtex
@article{espinosa2026dpbanking,
  title   = {Differential Privacy Strategies for Data Analytics in the Banking Sector},
  author  = {Espinosa, Daniela and P{\'e}rez, Juan F. and Gauthier-Uma{\~n}a, Val{\'e}rie},
  journal = {Information Sciences},
  year    = {2026},
  doi     = {<TODO>}
}
```

GitHub also reads `CITATION.cff` to display a "Cite this repository" button
on the repo home page.

---

## License

This code is released under the **MIT License** — see [`LICENSE`](LICENSE).
The included datasets are subject to their own licenses (see above).

---

## Acknowledgments

`<TODO: funding/institutional support>`.
