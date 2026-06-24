import streamlit as st
import pickle
import pandas as pd 
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

import requests

import os

from huggingface_hub import hf_hub_download
import shutil

if not os.path.exists("models/similarity.pkl"):
    file_path = hf_hub_download(
        repo_id="ikaushaljindal/movie_recommender-data",
        filename="similarity.pkl",
        repo_type="dataset"
    )

    shutil.copy(file_path, "../models/similarity.pkl")

def fetchPoster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

        return None

    except requests.exceptions.RequestException as e:
        print(f"Movie ID {movie_id} failed: {e}")
        return None

def recomend(movie_name):

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                reverse = True,
                key = lambda x : x[1])[1:6]

    recomendedMovies = []
    recomendedMoviesPoster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title

        print("TITLE:", title)
        print("MOVIE ID:", movie_id)

        recomendedMovies.append(title)
        recomendedMoviesPoster.append(fetchPoster(movie_id))

    return recomendedMovies, recomendedMoviesPoster



similarity = pickle.load(open('../models/similarity.pkl', 'rb'))
movies_list = pickle.load(open('../models/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
st.title("Movie Recomender System")


selected_movie_name = st.selectbox(
    'What would you like to watch?' , movies['title'].values)


if st.button("Recommend"):
        names, posters = recomend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        col = [col1, col2, col3, col4, col5]
        for i in range(5):
            with col[i]:
                st.text(names[i])

                if posters[i]:
                    st.image(posters[i])
                else:
                    st.write("No Poster")