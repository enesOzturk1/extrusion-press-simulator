import psycopg2
from datetime import datetime, timedelta
import random
import math
import time

# TimescaleDB/PostgreSQL bağlantı ayarları
conn = psycopg2.connect(
    dbname="tsdb",
    user="tsdbuser",
    password="tsdbpass",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Tabloyu baştan oluştur (geliştirme/test için)
cur.execute("DROP TABLE IF EXISTS presdata;")
cur.execute("""
CREATE TABLE presdata (
    id SERIAL,
    zaman TIMESTAMPTZ NOT NULL,
    siparis_no TEXT,
    kalip_no TEXT,
    alasim TEXT,
    billet_boyu INT,
    billet_kg FLOAT,
    profil_gramaj FLOAT,
    profil_boyu FLOAT,
    profil_adedi INT,
    brut_uretim FLOAT,
    fire FLOAT,
    net_uretim FLOAT,
    kalan_adet INT,
    kalan_kg FLOAT,
    kalan_billet INT,
    billet_sayisi INT,
    operator TEXT,
    vardiya INT,
    olay_tipi TEXT,
    olay_mesaji TEXT
);
""")
cur.execute("SELECT create_hypertable('presdata', 'zaman', if_not_exists => TRUE);")
conn.commit()

# Simülasyon parametreleri
billet_boylari = {"6082": 1400, "6063": 1500, "606090": 1450}
pres_cap = 610  # mm

def billet_kg(cap_mm, length_mm, density=2.7):
    r_cm = (cap_mm / 2) / 10
    l_cm = length_mm / 10
    volume_cm3 = math.pi * r_cm**2 * l_cm
    kg = (volume_cm3 * density) / 1000
    return round(kg, 1)

kaliplar = {
    "11933-25": 1.10,
    "4536-28": 0.97,
    "7850-27": 1.04,
    "3415-19": 0.89,
    "2644-11": 1.25,
    "5632-21": 1.06,
    "2256-14": 0.95,
    "9001-35": 1.02,
    "10654-15": 1.13,
    "4235-07": 0.91,
    "7721-29": 1.17,
    "3478-33": 1.04,
    "6912-30": 1.15,
    "8211-22": 1.08,
    "6589-18": 1.22
}
alasimlar = list(billet_boylari.keys())
kalip_listesi = list(kaliplar.keys())

# Siparişleri oluştur
siparisler = {}
for i in range(1, 21):  # 20 sipariş
    sip_no = f"SP{i:03}"
    kalip = random.choice(kalip_listesi)
    alasim = random.choice(alasimlar)
    profil_gramaj = kaliplar[kalip]
    hedef_adet = random.randint(3000, 5000)
    profil_boyu = round(random.uniform(10, 16), 2)
    hedef_kg = round(profil_gramaj * profil_boyu * hedef_adet, 1)
    boy = billet_boylari[alasim]
    billetkg = billet_kg(pres_cap, boy)
    billet_sayisi = math.ceil(hedef_kg / billetkg)
    siparisler[sip_no] = {
        "kalip": kalip,
        "alasim": alasim,
        "profil_gramaj": profil_gramaj,
        "profil_boyu": profil_boyu,
        "hedef_adet": hedef_adet,
        "hedef_kg": hedef_kg,
        "kalan_adet": hedef_adet,
        "kalan_kg": hedef_kg,
        "billetkg": billetkg,
        "billet_boyu": boy,
        "billet_sayisi": billet_sayisi,
        "kalan_billet": billet_sayisi
    }

siparis_sirasi = list(siparisler.keys())
sip_idx = 0

operators = ["Ahmet", "Mehmet", "Esra", "Murat"]
vardiyalar = [1, 2, 3]

while True:
    tamamlanmayan = [s for s in siparisler.values() if s["kalan_adet"] > 0 and s["kalan_kg"] > 0 and s["kalan_billet"] > 0]
    if not tamamlanmayan:
        print("Tüm siparişler tamamlandı! Simülasyon bitiyor.")
        break

    if sip_idx >= len(siparis_sirasi):
        sip_idx = 0
    sip_no = siparis_sirasi[sip_idx]
    sp = siparisler[sip_no]

    if sp["kalan_adet"] <= 0 or sp["kalan_kg"] <= 0 or sp["kalan_billet"] <= 0:
        print(f"Sipariş {sip_no} tamamlandı! Sonraki siparişe geçiliyor.")
        sip_idx += 1
        continue

    alasim = sp["alasim"]
    boy = sp["billet_boyu"]
    billetkg = sp["billetkg"]
    kalan_adet = sp["kalan_adet"]

    cikan_profil_adedi = int(billetkg // (sp["profil_gramaj"] * sp["profil_boyu"]))
    if cikan_profil_adedi == 0:
        cikan_profil_adedi = 1
    if cikan_profil_adedi > kalan_adet:
        cikan_profil_adedi = kalan_adet

    brut_uretim = round(sp["profil_gramaj"] * sp["profil_boyu"] * cikan_profil_adedi, 2)
    fire = round(brut_uretim * random.uniform(0.015, 0.025), 2)
    net_uretim = round(brut_uretim - fire, 2)

    sp["kalan_adet"] -= cikan_profil_adedi
    sp["kalan_kg"] -= brut_uretim
    sp["kalan_billet"] -= 1

    zaman = datetime.now()
    operator = random.choice(operators)
    vardiya = random.choice(vardiyalar)

    # ----- Olay Günlüğü Mantığı -----
    olay_tipi = "Normal Üretim"
    olay_mesaji = f"{sip_no} üretimi devam ediyor."
    if sp["kalan_billet"] == sp["billet_sayisi"] - 1:  # Sipariş ilk başlarken
        olay_tipi = "Sipariş Başlangıcı"
        olay_mesaji = f"{sip_no} numaralı sipariş başlatıldı."
    elif sp["kalan_adet"] <= 0 or sp["kalan_billet"] <= 0 or sp["kalan_kg"] <= 0:  # Sipariş biterken
        olay_tipi = "Sipariş Bitişi"
        olay_mesaji = f"{sip_no} numaralı sipariş tamamlandı."
    elif random.random() < 0.05:  # %5 ihtimalle arıza
        olay_tipi = "Arıza"
        olay_mesaji = f"{sip_no} sırasında arıza oluştu!"
    elif random.random() < 0.07:  # %7 ihtimalle vardiya değişimi
        olay_tipi = "Vardiya Değişimi"
        olay_mesaji = f"{operator} ile Vardiya {vardiya} başladı."
    elif random.random() < 0.03:  # %3 ihtimalle kalıp değişimi
        olay_tipi = "Kalıp Değişimi"
        olay_mesaji = f"{sp['kalip']} kalıbına geçildi."

    # SQL insert ile veri ekle
    cur.execute("""
        INSERT INTO presdata (
            zaman, siparis_no, kalip_no, alasim, billet_boyu, billet_kg,
            profil_gramaj, profil_boyu, profil_adedi, brut_uretim, fire, net_uretim,
            kalan_adet, kalan_kg, kalan_billet, billet_sayisi, operator, vardiya,
            olay_tipi, olay_mesaji
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        zaman, sip_no, sp["kalip"], alasim, boy, billetkg, sp["profil_gramaj"], sp["profil_boyu"],
        cikan_profil_adedi, brut_uretim, fire, net_uretim,
        sp["kalan_adet"], sp["kalan_kg"], sp["kalan_billet"], sp["billet_sayisi"], operator, vardiya,
        olay_tipi, olay_mesaji
    ))
    conn.commit()

    print(
        f"{zaman.strftime('%H:%M:%S')} | Sipariş: {sip_no} | Kalıp: {sp['kalip']} | Alaşım: {alasim} | "
        f"Billet KG: {billetkg} | Çıkan profil adedi: {cikan_profil_adedi} | "
        f"Brüt: {brut_uretim} kg | Net: {net_uretim} kg | "
        f"Kalan: {sp['kalan_adet']} adet, {round(sp['kalan_kg'],1)} kg | "
        f"Kalan billet: {sp['kalan_billet']} | Olay: {olay_tipi} | Mesaj: {olay_mesaji}"
    )

    time.sleep(10)  # Her 10 sn'de bir veri

cur.close()
conn.close()
