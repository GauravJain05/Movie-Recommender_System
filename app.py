from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
import os
import gdown
from urllib.parse import quote

app = Flask(__name__)

API_KEY = os.environ.get("TMDB_API_KEY")

if API_KEY:
    print("✅ TMDB API key loaded")
else:
    print("⚠️ TMDB API key NOT found — posters disabled")


MODEL_URL = "https://drive.google.com/uc?id=17n9kKc-_FHtPrO_Ssv-DB6c89dfwYIlC"
MODEL_PATH = "model/model.pkl"


def download_model():
    if not os.path.exists(MODEL_PATH):
        print("⬇ Downloading model from Google Drive...")
        os.makedirs("model", exist_ok=True)
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
        print("✅ Model downloaded.")


download_model()

data = pickle.load(open(MODEL_PATH, 'rb'))
movies = data['movies']
similarity = data['similarity']

poster_cache = {}


def fetch_poster(movie_title):
    if not API_KEY:
        return None

    if movie_title in poster_cache:
        return poster_cache[movie_title]

    movie_title_encoded = quote(movie_title)

    search_url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}&query={movie_title_encoded}"
    )

    try:
        response = requests.get(search_url, timeout=5)
        data = response.json()

        poster_url = None

        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                poster_url = "https://image.tmdb.org/t/p/w500" + poster_path

        poster_cache[movie_title] = poster_url
        return poster_url

    except requests.exceptions.RequestException as e:
        print("TMDB error:", e)
        return None


def recommend(movie):
    movie = movie.strip()

    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_names = []
    movie_posters = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        movie_names, movie_posters = recommend(selected_movie)

    return render_template(
        'index.html',
        movies=movies['title'].values,
        movie_names=movie_names,
        movie_posters=movie_posters
    )

if __name__ == '__main__':
    app.run(debug=True)
