import sqlite3
import pandas as pd
import os

db_path = "data/output.db"

if not os.path.exists(db_path):
    print(f"ERROR: File {db_path} not found!")
else:
    try:
        conn = sqlite3.connect(db_path)
        
        df = pd.read_sql("SELECT * FROM cars", conn)
        
        print(f"\n--- SUCCESS! FOUND {len(df)} RECORDS IN DB ---")
        print("Here are the first 10 rows:\n")
        print(df.head(10).to_string()) 
        
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")