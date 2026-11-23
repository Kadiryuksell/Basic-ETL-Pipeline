import logging
import os
import sys

from extract import extract
from transform import transform
from load import load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def main():
    logging.info("=== PIPELINE BAŞLADI ===")

    try:
        ham_veri = extract()
        temiz_veri = transform(ham_veri)

        # Temiz veriyi ara kayıt olarak sakla (klasör yoksa oluştur)
        os.makedirs("data/processed", exist_ok=True)
        temiz_veri.to_csv("data/processed/sales_clean.csv", index=False)

        load(temiz_veri)
    except Exception:
        # logging.exception: hata mesajını + hatanın hangi satırda olduğunu yazar
        logging.exception("=== PIPELINE HATA İLE DURDU ===")
        sys.exit(1)

    logging.info("=== PIPELINE BİTTİ ===")


# Bu dosya doğrudan çalıştırılırsa main() çalışsın,
# başka bir dosyadan import edilirse çalışmasın
if __name__ == "__main__":
    main()
