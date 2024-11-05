import pandas as pd
import os
import logging
from api_schema import data 

def extract_country_data(raw_data):
    for i in raw_data:
        data["Country_Name"].append(i.get("name", {}).get("common", "Unknown"))
        data["Independence"].append(i.get("independent", "Unknown"))
        data["United_Nation members"].append(i.get("unMember", "Unknown"))
        data["Start_Of_Week"].append(i.get("startOfWeek", "Unknown"))
        data["Official_Country_Name"].append(i.get("name", {}).get("official", "Unknown"))

        native_names = i.get("name", {}).get("nativeName", {})
        common_native_name = next(iter(native_names.values()), {}).get("common", "Unknown")
        data["Common_Native_Name"].append(common_native_name)

        currencies = i.get("currencies", {})
        currency_codes = ", ".join(currencies.keys())
        currency_names = ", ".join(details.get("name", "Unknown") for details in currencies.values())
        currency_symbols = ", ".join(details.get("symbol", "Unknown") for details in currencies.values())
        data["Currency_Code"].append(currency_codes)
        data["Currency_Name"].append(currency_names)
        data["Currency_Symbol"].append(currency_symbols)

        idd = i.get("idd", {})
        country_code = idd.get("root", "") + "".join(idd.get("suffixes", []))
        data["Country_Code"].append(country_code or "Unknown")

        data["Capital"].append(i.get("capital", [None])[0])
        data["Region"].append(i.get("region", "Unknown"))
        data["Sub_Region"].append(i.get("subregion", "Unknown"))

        languages = i.get("languages", {})
        languages_list = ", ".join(languages.values())
        data["Languages"].append(languages_list or "Unknown")

        data["Area"].append(i.get("area", "Unknown"))
        data["Population"].append(i.get("population", "Unknown"))

        data["Continents"].append(i.get("continents", [None])[0])

    return data
