from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# ChromeDriver yolu
driver_yolu = "C:\\Users\\User\\.wdm\\drivers\\chromedriver\\win64\\131.0.6778.85\\chromedriver-win32\\chromedriver.exe"

# Tarayıcı seçenekleri (isteğe bağlı)
options = webdriver.ChromeOptions()

# Driver başlatma (Service sınıfını kullanarak)
service = Service(driver_yolu)
browser = webdriver.Chrome(service=service, options=options)

# Google sayfasına gitme
browser.get("https://www.google.com")
print("Sayfa başlığı:", browser.title)

# Kullanıcıdan kitap adı ve yayınevini alma
kitap_adi = input("Kitap adı gir: ")
yayin = input("Yayınevi gir: ")

# Google'da Kitapyurdu araması yapma
search_box = browser.find_element("name", "q")
search_box.send_keys(kitap_adi + " " + yayin + " site:kitapyurdu.com")
time.sleep(1)
search_box.send_keys(Keys.ENTER)
time.sleep(3)

# İlk sonuç linkini tıklama
try:
    bkm_tik = browser.find_element(By.XPATH, "//*[@id='rso']/div[1]/div/div/div/div[1]/div/div/span/a")
    bkm_tik.click()
except Exception as e:
    print("Bağlantı bulunamadı:", e)
    browser.quit()
    exit()

# Sayfa yüklenene kadar bekle
time.sleep(2)

# Sayfa kaynağını al ve BeautifulSoup ile işle
bkm_sayfa = browser.page_source
bkm_soup = BeautifulSoup(bkm_sayfa, "lxml")

# Kitap adını al
try:
    bkm_bilgi = bkm_soup.find("div", attrs={"class": "pr_header"})
    bkm_ad = bkm_bilgi.find("h1").text.strip()
    print("Kitap Adı:", bkm_ad)
except Exception as e:
    print("Kitap bilgisi alınamadı:", e)

# Fiyat bilgisini al
try:
    bkm_sayi = bkm_soup.find("div", attrs={"class": "pr_price"})
    price_div = bkm_sayi.find("div", class_="price__item")
    price_text = price_div.text.strip()  # Tüm metni al
    price_main = price_text.split(',')[0].strip()  # Virgülden önceki kısmı al
    print("Fiyat:", price_main)
except Exception as e:
    print("Fiyat bilgisi alınamadı:", e)

# Tarayıcıyı kapatma
browser.quit()
