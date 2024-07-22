import os
import logging
import duckdb
from dotenv import load_dotenv
from functions import fetch_country_data, transform_data,load_data_to_motherduck

load_dotenv()
duckdb_file_path = os.getenv("DB_PATH")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

con = None
try:
    logging.info("Fetching country data from API...")
    df, df_language_expand = transform_data(fetch_country_data())
    logging.info(f"DataFrame 'df' has {df.shape[0]} rows and {df.shape[1]} columns.")
    logging.info(f"DataFrame 'df_language_expand' has {df_language_expand.shape[0]} rows and {df_language_expand.shape[1]} columns.")
    logging.info("Data fetched and transformed successfully.")

    logging.info("Connecting to DuckDB...")
    con = duckdb.connect(duckdb_file_path)

    def table_exists(con, table_name):
        try:
            result = con.execute(f"SHOW TABLES LIKE '{table_name}'").fetchall()
            return len(result) > 0
        except Exception as e:
            logging.error(f"Error checking table existence: {e}")
            return False

    table1_name = 'countries_tour_data'
    if not table_exists(con, table1_name):
        logging.info(f"Saving DataFrame to table '{table1_name}' in DuckDB...")
        con.execute(f"CREATE OR REPLACE TABLE {table1_name} AS SELECT * FROM df")
        logging.info(f"Data saved to table '{table1_name}' successfully.")
    else:
        logging.info(f"Table '{table1_name}' already exists in DuckDB. Skipping ingestion.")

    table2 = 'countries_language_expand'
    if not table_exists(con, table2):
        logging.info(f"Saving DataFrame to table '{table2}' in DuckDB...")
        con.execute(f"CREATE OR REPLACE TABLE {table2} AS SELECT * FROM df_language_expand")
        logging.info(f"Data saved to table '{table2}' successfully.")
    else:
        logging.info(f"Table '{table2}' already exists in DuckDB. Skipping ingestion.")

    tables = con.execute("SHOW TABLES").fetchall()
    logging.info(f"Tables in DuckDB: {tables}")

except Exception as e:
    logging.error(f"Error occurred: {e}")

finally:
    if con:
        con.close()
    logging.info("Disconnected from DuckDB.")

try:
    logging.info("Attaching DuckDB database to MotherDuck...")
    attach_db_to_motherduck()
    logging.info("Database attached to MotherDuck successfully.")
except Exception as e:
    logging.error(f"Failed to attach database to MotherDuck: {e}")

try:
    logging.info("Loading data into MotherDuck...")
    load_data_to_motherduck()
    logging.info("Data loaded into MotherDuck successfully.")
except Exception as e:
    logging.error(f"Failed to load data into MotherDuck: {e}")
