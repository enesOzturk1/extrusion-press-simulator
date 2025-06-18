# Pres Üretim Simülasyonu

Bu proje, alüminyum ekstrüzyon üretimini Python ile simüle eder. Üretilen veriler TimescaleDB veritabanına kaydedilir ve Grafana üzerinden canlı olarak izlenebilir. Sistem, Docker Compose kullanılarak kolayca ayağa kaldırılabilir.

---

## 🚀 Kullanılan Teknolojiler

- **Python** – Üretim verisi simülasyonu  
- **PostgreSQL + TimescaleDB** – Zaman serisi veri tabanı  
- **Grafana** – Görselleştirme paneli  
- **Docker** – Konteyner yönetimi  

---

## 🧱 Sistem Mimarisi

Sistem üç ana bileşenden oluşmaktadır:

1. Python scripti ile üretilen veriler,  
2. TimescaleDB veritabanına kaydedilmektedir,  
3. Grafana arayüzü ile kullanıcıya sunulmaktadır.

---

## ⚙️ Simülasyon Yapısı

`simulate.py` dosyasında, rastgele sipariş ve kalıp bilgileri ile işlenen billet verileri, üretim gramajları ve fire oranları gibi çeşitli üretim parametreleri simüle edilerek 5 saniyede bir veritabanına yazılmaktadır.

---

## 🗃️ Veritabanı Şeması

Veritabanında `presdata` isimli tablo aşağıdaki sütunlardan oluşur:

- `id`: Otomatik artan benzersiz ID  
- `zaman`: Zaman damgası (TIMESTAMPTZ)  
- `siparis_no`: Sipariş numarası  
- `kalip_no`: Kalıp numarası  
- `alasim`: Kullanılan alaşım tipi  
- `billet_boyu`: Billet uzunluğu (mm)  
- `billet_kg`: Tek billetin kilogramı  
- `profil_gramaj`: Profilin gramajı (gr/m)  
- `profil_boyu`: Profilin boyu (m)  
- `profil_adedi`: Üretilen profil adedi  
- `brut_uretim`: Brüt üretim miktarı (kg)  
- `fire`: Fire miktarı (kg)  
- `net_uretim`: Net üretim miktarı (kg)  
- `kalan_adet`: Kalan üretilecek adet  
- `kalan_kg`: Kalan üretim miktarı (kg)  
- `kalan_billet`: Kalan billet adedi  
- `billet_sayisi`: Siparişte kullanılan toplam billet sayısı  
- `operator`: Operatör adı  
- `vardiya`: Vardiya numarası  
- `olay_tipi`: Olay türü (üretim, hata, uyarı vb.)  
- `olay_mesaji`: Açıklayıcı mesaj veya olay detayı  

> TimescaleDB kullanılarak `zaman` sütunu üzerinden `hypertable` oluşturulmuştur.

---

## 📌 Sonuç ve Değerlendirme

Bu proje ile üretim verilerinin simüle edilmesi, depolanması ve görselleştirilmesi süreci başarıyla gerçekleştirilmiştir. Endüstriyel üretim ortamlarında benzer yapılar kullanılarak anlık takip ve analiz sistemleri geliştirilebilir.
