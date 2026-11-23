import pandas as pd

from transform import transform


def ornek_veri():
    # Her testte kullanılacak küçük, bilerek "kirli" bir tablo
    return pd.DataFrame(
        {
            "order_id": [1, 1, 2, 3, 4],
            "order_date": ["2026-01-05", "2026-01-05", "06.01.2026", "2026-01-07", "2026-01-08"],
            "customer_name": ["Ayşe", "Ayşe", None, "Can", "Elif"],
            "city": ["  ankara ", "  ankara ", "izmir", None, "İstanbul"],
            "product": ["Klavye", "Klavye", "Klavye", "Mouse", "Mouse"],
            "category": ["Elektronik"] * 5,
            "unit_price": [100.0, 100.0, None, 50.0, 50.0],
            "quantity": [2, 2, 1, 3, -1],
            "payment_method": ["Havale"] * 5,
        }
    )


def test_tekrar_eden_satirlar_silinir():
    sonuc = transform(ornek_veri())
    assert sonuc["order_id"].is_unique


def test_negatif_adetler_elenir():
    sonuc = transform(ornek_veri())
    assert (sonuc["quantity"] > 0).all()
    assert 4 not in sonuc["order_id"].values


def test_tarihler_tek_formata_cevrilir():
    sonuc = transform(ornek_veri())
    assert list(sonuc["order_date"]) == ["2026-01-05", "2026-01-06", "2026-01-07"]


def test_sehirler_duzeltilir():
    sonuc = transform(ornek_veri())
    assert list(sonuc["city"]) == ["Ankara", "İzmir", "Bilinmiyor"]


def test_eksik_fiyat_urun_ortalamasiyla_doldurulur():
    sonuc = transform(ornek_veri())
    klavye_2 = sonuc[sonuc["order_id"] == 2]
    assert klavye_2["unit_price"].iloc[0] == 100.0


def test_eksik_musteri_adi_doldurulur():
    sonuc = transform(ornek_veri())
    assert sonuc["customer_name"].notna().all()


def test_total_dogru_hesaplanir():
    sonuc = transform(ornek_veri())
    assert (sonuc["total"] == sonuc["unit_price"] * sonuc["quantity"]).all()


def test_girdi_tablosu_degismez():
    girdi = ornek_veri()
    transform(girdi)
    assert len(girdi) == 5
    assert "total" not in girdi.columns
