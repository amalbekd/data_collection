import csv
import time
import random
import os
import sys
from playwright.sync_api import sync_playwright


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_data.csv")
BASE_URL = "https://kolesa.kz/cars/almaty/"

def clean_text(text):
    if not text: return ""
    return text.replace("\n", " ").replace("\xa0", "").strip()

def run_scraper():
    print(f"--- go scraping ---")
    print(f"Path to save: {RAW_DATA_PATH}")
    

    if not os.path.exists(DATA_DIR):
        print(f"Folder {DATA_DIR} not found, creating...")
        os.makedirs(DATA_DIR, exist_ok=True)

    data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-setuid-sandbox']
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
     
        for i in range(1, 10):
            url = f"{BASE_URL}?page={i}"
            print(f">>> page {i}: {url}")
            
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(2)
                
                ads = page.query_selector_all("div.a-card")
                if not ads: ads = page.query_selector_all("div.a-elem") 
                
                print(f"   Found ads: {len(ads)}")

                for ad in ads:
                    try:
                        t_el = ad.query_selector("[class*='title']")
                        p_el = ad.query_selector("[class*='price']")
                        d_el = ad.query_selector("[class*='desc'], [class*='body']")
                        city_el = ad.query_selector("[class*='region']")

                        title = clean_text(t_el.inner_text()) if t_el else "No title"
                        price = clean_text(p_el.inner_text()) if p_el else "0"
                        desc = clean_text(d_el.inner_text()) if d_el else ""
                        city = clean_text(city_el.inner_text()) if city_el else "Almaty"

                        if title:
                            data.append((title, price, city, desc))
                    except Exception as e:
                        continue
            except Exception as e:
                print(f"Error on page {i}: {e}")
            
            time.sleep(random.uniform(1, 2))
            
        browser.close()

    if data:
        with open(RAW_DATA_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "raw_price", "city", "description"])
            writer.writerows(data)
        print(f"✅ УСПЕХ! Сохранено {len(data)} строк в {RAW_DATA_PATH}")
    else:
        print("!!! EMPTY !!! Failed to collect data.")
        raise ValueError("Scraper returned an empty list!")

if __name__ == "__main__":
    run_scraper()