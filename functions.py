import requests
import pandas as pd
import os
import duckdb
import logging
from dotenv import load_dotenv

def fetch_country_data(url="https://restcountries.com/v3.1/all"):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    countries_data = response.json()

    data = {
        "Country Name": [],
        "Independence": [],
        "United Nation members": [],
        "startOfWeek": [],
        "Official country name": [],
        "Common native name": [],
        "Currency Code": [],
        "Currency name": [],
        "Currency symbol": [],
        "Country code": [],
        "Capital": [],
        "Region": [],
        "Sub region": [],
        "Languages": [],
        "Area": [],
        "Population": [],
        "Continents": []
    }

    for i in countries_data:
        data["Country Name"].append(i.get("name", {}).get("common", "Unknown"))
        data["Independence"].append(i.get("independent", "Unknown"))
        data["United Nation members"].append(i.get("unMember", "Unknown"))
        data["startOfWeek"].append(i.get("startOfWeek", "Unknown"))
        data["Official country name"].append(i.get("name", {}).get("official", "Unknown"))

        native_names = i.get("name", {}).get("nativeName", {})
        common_native_name = next(iter(native_names.values()), {}).get("common", "Unknown")
        data["Common native name"].append(common_native_name)

        currencies = i.get("currencies", {})
        currency_codes = ", ".join(currencies.keys())
        currency_names = ", ".join(details.get("name", "Unknown") for details in currencies.values())
        currency_symbols = ", ".join(details.get("symbol", "Unknown") for details in currencies.values())
        data["Currency Code"].append(currency_codes)
        data["Currency name"].append(currency_names)
        data["Currency symbol"].append(currency_symbols)

        idd = i.get("idd", {})
        country_code = idd.get("root", "") + "".join(idd.get("suffixes", []))
        data["Country code"].append(country_code or "Unknown")

        data["Capital"].append(i.get("capital", [None])[0])
        data["Region"].append(i.get("region", "Unknown"))
        data["Sub region"].append(i.get("subregion", "Unknown"))

        languages = i.get("languages", {})
        languages_list = ", ".join(languages.values())
        data["Languages"].append(languages_list or "Unknown")

        data["Area"].append(i.get("area", "Unknown"))
        data["Population"].append(i.get("population", "Unknown"))

        data["Continents"].append(i.get("continents", [None])[0])

    df = pd.DataFrame(data)
    return df

def transform_data(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.fillna('Unspecified', inplace=True)

    df_language = df[['country_name', 'languages']]
    df_language_expand = df_language.set_index('country_name')['languages'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='language')
    
    df.drop('languages', axis=1, inplace=True)
    
    return df, df_language_expand

def load_data_to_motherduck():
    load_dotenv()
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    db_name = "my_db"

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        logging.info("Connecting to MotherDuck...")
        con = duckdb.connect("md:", config={"motherduck_token": motherduck_token})
        logging.info("Connected to MotherDuck successfully.")

        def table_exists(con, db_name, table_name):
            try:
                result = con.execute(f"SELECT table_name FROM {db_name}.information_schema.tables WHERE table_name = '{table_name}'").fetchall()
                return len(result) > 0
            except Exception as e:
                logging.error(f"Error checking table existence in MotherDuck: {e}")
                return False

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
