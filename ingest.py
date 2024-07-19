import requests  # Importing the 'requests' module to make HTTP requests
import pandas as pd  # Importing the 'pandas' library for data manipulation
import json # Importing the 'json' module to work with JSON data
import time

url = "https://restcountries.com/v3.1/all" # URL of the API endpoint

# Function to make a GET request to the API and fetch data
def get_request():
    response = requests.get(url) # Making a GET request
    res = response.json() # Parsing the JSON response into a Python dictionary
    return res
#df = pd.DataFrame(res['results'][0])
    
# Function to format the response data into a structured format    
def format_reponse(res):
    result = res['results'][0] # Extracting the first result from the response
    return result


def stream_data():
    resp = get_request() # Fetching data from the API
    res = format_reponse(resp) # Formatting the fetched data
    #data = json.dumps(res, indent = 3) # Converting formatted data into JSON format
    return res



json_data = stream_data()


data = {}
#formatting the data and passing into the empty dictionary
data["first_name"] = [json_data["name"]["first"]]
data["last_name"] = [json_data["name"]["last"]]
data["title"] = [json_data["name"]["title"]]
data["gender"] = [json_data["gender"]]
data["address"] = f'{[json_data["location"]["street"]["number"]]} {[json_data["location"]["street"]["name"]]}'
data["city"] = [json_data["location"]["city"]]
data["state"] = [json_data["location"]["state"]]
data["country"] = [json_data["location"]["country"]]
data["postal_code"] = [json_data["location"]["postcode"]]
data["timezone"] = [json_data["location"]["timezone"]["offset"]]
data["email"] = [json_data["email"]]
data["date_of_birth"] = [json_data["dob"]["date"]]
data["age"] = [json_data["dob"]["age"]]
data["profile_picture"] = [json_data["picture"]["large"]]
data["nationality"] = [json_data["nat"]]




# Function to stream data by fetching, formatting, and returning it as JSON


# print(stream_data()) # Printing the streamed data in JSON format
df = pd.DataFrame(data)