import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommendation System')
movies = pickle.load(open('./movies.pkl', 'rb'))
similarity = pickle.load(open('./similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
