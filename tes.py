import requests
import pandas as pd
import json

url = "https://restcountries.com/v3.1/all"


response = requests.get(url)
gh = response.json()
result = gh['name']

#print(result)

data = {}
data["Country name"] = [result["common"]]
