import sqlite3

import pandas as pd
import pytest

from extract import extract
from load import load


def test_extract_gercek_dosyayi_okur():
    df = extract()
    assert len(df) == 27


def test_extract_eksik_sutunda_hata_verir(tmp_path):
    # tmp_path: pytest'in her test için verdiği geçici klasör
    bozuk_csv = tmp_path / "bozuk.csv"
    bozuk_csv.write_text("order_id,city\n1,Ankara\n", encoding="utf-8")

    with pytest.raises(ValueError):
        extract(bozuk_csv)


def test_extract_dosya_yoksa_hata_verir(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract(tmp_path / "olmayan.csv")


def test_load_veriyi_veritabanina_yazar(tmp_path):
    # Gerçek sales.db'ye dokunmamak için geçici bir veritabanı kullan
    test_db = tmp_path / "test.db"
    df = pd.DataFrame({"order_id": [1, 2, 3], "total": [10.0, 20.0, 30.0]})

    satir_sayisi = load(df, db_path=test_db)

    assert satir_sayisi == 3
    conn = sqlite3.connect(test_db)
    toplam = pd.read_sql("SELECT SUM(total) AS t FROM sales", conn)["t"][0]
    conn.close()
    assert toplam == 60.0


def test_load_iki_kez_calisinca_veri_katlanmaz(tmp_path):
    test_db = tmp_path / "test.db"
    df = pd.DataFrame({"order_id": [1, 2, 3]})

    load(df, db_path=test_db)
    satir_sayisi = load(df, db_path=test_db)

    assert satir_sayisi == 3
