# Basic ETL Pipeline
A small, tested ETL pipeline that cleans messy e-commerce sales data with **Python + pandas** and loads it into a **SQLite** database for SQL analysis.

```
data/raw/sales.csv ──▶ extract() ──▶ transform() ──▶ load() ──▶ data/sales.db
                                         │
                                         └──▶ data/processed/sales_clean.csv
```

## What the pipeline does

| Step | File | What it does |
|---|---|---|
| Extract | `src/extract.py` | Reads the raw CSV and checks that all required columns exist |
| Transform | `src/transform.py` | Removes duplicates, normalizes city names, unifies two date formats (`YYYY-MM-DD` / `DD.MM.YYYY`), fills missing prices with the product average, fills missing text, drops invalid quantities, computes `total` |
| Load | `src/load.py` | Writes the clean data to the `sales` table (idempotent: `if_exists="replace"`) |
| Orchestration | `src/pipeline.py` | Runs the steps in order, logs to console and `pipeline.log`, and exits with code 1 on failure |
| Analysis | `src/analysis.py` | Example SQL queries (revenue by category, top products, payment methods, date range) |

Result: 27 raw rows → 24 clean rows.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python src\pipeline.py    # run the ETL
python src\analysis.py    # run SQL analysis
pytest -v                 # run the tests (13 tests)
```

Example log output:

```
2026-11-23 15:11:27 | INFO | === PIPELINE BAŞLADI ===
2026-11-23 15:11:27 | INFO | [EXTRACT] Okunan satır sayısı: 27
2026-11-23 15:11:27 | INFO | [TRANSFORM] Temizlenmiş satır sayısı: 24
2026-11-23 15:11:27 | INFO | [LOAD] Veritabanındaki satır sayısı: 24
2026-11-23 15:11:27 | INFO | === PIPELINE BİTTİ ===
```

## Project structure

```
├── data/raw/sales.csv      raw input (never modified)
├── src/                    pipeline code
├── tests/                  pytest tests for each step
├── pytest.ini
└── requirements.txt
```

## Tech

Python 3.12 · pandas · SQLite · logging · pytest
