# 🎬 Movie Recommendation System

A content-based movie recommendation system built using **Python**, **Flask**, and **Machine Learning**.  
The application recommends movies similar to a selected movie based on content similarity and displays movie posters using the TMDB API.

---

## 📌 Features

- Content-based movie recommendations
- Cosine similarity for measuring movie similarity
- Flask-based web application
- TMDB API integration for movie posters
- Clean and responsive user interface
- Secure handling of API keys using environment variables

---

## 🧠 How It Works

1. Movie metadata is processed and vectorized.
2. Cosine similarity is used to compute similarity between movies.
3. When a user selects a movie, the system recommends the top 5 similar movies.
4. Movie posters are fetched dynamically using the TMDB API.

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Pandas**
- **Scikit-learn**
- **NumPy**
- **HTML / CSS**
- **TMDB API**

---

## 📂 Project Structure

```text
Movie-Recommender_System/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── model/
│   └── (model file not included)
└── movie_recommendation_system.ipynb

