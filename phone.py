import requests
import pandas as pd
from datetime import datetime, timedelta

baseURL = "https://api.ftc.gov/"
endpoint = "v0/dnc-complaints"
api_key = "vwraVTew14HekZGmAsbJKzj7dSkSpacMcUX4PeMx"

items_per_page = 50

# Step 1: Automate Date Selection
yesterday = datetime.now() - timedelta(1)
created_date = yesterday.strftime('%Y-%m-%d')

# Step 2: Read Existing Data
try:
    df_existing = pd.read_csv('data/data_combined.csv')
except FileNotFoundError:
    df_existing = pd.DataFrame()

offset = 0
data_list = []

while True:
    params = {
        "api_key": api_key,
        "created_date": created_date,
        "items_per_page": items_per_page,
        "offset": offset
    }

    response = requests.get(baseURL + endpoint, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    data = response.json()
    # print(data)
    if len(data['data']) == 0:
        break
    data_list.extend([item['attributes'] for item in data['data']])
    offset += items_per_page

df_new = pd.DataFrame(data_list)

# Step 3: Append New Data
df_updated = pd.concat([df_existing, df_new], ignore_index=True)

# Remove duplicates
df_updated = df_updated.drop_duplicates()

# Step 4: Save the Updated Data
df_updated.to_csv('data/data_combined.csv', index=False)
# print("Data has been successfully retrieved and saved to combined.csv.")

class Phone():
    def search_phone_number(self, phone_number):
        # user_input = input("Enter a phone number to search: ")
        # phone_number = str(user_input)
        df = pd.read_csv('data/data_combined.csv')
        matches = df.loc[df['company-phone-number'] == phone_number]

        if matches.empty:
            print(f"No matches found for phone number: {phone_number}")
            return f"No matches found for phone number: {phone_number}"
            # return None
        else:
            print(f"Matches found for phone_number {phone_number}:")
            print(matches['subject'])
            return f"Matches found for phone number {phone_number}: " + matches['subject']

# Uncomment below line to simply run this file
# Phone().search_phone_number("45677677987")
