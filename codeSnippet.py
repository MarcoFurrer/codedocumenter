import requests
import json
import pandas as pd
from time import sleep
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load JSON data
with open('appointment.json', 'r') as file:
    json_data = json.load(file)

# Load DataFrame from Excel
df = pd.read_excel('appointment.xlsx', sheet_name='Termine')

# Function to update JSON data with DataFrame values
def set_params(df, json_data, index=0):
    begin_time = df["begin"].iloc[0]
    begin_time = df["begin"].iloc[index]
    end_time = begin_time + pd.Timedelta(minutes=df["duration"].iloc[index])
    json_data["properties"]["title"] = df["title"].iloc[index]
    json_data["properties"]["begin"] = df["begin"].iloc[index].strftime('%Y-%m-%d %H:%M:%S')
    json_data["properties"]["end"] = end_time.strftime('%Y-%m-%d %H:%M:%S')
    json_data["properties"]["duration"] = int(df["duration"].iloc[index])
    json_data["properties"]["place"] = df["place"].iloc[index]
    json_data["properties"]["description"] = df["description"].iloc[index]
    return json_data

# Update JSON data
json_data = set_params(df, json_data)
print(json.dumps(set_params(df, json_data)))

def set_termin(df, json_data):
    # Get API key from environment variable
    api_key = os.getenv('WEBLING_API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")

    # Correct API endpoint URL
    url = f"url={api_key}"

    # Post updated JSON data
    response = requests.post(url, json=json_data)

    # Check if the request was successful
    if response.status_code == 201:
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")   

for i in range(len(df)):
    json_data = set_params(df, json_data, i)
    set_termin(df, json_data)