import requests
import pandas as pd
import os
import logging
import duckdb
from dotenv import load_dotenv
from functions import attach_db_to_motherduck, fetch_country_data, transform_data

load_dotenv()
duckdb_file_path = os.getenv("DB_PATH")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    logging.info("Fetching country data from API...")
    df, df_language_expand = transform_data(fetch_country_data())
    logging.info("Data fetched and transformed successfully.")
    logging.info("Connecting to DuckDB...")
    con = duckdb.connect(duckdb_file_path)
    table1_name = 'countries_tour_data'
    logging.info(f"Saving DataFrame to table '{table1_name}' in DuckDB...")
    con.execute(f"CREATE TABLE IF NOT EXISTS {table1_name} AS SELECT * FROM df")
    logging.info(f"Data saved to table '{table1_name}' successfully.")

    table2 = 'countries_language_expand'
    logging.info(f"Saving DataFrame to table '{table2}' in DuckDB...")
    con.execute(f"CREATE TABLE IF NOT EXISTS {table2} AS SELECT * FROM df_language_expand")
    logging.info(f"Data saved to table '{table2}' successfully.")

except Exception as e:
    logging.error(f"Error occurred: {e}")

finally:
    con.close()
    logging.info("Disconnected from DuckDB.")
try:
    logging.info("Attaching DuckDB database to MotherDuck...")
    attach_db_to_motherduck()
    logging.info("Database attached to MotherDuck successfully.")
except Exception as e:
    logging.error(f"Failed to attach database to MotherDuck: {e}")
