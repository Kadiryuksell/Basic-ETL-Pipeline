import logging
import sqlite3

import pandas as pd

logger = logging.getLogger(__name__)


def load(df, db_path="data/sales.db"):
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql("sales", conn, if_exists="replace", index=False)

        kontrol = pd.read_sql("SELECT COUNT(*) AS satir_sayisi FROM sales", conn)
        satir_sayisi = int(kontrol["satir_sayisi"][0])
        logger.info("[LOAD] Veritabanındaki satır sayısı: %d", satir_sayisi)
    finally:
        # Hata çıksa bile bağlantıyı kapat
        conn.close()

    return satir_sayisi
