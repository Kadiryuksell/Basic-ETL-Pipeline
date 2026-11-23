import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform(df):
    # Gelen tabloyu bozmamak için kopyasıyla çalış
    df = df.copy()

    # Tekrar eden satırları sil
    df = df.drop_duplicates()

    # Şehirleri düzelt
    df["city"] = df["city"].str.strip().str.title()
    df["city"] = df["city"].replace({"Izmir": "İzmir"})

    # Tarihleri tek formata çevir
    iso_dates = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    tr_dates = pd.to_datetime(df["order_date"], format="%d.%m.%Y", errors="coerce")
    df["order_date"] = iso_dates.fillna(tr_dates)

    # Hiçbir formata uymayan tarihleri uyarı olarak logla
    bozuk_tarih = df["order_date"].isna().sum()
    if bozuk_tarih > 0:
        logger.warning("[TRANSFORM] Okunamayan tarih sayısı: %d", bozuk_tarih)

    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")

    # Eksik fiyatları aynı ürünün ortalamasıyla doldur
    avg_price = df.groupby("product")["unit_price"].transform("mean")
    df["unit_price"] = df["unit_price"].fillna(avg_price)

    # Eksik metinleri doldur
    df = df.fillna({"city": "Bilinmiyor", "customer_name": "Bilinmiyor"})

    # Mantıksız adetleri ele
    df = df[df["quantity"] > 0].copy()

    # Toplam tutar sütunu ekle
    df["total"] = df["unit_price"] * df["quantity"]

    logger.info("[TRANSFORM] Temizlenmiş satır sayısı: %d", len(df))
    return df
