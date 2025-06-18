## Pres Üretim Simülasyonu

Bu proje, alüminyum ekstrüzyon üretimini Python ile simüle eder. Üretilen veriler TimescaleDB veritabanına kaydedilir ve Grafana üzerinden canlı olarak izlenebilir. Sistem, Docker Compose kullanılarak kolayca ayağa kaldırılabilir.


##  Kullanılan Teknolojiler

- **Python** – Üretim verisi simülasyonu
- **PostgreSQL + TimescaleDB** – Zaman serisi veri tabanı
- **Grafana** – Görselleştirme paneli
- **Docker** – Konteyner yönetimi


##  Sistem Mimarisi

Sistem üç ana bileşenden oluşmaktadır:

1. Python scripti ile üretilen veriler,

2. TimesclaDB veritabanına kaydedilmektedir,

3. Grafana arayüzü ile kullanıcıya sunulmaktadır.


## Similasyon Yapısı

simulate.py dosyasında, rastgele sipariş ve kalıp bilgileri ile işlenen billet sayısı ve fire oranı
üretilmektedir. Her 5 saniyede bir kayıt, veritabanına işlenmektedir.


## Veritabanı Şeması

Veritabanında 'presdata' isimli tablo oluşturulmuştur. Bu tablo aşağıdaki sütunları içerir:
- siparis_no: Sipariş numarası
- kalip_no: Kalıp numarası
- islenen_billet: İşlenen billet sayısı
- fire_orani: Oluşan fire oranı
- zaman: Zaman damgası
Zaman serisi verisi olarak optimize edilmesi için TimescaleDB'nin hypertable özelliği
kullanılmıştır


## Sonuç ve Değerlendirme

Bu proje ile üretim verilerinin simüle edilmesi, depolanması ve görselleştirilmesi süreci başarıyla
gerçekleştirilmiştir. Endüstriyel üretim ortamlarında benzer yapılar kullanılarak anlık takip ve
analiz sistemleri geliştirilebilir.


