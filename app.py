import requests
import json
import sqlalchemy as db
import pandas as pd

api_key = '8YQ53Ao5sqOGEq826OfsK3PqOEQBWY36Iv0KJsTx'
base_url = 'https://api.watchmode.com/v1/title/'


def fetch_data(api_key, search_query):
    url = f"{base_url}{search_query}/details/?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


if __name__ == '__main__':
    
    df = pd.read_csv('title_id_map.csv', dtype={'Year': 'string'})
    title = input("Please enter a movie title: ")
    results = df[df['Title'] == title]
    id = int(results['Watchmode ID'].iloc[0])

    # Fetch data from Watchmode API
    data = fetch_data(api_key, id)
    print(data['similar_titles'])
