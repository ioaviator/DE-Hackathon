#importing library needed
import requests
import pandas as pd

url = "https://restcountries.com/v3.1/all"  #country data api

response = requests.get(url)
countries_data = response.json()

# Initialize an empty dictionary to store the data
data = {"Country Name": [],
        "Independence": [],
        "United Nation members": [],
        "startOfWeek": [],
        "Official country name": [],
        "Common native name": [],
        "Currency Code": [],
        "Currency name": [],
        "Currency symbol":[],
        "Country code": [],
        "Capital": [],
        "Region": [],
        "Sub region": [],
        "Languages": [],
        "Area": [],
        "Population": [],
        "Continents": []
        }

# Loop through each country in the response
for i in countries_data:
    # Extract the common and official country names and add them to the data dictionary
    data["Country Name"].append(i.get("name", {}).get("common"))
    data["Independence"].append(i.get("independent")) #Extracting independence status
    data["United Nation members"].append(i.get("unMember")) #Extracting UN membership status
    data["startOfWeek"].append(i.get("startOfWeek")) #Extracting country week satrt day
    data["Official country name"].append(i.get("name", {}).get("official"))
    
    #Extracting natives names
    native_names = i.get("name", {}).get("nativeName", {})
    if native_names:
        # Get the first available native name
        common_native_name = list(native_names.values())[0].get("common")
    else:
        common_native_name = None
    data["Common native name"].append(common_native_name)

    #Extracting currency code,name and symbol
    currencies = i.get("currencies")
    if currencies:
        currency_codes = ", ".join(currencies.keys()) #currency code
        currency_names = ", ".join([details.get("name") for details in currencies.values()]) #currency name
        currency_symbols = ", ".join([details.get("symbol") for details in currencies.values() if details.get("symbol")]) #currency symbol
    else:
        currency_codes = None
        currency_names = None
        currency_symbols = None
    data["Currency Code"].append(currency_codes) #currency code
    data["Currency name"].append(currency_names) #currency name
    data["Currency symbol"].append(currency_symbols) #currency symbol

    #Extracting country code
    idd = i.get("idd", {})
    root = idd.get("root", "")
    suffixes = idd.get("suffixes", [])
    if root and suffixes:
        country_code = root + "".join(suffixes) #concatinating root and suffixes using join  
    else:
        country_code = None
    data["Country code"].append(country_code)

    #Extracting the Capital city
    capital = i.get("capital", [])
    if capital:
        capital_city = capital[0]
    else:
        capital_city = None
    data["Capital"].append(capital_city)

    #Extracting Region
    data["Region"].append(i.get("region"))

    #Extracting Sub Region
    data["Sub region"].append(i.get("subregion"))

    #Extracting Country Languages into a list
    languages = i.get("languages", {})
    if languages:
        languages_list = ", ".join(languages.values())
    else:
        languages_list = None
    data["Languages"].append(languages_list)

    #Extracting Country Area
    data["Area"].append(i.get("area"))

    #Extracting Country population
    data["Population"].append(i.get("population"))

    #Extracting Country continent
    continents = i.get("continents", [])
    if continents:
        continent = continents[0]
    else:
        continent = None
    data["Continents"].append(continent)


# Create a DataFrame from the data dictionary
df = pd.DataFrame(data)
print(df.head(26))

# Save DataFrame to CSV file
csv_file_path = "countries_tour_data.csv"
df.to_csv(csv_file_path)