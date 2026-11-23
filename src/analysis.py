import sqlite3
import pandas as pd

conn = sqlite3.connect("data/sales.db")

# --- Soru 1: Kategorilere göre toplam ciro ---
sorgu1 = """
select category, sum(total) from sales group by category
"""

print("Kategorilere göre ciro:")
print(pd.read_sql(sorgu1, conn))


# --- Soru 2: En çok adet satan ilk 3 ürün ---
sorgu2 = """
select product, sum(quantity) as toplam_adet from sales group by product order by toplam_adet DESC limit 3
"""

print("En çok adet satan ilk 3 ürün:")
print(pd.read_sql(sorgu2, conn))

# --- Soru 3: Ödeme yöntemlerine göre sipariş sayısı ve toplam ciro ---
sorgu3 = """
select payment_method, count(*) as siparis_sayisi, sum(quantity) as toplam_adet, sum(total) as ciro from sales group by payment_method
"""

print("Ödeme yöntemlerine göre sipariş sayisi ve toplam ciro:")
print(pd.read_sql(sorgu3, conn))

# --- Soru 4: Tarih Hatası ---
sorgu4 = """
SELECT * FROM sales
WHERE order_date BETWEEN '2026-01-05' AND '2026-01-07'
"""

print("5-7 Ocak arasındaki siparişler:")
print(pd.read_sql(sorgu4, conn))

conn.close()