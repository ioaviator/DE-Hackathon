import logging

def load_data_to_duckdb(table_exists, con, df_language_expand):
    table1_name = 'countries_tour_data'
    if not table_exists(con, table1_name):
        logging.info(f"Saving DataFrame to table '{table1_name}' in DuckDB...")
        con.execute(f"CREATE OR REPLACE TABLE {table1_name} AS SELECT * FROM df")
        logging.info(f"Data saved to table '{table1_name}' successfully.")
    else:
        logging.info(f"Table '{table1_name}' already exists in DuckDB. Skipping ingestion.")

    table2 = 'countries_language_expand'
    if not table_exists(con, table2):
        if not df_language_expand.empty:
            logging.info(f"Saving DataFrame to table '{table2}' in DuckDB...")
            con.execute(f"CREATE OR REPLACE TABLE {table2} AS SELECT * FROM df_language_expand")
            logging.info(f"Data saved to table '{table2}' successfully.")
        else:
            logging.warning(f"DataFrame '{table2}' is empty. Skipping ingestion.")
    else:
        logging.info(f"Table '{table2}' already exists in DuckDB. Skipping ingestion.")
