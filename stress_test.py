import argparse
import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Loglama ayarları (Ekrana bilgi basmak için)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_headless_driver():
    """Headless (görünmez) Chrome tarayıcı ayarlarını yapılandırır."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Tarayıcıyı arka planda (arayüzsüz) çalıştır
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Selenium 4.6+ dahili (built-in) Selenium Manager kullanır, webdriver_manager'a gerek yoktur
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def user_task(user_id, target_url):
    """Her bir sanal kullanıcının (thread) yapacağı işlemleri tanımlar."""
    start_time = time.time()
    driver = None
    try:
        logging.info(f"Kullanıcı {user_id} tarayıcıyı başlatıyor...")
        driver = setup_headless_driver()
        
        # 1. URL'ye Git
        logging.info(f"Kullanıcı {user_id} {target_url} adresine gidiyor...")
        driver.get(target_url)
        
        # 2. Sayfanın yüklenmesini bekle (Örnek: body etiketinin yüklenmesini bekle)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # --- ETKİLEŞİM ŞABLONLARI (İHTİYAÇ HALİNDE AŞAĞIDAKİLERİ YORUMDAN ÇIKARTABİLİRSİNİZ) ---
        
        # Örnek A: Sayfanın en altına kadar kaydırma (Scroll)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(1) # Kaydırdıktan sonra biraz bekle
        
        # Örnek B: Belirli bir butona tıklama (ID veya Class ile)
        # buton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sepete-ekle-butonu")))
        # buton.click()
        # time.sleep(1)
        
        # ----------------------------------------------------------------------------------------
        
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Kullanıcı {user_id} işlemi BAŞARIYLA tamamladı. Süre: {duration:.2f} saniye")
        return {"user_id": user_id, "status": "success", "duration": duration}
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logging.error(f"Kullanıcı {user_id} HATA ALDI: {str(e)[:100]}... Süre: {duration:.2f} saniye")
        return {"user_id": user_id, "status": "error", "duration": duration, "error": str(e)}
    finally:
        if driver:
            driver.quit() # Tarayıcıyı mutlaka kapat, yoksa RAM şişer

def main():
    parser = argparse.ArgumentParser(description="Selenium Headless Web Stres Test Aracı")
    parser.add_argument("--url", required=True, help="Test edilecek hedef URL (örn: https://example.com/products)")
    parser.add_argument("--users", type=int, default=10, help="Eşzamanlı çalışacak sanal kullanıcı sayısı (Varsayılan: 10)")
    
    args = parser.parse_args()
    
    target_url = args.url
    num_users = args.users
    
    print("="*60)
    print(f"STRES TESTİ BAŞLIYOR")
    print(f"Hedef URL       : {target_url}")
    print(f"Kullanıcı Sayısı: {num_users}")
    print("="*60)
    
    # ThreadPoolExecutor ile eşzamanlı (concurrent) tarayıcıları başlat
    results = []
    start_total_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        # Future objelerini oluştur (görevleri havuza at)
        futures = [executor.submit(user_task, i+1, target_url) for i in range(num_users)]
        
        # Görevlerin tamamlanmasını bekle ve sonuçları topla
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    end_total_time = time.time()
    
    # Sonuçları Analiz Et
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")
    total_duration = end_total_time - start_total_time
    
    print("\n" + "="*60)
    print(f"TEST TAMAMLANDI")
    print(f"Toplam Geçen Süre : {total_duration:.2f} saniye")
    print(f"Başarılı İstekler : {successful}")
    print(f"Başarısız İstekler: {failed}")
    if failed > 0:
        print("DİKKAT: Başarısız istekler var. Sunucu sınırına ulaşılmış veya aşılmış olabilir!")
    print("="*60)

if __name__ == "__main__":
    main()
