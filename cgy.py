import requests
import pandas as pd

# Fetch data from the API
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
countries = response.json()

# Extract the required data
data = {
    "Country name": [],
    "Independence": [],
    "United Nation members": [],
    "startOfWeek": [],
    "Official country name": [],
    "Common native name": [],
    "Currency Code": [],
    "Currency name": [],
    "Currency symbol": [],
    "Country code (IDD)": [],
    "Capital": [],
    "Region": [],
    "Sub region": [],
    "Languages": [],
    "Area": [],
    "Population": [],
    "Continents": []
}

for country in countries:
    # Country name
    data["Country name"].append(country.get("name", {}).get("common", "N/A"))
    
    # Independence
    data["Independence"].append(country.get("independent", "N/A"))
    
    # United Nation members
    data["United Nation members"].append(country.get("unMember", "N/A"))
    
    # startOfWeek
    data["startOfWeek"].append(country.get("startOfWeek", "N/A"))
    
    # Official country name
    data["Official country name"].append(country.get("name", {}).get("official", "N/A"))
    
    # Common native name
    native_names = country.get("name", {}).get("nativeName", {})
    if native_names:
        # Get the first native name entry
        first_native_name = next(iter(native_names.values()))
        data["Common native name"].append(first_native_name.get("common", "N/A"))
    else:
        data["Common native name"].append("N/A")
    
    # Currency Code, Currency name, and Currency symbol
    currencies = country.get("currencies", {})
    if currencies:
        # Get the first currency entry
        first_currency = next(iter(currencies.values()))
        data["Currency Code"].append(first_currency.get("name", "N/A"))
        data["Currency name"].append(first_currency.get("name", "N/A"))
        data["Currency symbol"].append(first_currency.get("symbol", "N/A"))
    else:
        data["Currency Code"].append("N/A")
        data["Currency name"].append("N/A")
        data["Currency symbol"].append("N/A")
    
    # Country code (IDD)
    idd = country.get("idd", {})
    root = idd.get("root", "")
    suffixes = idd.get("suffixes", [])
    if root and suffixes:
        country_code = root + ''.join(suffixes)
        data["Country code (IDD)"].append(country_code)
    else:
        data["Country code (IDD)"].append("N/A")
    
    # Capital
    data["Capital"].append(country.get("capital", ["N/A"])[0])
    
    # Region
    data["Region"].append(country.get("region", "N/A"))
    
    # Sub region
    data["Sub region"].append(country.get("subregion", "N/A"))
    
    # Languages
    languages = country.get("languages", {})
    if languages:
        language_list = ', '.join(languages.values())
        data["Languages"].append(language_list)
    else:
        data["Languages"].append("N/A")
    
    # Area
    data["Area"].append(country.get("area", "N/A"))
    
    # Population
    data["Population"].append(country.get("population", "N/A"))
    
    # Continents
    continents = country.get("continents", [])
    if continents:
        data["Continents"].append(', '.join(continents))
    else:
        data["Continents"].append("N/A")

# Create DataFrame
df = pd.DataFrame(data)

# Set index to start from 1
#df.index = df.index + 1

# Save DataFrame to CSV file
csv_file_path = "countries_data1.csv"
df.to_csv(csv_file_path)

print(f"Data saved to {csv_file_path}")
print(df.head(10))
d