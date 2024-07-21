import requests
import pandas as pd
import os
import logging
import duckdb
from dotenv import load_dotenv
from functions import attach_db_to_motherduck, fetch_country_data

load_dotenv()

duckdb_file_path = os.getenv("DB_PATH")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    logging.info("Fetching country data from API...")
    df = fetch_country_data()
    logging.info("Data fetched successfully.")
    logging.info("Saving data to DuckDB...")
    con = duckdb.connect(duckdb_file_path)
    
    table_exists = con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'countries_tour_data'").fetchone()[0]
    if table_exists:
        logging.warning("Table 'countries_tour_data' already exists. Dropping the existing table.")
        con.execute("DROP TABLE countries_tour_data")
    
    con.execute("CREATE TABLE countries_tour_data AS SELECT * FROM df")
    logging.info("Data saved to DuckDB successfully.")
except Exception as e:
    logging.error(f"Error occurred: {e}")
finally:
    con.close()
attach_db_to_motherduck()