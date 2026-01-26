from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
import os

API_KEY = os.environ.get("TMDB_API_KEY")


app = Flask(__name__)


# 📦 Load saved model
data = pickle.load(open('model/model.pkl', 'rb'))
movies = data['movies']          # DataFrame
similarity = data['similarity']  # Similarity matrix


# 🎬 Fetch poster using MOVIE TITLE (not movie_id)
def fetch_poster(movie_title):
    movie_title = movie_title.replace(" ", "+")  # safe for URL

    search_url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}&query={movie_title}"
    )

    try:
        response = requests.get(search_url, timeout=5)
        data = response.json()

        if data.get('results'):
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except requests.exceptions.RequestException as e:
        print("TMDB error:", e)
        return None


# 🤖 Recommendation logic
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


# 🌐 Flask route
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


# ▶ Run app
if __name__ == '__main__':
    app.run(debug=True)
