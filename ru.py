import requests
import pandas as pd

url = "https://restcountries.com/v3.1/all"

response = requests.get(url)
gh = response.json()

# Initialize an empty dictionary to store the data
data = {"Country Name": [],
        "Independence": [],
        "United Nation members": [],
        "startOfWeek": [],
        "Official country name": [],
        "Common native name": [],
        "Currency Code": [],
        "Currency name": [],
        "Currency symbol": [],
        "Country Code": [],
        "Capital": [],
        "Languages": []
        }

# Loop through each country in the response
for i in gh:
    # Extract the common and official country names and add them to the data dictionary
    data["Country Name"].append(i.get("name", {}).get("common"))
    data["Independence"].append(i.get("independent"))
    data["United Nation members"].append(i.get("unMember"))
    data["startOfWeek"].append(i.get("startOfWeek"))
    data["Official country name"].append(i.get("name", {}).get("official"))

    native_names = i.get("name", {}).get("nativeName", {})
    if native_names:
        # Get the first available native name
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

    # Extract the country calling code
    idd = i.get("idd", {})
    root = idd.get("root", "")
    suffixes = idd.get("suffixes", [])
    if root and suffixes:
        country_code = root + "".join(suffixes)
    else:
        country_code = None

    data["Country Code"].append(country_code)

    # Extract the capital city
    capital = i.get("capital", [])
    if capital:
        capital_city = capital[0]
    else:
        capital_city = None

    data["Capital"].append(capital_city)

    # Extract the languages
    languages = i.get("languages", {})
    if languages:
        languages_list = ", ".join(languages.values())
    else:
        languages_list = None

    data["Languages"].append(languages_list)

# Create a DataFrame from the data dictionary
df = pd.DataFrame(data)

print(df.head(10))
