import requests
import pandas as pd
import os
import duckdb
import logging
from dotenv import load_dotenv

def fetch_country_data(url="https://restcountries.com/v3.1/all"):
    response = requests.get(url)
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
        data["Country Name"].append(i.get("name", {}).get("common"))
        data["Independence"].append(i.get("independent"))
        data["United Nation members"].append(i.get("unMember"))
        data["startOfWeek"].append(i.get("startOfWeek"))
        data["Official country name"].append(i.get("name", {}).get("official"))

        native_names = i.get("name", {}).get("nativeName", {})
        if native_names:
            common_native_name = list(native_names.values())[0].get("common")
        else:
            common_native_name = None
        data["Common native name"].append(common_native_name)

        currencies = i.get("currencies")
        if currencies:
            currency_codes = ", ".join(currencies.keys())
            currency_names = ", ".join([details.get("name") for details in currencies.values()])
            currency_symbols = ", ".join([details.get("symbol") for details in currencies.values() if details.get("symbol")])
        else:
            currency_codes = None
            currency_names = None
            currency_symbols = None
        data["Currency Code"].append(currency_codes)
        data["Currency name"].append(currency_names)
        data["Currency symbol"].append(currency_symbols)

        idd = i.get("idd", {})
        root = idd.get("root", "")
        suffixes = idd.get("suffixes", [])
        if root and suffixes:
            country_code = root + "".join(suffixes)
        else:
            country_code = None
        data["Country code"].append(country_code)

        capital = i.get("capital", [])
        if capital:
            capital_city = capital[0]
        else:
            capital_city = None
        data["Capital"].append(capital_city)

        data["Region"].append(i.get("region"))
        data["Sub region"].append(i.get("subregion"))

        languages = i.get("languages", {})
        if languages:
            languages_list = ", ".join(languages.values())
        else:
            languages_list = None
        data["Languages"].append(languages_list)

        data["Area"].append(i.get("area"))
        data["Population"].append(i.get("population"))

        continents = i.get("continents", [])
        if continents:
            continent = continents[0]
        else:
            continent = None
        data["Continents"].append(continent)

    df = pd.DataFrame(data)
    return df

def attach_db_to_motherduck():
    load_dotenv()
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    db_path = os.getenv("DB_PATH")
    db_name = "countries_tour_data"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        logging.info("Connecting to MotherDuck...")
        con = duckdb.connect("md:", config={"motherduck_token": motherduck_token})
        logging.info("Connected to MotherDuck successfully.")

        logging.info(f"Checking if the database '{db_path}' is already attached...")

        attached_dbs = con.execute("PRAGMA database_list").fetchall()
        logging.info(f"Currently attached databases: {attached_dbs}")

        for db in attached_dbs:
            if db[1] == db_name:
                logging.info(f"Detaching the already attached database: {db_name}")
                con.execute(f"DETACH DATABASE {db_name}")
                logging.info(f"Database '{db_name}' detached successfully.")

        logging.info(f"Attaching the database from path: {db_path}")
        con.sql(f"ATTACH DATABASE '{db_path}' AS {db_name}")
        logging.info(f"Database '{db_path}' attached successfully.")
        logging.info(f"Checking if the database '{db_name}' exists in MotherDuck...")
        existing_dbs = con.execute("SHOW DATABASES").fetchall()
        if db_name in [db[0] for db in existing_dbs]:
            logging.info(f"Database '{db_name}' already exists in MotherDuck. Skipping creation.")
        else:
            logging.info(f"Creating the database '{db_name}' in MotherDuck...")
            con.sql(f"CREATE DATABASE {db_name} FROM '{db_path}'")
            logging.info(f"Database '{db_name}' created successfully in MotherDuck.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        con.close()