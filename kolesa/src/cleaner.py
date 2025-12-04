import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw_data.csv")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_data.csv")

def parse_description(row):
    text = str(row['description']).lower()
    
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    year = int(year_match.group(0)) if year_match else 0
    
    volume_match = re.search(r'(\d+(\.\d+)?)\s*л', text)
    volume = float(volume_match.group(1)) if volume_match else 0.0
    
    transmission = "other"
    if "автомат" in text or "типтроник" in text: transmission = "automatic"
    elif "механика" in text: transmission = "manual"
    elif "робот" in text: transmission = "robot"
    elif "вариатор" in text: transmission = "cvt"
    
    body_style = "other"
    bodies = ["седан", "кроссовер", "внедорожник", "хэтчбек", "универсал", "лифтбек", "купе"]
    for b in bodies:
        if b in text:
            body_style = b
            break

    drive_type = "other"
    if "передний" in text: drive_type = "fwd"
    elif "полный" in text: drive_type = "awd"
    elif "задний" in text: drive_type = "rwd"
    
    fuel = "other"
    if "бензин" in text: fuel = "petrol"
    elif "дизель" in text: fuel = "diesel"
    elif "газ" in text: fuel = "gas"
    elif "электро" in text: fuel = "electric"

    return pd.Series([year, volume, transmission, body_style, drive_type, fuel])

def clean_price(val):
    try:
        return int(re.sub(r'\D', '', str(val)))
    except:
        return 0

def run_cleaner():
    print(f"--- CLEANING DATA ---")
    print(f"Looking for file: {RAW_DATA_PATH}")

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"File {RAW_DATA_PATH} not found! Did the scraper run?")

    df = pd.read_csv(RAW_DATA_PATH)
    
    if df.empty:
        raise ValueError("CSV file is empty!")

    df['price'] = df['raw_price'].apply(clean_price)
    
    new_cols = df.apply(parse_description, axis=1)
    new_cols.columns = ['year', 'engine_vol', 'transmission', 'body_style', 'drive_type', 'fuel']
    
    final_df = pd.concat([df[['title', 'city', 'price']], new_cols], axis=1)
    

    final_df = final_df[final_df['price'] > 0]
    final_df = final_df[final_df['year'] > 1900]

    final_df = final_df.drop_duplicates(subset=['title', 'city', 'year'], keep='first')

    print(final_df.head())
    print(f"Clean records: {len(final_df)}")
    
    final_df.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"Saved to {CLEAN_DATA_PATH}")

if __name__ == "__main__":
    run_cleaner()