# Selenium Headless Stres Testi Kullanım Kılavuzu

Bu araç, bir web sitesinin "ürünler" veya benzeri sayfalarının eşzamanlı olarak kaç kullanıcıyı kaldırabildiğini (sınırını) test etmek için Python ve Selenium (Headless) kullanılarak hazırlanmıştır.

## ⚠️ Önemli Uyarı (Lütfen Okuyun)
Selenium her bir sanal kullanıcı için arka planda gerçek bir Chrome tarayıcı açar. 
Eğer `--users` parametresini çok yüksek verirseniz (örneğin 500, 1000), testi çalıştırdığınız bu **bilgisayarın CPU ve RAM'i tamamen tükenebilir ve bilgisayarınız çökebilir.** 
* Teste düşük sayılarla (10, 50) başlayın.
* Sunucu sınırından önce bilgisayarınızın sınırına takılabileceğinizi unutmayın.

---

## 1. Kurulum (İlk Hazırlık)

Testi çalıştırabilmeniz için bilgisayarınızda **Python 3** yüklü olmalıdır.

**Gerekli Kütüphaneleri Yüklemek İçin:**
Komut satırını (Terminal veya CMD) açın, bu dosyaların bulunduğu klasöre gidin ve aşağıdaki komutu çalıştırın:
```bash
pip install -r requirements.txt
```

---

## 2. Testi Çalıştırma

Terminal ekranında aşağıdaki komutu kendinize göre düzenleyerek testi başlatabilirsiniz:

```bash
python stress_test.py --url "https://ornek-site.com/urunler" --users 10
```

* `--url`: Test edilecek hedefin tam adresini girin (Tırnak içinde yazmanız önerilir).
* `--users`: Aynı anda (eşzamanlı) sayfaya girecek kullanıcı sayısıdır.

### Deneme Stratejisi
Sistemin çökme noktasını bulmak için testi kademeli olarak artırarak çalıştırın:
1. Adım: `python stress_test.py --url "..." --users 10`
2. Adım: `python stress_test.py --url "..." --users 50`
3. Adım: `python stress_test.py --url "..." --users 100`
... (Hatalar ("Başarısız İstekler") artmaya başladığında sunucunun sınırına yaklaşmışsınız demektir.)

---

## 3. Ekstra Etkileşimler (Gelişmiş)
Eğer sadece sayfanın yüklenmesi yetmiyor ve kullanıcıların sayfada **aşağı kaydırmasını (scroll)** veya **bir butona tıklamasını** istiyorsanız:

1. `stress_test.py` dosyasını herhangi bir metin editörüyle açın.
2. `user_task` fonksiyonunun içindeki "ETKİLEŞİM ŞABLONLARI" bölümünü bulun.
3. İhtiyacınız olan kodların başındaki `#` işaretlerini kaldırarak aktifleştirin ve HTML ID/Class değerlerini kendi sitenize göre değiştirin.
