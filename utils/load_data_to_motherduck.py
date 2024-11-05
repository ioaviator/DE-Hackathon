import logging
import os
import duckdb
from dotenv import load_dotenv


def table_exists(con, db_name, table_name):
  try:
      result = con.execute(f"SELECT table_name FROM {db_name}.information_schema.tables WHERE table_name = '{table_name}'").fetchall()
      return len(result) > 0
  except Exception as e:
      logging.error(f"Error checking table existence in MotherDuck: {e}")
      return False

def load_data_to_motherduck():
    load_dotenv()
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    db_name = "my_db"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        logging.info("Connecting to MotherDuck...")
        con = duckdb.connect("md:", config={"motherduck_token": motherduck_token})
        logging.info("Connected to MotherDuck successfully.")

        if not table_exists(con, db_name, 'countries_tour_data'):
            logging.info("Loading table 'countries_tour_data' into MotherDuck...")
            con.execute(f"CREATE TABLE {db_name}.countries_tour_data AS SELECT * FROM 'countries_tour_data'")
            logging.info("Table 'countries_tour_data' loaded successfully.")
        else:
            logging.info("Table 'countries_tour_data' already exists in MotherDuck. Skipping loading.")

        if not table_exists(con, db_name, 'countries_language_expand'):
            logging.info("Loading table 'countries_language_expand' into MotherDuck...")
            con.execute(f"CREATE TABLE {db_name}.countries_language_expand AS SELECT * FROM 'countries_language_expand'")
            logging.info("Table 'countries_language_expand' loaded successfully.")
        else:
            logging.info("Table 'countries_language_expand' already exists in MotherDuck. Skipping loading.")

    except Exception as e:
        logging.error(f"Failed to load data into MotherDuck: {e}")
    finally:
        con.close()
