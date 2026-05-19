# Reproducibility protocol

This document complements the top-level [README](../README.md) with a
detailed, step-by-step protocol for reproducing the results published in
the paper *Differential Privacy Strategies for Data Analytics in the
Banking Sector*.

---

## 1. Environment

### 1.1 Operating system

The published results were produced on:

- **OS**: Windows 11 (64-bit, x64)
- **CPU**: Intel Core 7 150U (10 cores / 12 threads, base 1.80 GHz, Meteor Lake-U)
- **RAM**: 16 GB
- **GPU**: Intel integrated graphics — **no discrete GPU; all training ran on CPU**

### 1.2 Python versions

| Environment | Required Python | Reason |
|---|---|---|
| `.venv-cdp` | 3.7.9 | `tensorflow==2.3.0` ships wheels only for 3.5–3.8; `tensorflow-privacy 0.5.1` and `numpy 1.18.5` follow |
| `.venv-ldp` | 3.11 | `tensorflow==2.18.0` + `keras==3.8` |
| `.venv-fdb` | 3.7.9 | `autogluon==0.4.2` and `h2o 3.36` need Python ≤ 3.8 |

### 1.3 Virtual environments

The recommended layout is to put each environment at the repository root,
under a hidden directory (`.venv-cdp/`, `.venv-ldp/`, `.venv-fdb/`). These are gitignored.

```bash
python3.7  -m venv .venv-cdp
python3.11 -m venv .venv-ldp
python3.7  -m venv .venv-fdb
```

For each: activate, upgrade pip, then `pip install -r requirements/<env>.txt`.

---

## 2. Data acquisition

### 2.1 Bank Marketing

Already in `BankMarketing/data/raw/bank-full.csv`
(from the UCI Machine Learning Repository, included with permission under
CC BY 4.0). No additional download required.

### 2.2 IPBlock (fraud)

The IPBlock dataset is hosted on Kaggle and accessed through Amazon's
Fraud Dataset Benchmark library.

Prerequisites:

1. Create a Kaggle account if you do not have one.
2. Generate an API token from your Kaggle account settings; save the
   resulting `kaggle.json` to `~/.kaggle/kaggle.json` (or
   `%USERPROFILE%\.kaggle\kaggle.json` on Windows).
3. Run (from the repository root):

   ```bash
   source .venv-fdb/bin/activate
   python -m src.fdb_export.export_data
   ```

This writes three CSVs to `FraudDetection/data/raw/`:

- `ipblock_train.csv`
- `ipblock_test_features.csv`
- `ipblock_test_labels.csv`

This step needs to be run **once** per machine.

---

## 3. Execution order

Run notebooks top-to-bottom in this order. Cell-by-cell execution is not
required; each notebook can be run end-to-end (e.g., via
`jupyter nbconvert --to notebook --execute`).

| # | Env | Notebook | Approximate runtime |
|---|---|---|---|
| 1 | `.venv-ldp` | `BankMarketing/notebooks/01_data_cleaning.ipynb` | < 1 min |
| 2 | `.venv-ldp` | `BankMarketing/notebooks/02_eda.ipynb` | ~ 2 min |
| 3 | `.venv-ldp` | `BankMarketing/notebooks/03_data_preprocessing.ipynb` | < 1 min |
| 4 | `.venv-ldp` | `BankMarketing/notebooks/04_non_private_training.ipynb` | ~ 3 hrs |
| 5 | `.venv-ldp` | `BankMarketing/notebooks/05_local_dp_training.ipynb` | ~ 4.5 hrs |
| 6 | `.venv-cdp` | `BankMarketing/notebooks/06_central_dp_training.ipynb` | ~ 26 hrs |
| 7 | `.venv-ldp` | `FraudDetection/notebooks/02_eda.ipynb` | ~ 2 min |
| 8 | `.venv-ldp` | `FraudDetection/notebooks/04_non_private_training.ipynb` | ~ 25 min |
| 9 | `.venv-ldp` | `FraudDetection/notebooks/05_local_dp_training.ipynb` | ~ 1 hrs |
| 10 | `.venv-cdp` | `FraudDetection/notebooks/06_central_dp_training.ipynb` |  ~ 22 hrs |

---

## 4. Sources of non-determinism

The artifact has been designed for byte-equivalent reproduction of
intermediate CSVs, but the following sources of variability remain on
training metrics:

- **GPU floating-point non-determinism.** `tf.random.set_seed` does not
  fully constrain reductions on GPU. To force CPU-only execution for
  bitwise reproducibility, set `CUDA_VISIBLE_DEVICES=` before running.
- **Boruta's internal RNG**. BorutaPy seeds its iterations from
  NumPy's global state; if you re-order cells, results may drift.
- **OS-level thread scheduling**. Multi-threaded BLAS can introduce
  reduction-order differences.


### 4.1 Reproducing the published numbers

The CDP notebooks (`06_central_dp_training.ipynb`) pinned
`tf.random.set_seed` in the runs used for the paper, so re-running them
reproduces the values in Tables 2–3 and Figures 5–16 to the precision
shown.

The non-private baselines (`04_non_private_training.ipynb`) and the LDP
notebooks (`05_local_dp_training.ipynb`) did not pin the TensorFlow seed
in their original runs. The versions in this artifact add
`tf.random.set_seed(SEED)`, which makes future re-runs mutually
reproducible but means the network weight initialization now draws from
a different RNG state than the original runs. Absolute values in Table 1
and Figures 3–4 may therefore differ slightly from the paper, 
while qualitative trends across ε reproduce as reported.

---

## 5. Troubleshooting

### `pip install -r requirements/cdp.txt` fails on macOS arm64

`tensorflow==2.3.0` does not have arm64 wheels. Use an x86_64 Python
under Rosetta 2, or run the `.venv-cdp` notebooks inside a Linux container.

### `kaggle.json` permissions warning

```bash
chmod 600 ~/.kaggle/kaggle.json
```

### CUDA out-of-memory in the CDP notebook

Reduce `batch_size` to 16 only and run the heatmap grid in sub-batches.
This does not affect the numeric results — each cell of the heatmap is
computed independently.
