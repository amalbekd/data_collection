import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_data.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "output.db")

def run_loader():
    print("--- LOADING TO DB ---")
    if not os.path.exists(CLEAN_DATA_PATH):
        print("No cleaned_data.csv file found!")
        return

    df = pd.read_csv(CLEAN_DATA_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price INTEGER,
        city TEXT,
        year INTEGER,
        engine_vol REAL,
        transmission TEXT,
        body_style TEXT,
        drive_type TEXT,
        fuel TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

    df.to_sql('cars', conn, if_exists='append', index=False)
    print(f"Loaded {len(df)} rows into the 'cars' table.")
    conn.close()

if __name__ == "__main__":
    run_loader()