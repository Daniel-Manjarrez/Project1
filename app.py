from flask import Flask
from flask import render_template
import os
import openai
import requests
import json
import random
import pandas as pd
from openai import OpenAI

api_key = '8YQ53Ao5sqOGEq826OfsK3PqOEQBWY36Iv0KJsTx'
base_url = 'https://api.watchmode.com/v1/title/'
gpt_api = ""

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

def generate(user_input):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    title = user_input
    results = df[df['Title'] == title]
    id = int(results['Watchmode ID'].iloc[0])

    # Fetch data from Watchmode API
    data = fetch_data(api_key, id)
    print(data)
    similar_movies = []
    for title_id in data['similar_titles']:
        title_result = df[df['Watchmode ID'] == title_id]
        movie = title_result['Title'].iloc[0]
        similar_movies.append(movie)


    if len(similar_movies) > 2:
        random_indices = random.sample(range(0, len(similar_movies) - 1), 3)
        list_here = []
        for index in random_indices:
            list_here.append(similar_movies[index])
        return list_here
    elif not similar_movies:
        lesser_list = []
        for movie in similar_movies:
            lesser_list.append(movie)
        return lesser_list
    else:
        return []

def summaries(similar_movies):
    if len(similar_movies) > 2:
        random_indices = random.sample(range(0, len(similar_movies) - 1), 3)
        list_here = []
        for index in random_indices:
            list_here.append(chatGPT_summary(gpt_api, f"Explain this movie: {similar_movies[index]}"))
        return list_here
    elif not similar_movies:
        lesser_list = []
        for movie in similar_movies:
            lesser_list.append(chatGPT_summary(gpt_api, f"Explain this movie: {movie}"))
        return lesser_list
    else:
        return []

def convert_to_embedded_link(link):
    video_id = link.split('v=')[1]
    embedded_link = f'https://www.youtube.com/embed/{video_id}'
    return embedded_link
app = Flask(__name__)

@app.route('/')
def start():
    return render_template('input.html') # home page


@app.route('/movie/<string:title>', methods=['GET']) # GET request because just requesting info from server
def learn(title):
    item = None
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    
    suggested_titles = generate(title)
    titles_data = []
    for movie in suggested_titles:
        title_result = df[df['Title'] == movie]
        id = int(title_result['Watchmode ID'].iloc[0])
        titles_data.append(id)

    complete_data = []
    for inner_id in titles_data:
        complete_data.append(fetch_data(api_key, inner_id))
    print(complete_data)

    return render_template('movie.html', item=item, title=title, items=complete_data)

@app.route('/overview/<string:title>', methods=['GET']) # GET request because just requesting info from server
def learn2(title):
    item = None
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, 'title_id_map.csv')

    # Read the CSV file
    df = pd.read_csv(csv_file_path, dtype={'Year': 'string'})
    better_summary = chatGPT_summary(gpt_api, f"Explain this movie: {title}")

    title_result = df[df['Title'] == title]
    id = int(title_result['Watchmode ID'].iloc[0])
    data = fetch_data(api_key, id)
    print(data)
    standard_link = data['trailer']
    embedded_link = convert_to_embedded_link(standard_link)

    return render_template('main.html', item=item, title=title, movie=data, trailer=embedded_link, sum=better_summary)


@app.route('/readme', methods=['GET']) # GET request because just requesting info from server
def learn3():
    return render_template('readme.html')

if __name__ == '__main__':
   app.run(debug = True)