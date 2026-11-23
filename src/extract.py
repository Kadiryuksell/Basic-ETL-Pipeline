import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Ham veride mutlaka bulunması gereken sütunlar
GEREKLI_SUTUNLAR = [
    "order_id",
    "order_date",
    "customer_name",
    "city",
    "product",
    "category",
    "quantity",
    "unit_price",
    "payment_method",
]


def extract(path="data/raw/sales.csv"):
    df = pd.read_csv(path)

    # Beklenen sütunlar yoksa devam etmenin anlamı yok, hemen dur
    eksik = [s for s in GEREKLI_SUTUNLAR if s not in df.columns]
    if eksik:
        raise ValueError(f"CSV'de eksik sütunlar var: {eksik}")

    logger.info("[EXTRACT] Okunan satır sayısı: %d", len(df))
    return df
