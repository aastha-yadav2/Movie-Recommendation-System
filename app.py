import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Load movie dictionary
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Download similarity.pkl from Google Drive if not present
similarity_file = 'similarity.pkl'
drive_url = 'https://drive.google.com/uc?id=1YBMtK46zJAmZ4J4dDUSsITsbbDDQOSSy'

if not os.path.exists(similarity_file):
    with st.spinner("Downloading similarity model..."):
        gdown.download(drive_url, similarity_file, quiet=False)

# Load similarity
similarity = pickle.load(open(similarity_file, 'rb'))

# Title
st.title('🎬 Movie Recommender System')

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=cb4e1e1e713c5c020fb8c20c50ee89e6&language=en-US'
    )
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/300x450.png?text=No+Poster"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Streamlit UI
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
