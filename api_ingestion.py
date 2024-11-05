import os
import logging
import duckdb
import pandas as pd
from dotenv import load_dotenv

from utils.extract_data import fetch_country_data
from utils.extract_data import extract_country_data
from utils.api_to_dataframe import convert_to_dataframe
from utils.load_data_to_motherduck import load_data_to_motherduck
from utils.load_data_to_duckdb import load_data_to_duckdb
from utils.transform_data import transform_data
from utils.connect_api import fetch_country_data


load_dotenv()
duckdb_file_path = os.getenv("DB_PATH")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
con = None

def table_exists(con, table_name):
    try:
        result = con.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'").fetchone()
        return result[0] > 0
    except Exception as e:
        logging.error(f"Error checking table existence: {e}")
        return False

## Activate API calls 
## Extract data from API
## Convert to dataframe
## Transform Data
try:
    logging.info("Fetching country data from API...")
    raw_data = fetch_country_data()
    country_data = extract_country_data(raw_data)
    df = convert_to_dataframe(country_data)
    df, df_language_expand = transform_data(df)
    logging.info(f"DataFrame 'df' has {df.shape[0]} rows and {df.shape[1]} columns.")
    
    logging.info("Data fetched and transformed successfully.")

    logging.info("Connecting to DuckDB...")
    con = duckdb.connect(duckdb_file_path)

    ## load data to duckdb
    load_data_to_duckdb(table_exists, con, df_language_expand)

    tables = con.execute("SHOW TABLES").fetchall()
    logging.info(f"Tables in DuckDB: {tables}")

except Exception as e:
    logging.error(f"Error occurred: {e}")

finally:
    if con:
        con.close()
    logging.info("Disconnected from DuckDB.")


### loading data to motherduck
try:
    logging.info("Loading data into MotherDuck...")
    load_data_to_motherduck()
    logging.info("Data loaded into MotherDuck successfully.")
except Exception as e:
    logging.error(f"Failed to load data into MotherDuck: {e}")
