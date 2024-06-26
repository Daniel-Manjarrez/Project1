import os
import openai
import requests
import json
import random
import sqlalchemy as db
import pandas as pd
from openai import OpenAI

# # Set environment variables
# my_api_key = os.getenv('OPENAI_KEY')
# openai.api_key = my_api_key

api_key = '8YQ53Ao5sqOGEq826OfsK3PqOEQBWY36Iv0KJsTx'
base_url = 'https://api.watchmode.com/v1/title/'
gpt_api = 'generate new key'

def fetch_data(api_key, search_query):
    url = f"{base_url}{search_query}/details/?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def chatGPT_summary(my_api_key, message):
    # Create an OpenAPI client using the key from our environment variable
    client = OpenAI(
        api_key=my_api_key,
    )

    # Specify the model to use and the messages to send
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a movie critic giving an unbiased overview of a specific movie to get someone else to watch it"},
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':

    df = pd.read_csv('title_id_map.csv', dtype={'Year': 'string'})
    title = input("Please enter a movie title: ")
    results = df[df['Title'] == title]
    id = int(results['Watchmode ID'].iloc[0])

    # Fetch data from Watchmode API
    data = fetch_data(api_key, id)
    print(data)
    # similar_movies = []
    # for title_id in data['similar_titles']:
    #     title_result = df[df['Watchmode ID'] == title_id]
    #     movie = title_result['Title'].iloc[0]
    #     similar_movies.append(movie)

    # if len(similar_movies) > 2:
    #     random_indices = random.sample(range(0, len(similar_movies) - 1), 3)
    #     for index in random_indices:
    #         print(f"Summary for {similar_movies[index]}: ")
    #         print(chatGPT_summary(gpt_api, f"Explain this movie: {similar_movies[index]}"))
    #         print()
    # elif not similar_movies:
    #     for movie in similar_movies:
    #         print(f"Summary for {movie}: ")
    #         print(chatGPT_summary(gpt_api, f"Explain this movie: {movie}"))
    #         print()
    # else:
    #     print("No similar titles found!")
