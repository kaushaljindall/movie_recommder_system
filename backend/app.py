import streamlit as st
import pickle
import pandas as pd 

import os

print(os.getcwd())
print(os.listdir('.'))

def recomend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                reverse = True,
                key = lambda x : x[1])[1:6]

    recomendedMovies = []
    for i in movies_list:
        recomendedMovies.append(movies.iloc[i[0]].title)
    
    return recomendedMovies

similarity = pickle.load(open('../models/similarity.pkl', 'rb'))
movies_list = pickle.load(open('../models/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
st.title("Movie Recomender System")


selected_movie_name = st.selectbox(
    'What would you like to watch?' , movies['title'].values)



if st.button("Recommend"):
    recomendaton = recomend(selected_movie_name)

    for i in recomendaton:
        st.write(i)