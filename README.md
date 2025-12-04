Here is the professional, ready-to-use **README.md** file in English. It covers all the points required by your assignment.

Copy the code below and save it as `README.md` in your project folder.

# Kolesa.kz ETL Data Pipelinе

**Course:** Data Collection & Preparation  
**Project:** Automated ETL Pipeline using Playwright, Docker, and Apache Airflow.

## 1. Website Description
**Target Website:** [Kolesa.kz](https://kolesa.kz/cars/almaty/)

**Description:**
Kolesa.kz is the largest vehicle classifieds platform in Kazakhstan. It is a **dynamic website** that renders content using JavaScript.
This project scrapes listing data for passenger cars in Almaty, extracting details such as vehicle name, price, year of manufacture, engine volume, transmission type, and body style.

**Challenges:**
- The site uses dynamic DOM elements.
- It requires handling pagination and scrolling.
- Protection mechanisms require "human-like" browser behavior (Headless Chrome).

---

## 2. Tech Stack
*   **Language:** Python 3.10
*   **Scraping:** Playwright (for dynamic content extraction)
*   **Data Processing:** Pandas (cleaning, regex extraction, type conversion)
*   **Database:** SQLite3
*   **Orchestration:** Apache Airflow
*   **Containerization:** Docker & Docker Compose

---

## 3. Project Structure
```text
project/
├── dags/                  # Airflow DAG folder
│   └── airflow_dag.py     # DAG configuration
├── src/                   # ETL Scripts
│   ├── scraper.py         # Extract: Scrapes raw data to CSV
│   ├── cleaner.py         # Transform: Cleans and parses columns
│   └── loader.py          # Load: Inserts data into SQLite
├── data/                  # Data storage
│   ├── raw_data.csv       # Intermediate raw data
│   ├── cleaned_data.csv   # Intermediate clean data
│   └── output.db          # Final SQLite Database
├── check_db.py            # Script to view database contents
├── docker-compose.yml     # Docker orchestration config
├── Dockerfile             # Custom Airflow image with Playwright
├── entrypoint.sh          # Entry script for Docker
└── requirements.txt       # Python dependencies
```

---

## 4. How to Run (Automated with Airflow)

The entire pipeline is containerized. This is the recommended way to run the project.

**Prerequisites:**
- Docker Desktop installed and running.

**Steps:**
1.  Open a terminal in the project root.
2.  Build and start the container:
    ```bash
    docker-compose up --build
    ```
3.  Wait until the logs show `Airflow is ready` (usually 1-2 minutes).
4.  Open your browser and go to: **http://localhost:8085**
5.  Login with credentials:
    *   **Username:** `admin`
    *   **Password:** `admin`
6.  Locate the DAG named **`kolesa_trucks_etl`**.
7.  **Unpause** the DAG (toggle the switch to blue) and click the **Play** button -> **Trigger DAG**.
8.  Watch the **Graph** view. Wait for all tasks (`scrape` -> `clean` -> `load`) to turn **Dark Green (Success)**.

---

## 5. How to Run (Manual Scraping)

If you cannot use Docker, you can run the scripts sequentially in your local environment.

**Prerequisites:**
- Python 3.8+ installed.
- Dependencies installed: `pip install -r requirements.txt`
- Playwright browsers installed: `playwright install chromium`

**Steps:**
1.  Run the Scraper (Extract):
    ```bash
    python src/scraper.py
    ```
2.  Run the Cleaner (Transform):
    ```bash
    python src/cleaner.py
    ```
3.  Run the Loader (Load):
    ```bash
    python src/loader.py
    ```
4.  Check the database:
    ```bash
    python check_db.py
    ```

---

## 6. Expected Output

The pipeline creates a SQLite database file located at `data/output.db`.
The table `cars` contains the following schema:

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Auto-incrementing ID |
| `title` | TEXT | E.g., "Toyota Camry" |
| `price` | INTEGER | Cleaned price (e.g., 9500000) |
| `city` | TEXT | E.g., "Almaty" |
| `year` | INTEGER | Extracted year (e.g., 2018) |
| `engine_vol` | REAL | Engine volume in liters (e.g., 2.5) |
| `transmission`| TEXT | automatic / manual / robot / cvt |
| `body_style` | TEXT | sedan / crossover / suv / etc. |
| `fuel` | TEXT | petrol / diesel / gas / electric |
| `created_at` | TIMESTAMP | Time of data insertion |

**Sample Data (from `check_db.py`):**
```text
   id         title       price    city  year  engine_vol transmission   body_style  fuel
0   1   Toyota RAV4   8500000  Алматы  2007         2.4    automatic    кроссовер  petrol
1   2       BMW 316   8500000  Алматы  1983         4.4       manual         купе  petrol
2   3  Toyota Camry   9450000  Алматы  2015         2.5    automatic        седан  petrol
```