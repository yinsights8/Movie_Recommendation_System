import streamlit as st
import pickle
import difflib
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=0b49f5abe3eefb68ea91ccc14b3bc91d&language=en-US".format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie_name):
    find_colse_match = difflib.get_close_matches(movie_name, movies_list)[0]
    index_of_movies = movies[movies['title'] == find_colse_match].index.values[0]

    similarity_score = list(enumerate(similarity[index_of_movies]))
    sort_similarities_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:6]

    recommend_movies_names = []
    recommended_movie_posters = []
    for i in sort_similarities_movies:
        movie_id = movies.iloc[i[0]].id
        # print(movie_id)
        recommend_movies_names.append(movies.iloc[i[0]].title)

        # fetch poster from tmdb
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommend_movies_names,recommended_movie_posters


path = "E:\My_Model\Project Under Construction\movie_recommender\models"
movies = pickle.load(open(f"{path}\movies.pkl", "rb"))
movies_list = movies["title"].values
similarity = pickle.load(open(f"{path}\similarity.pkl", "rb"))

st.title("Movies Recommender System")

selected_movie = st.selectbox("Enter the Movie Name", movies_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    # num_columns = 30
    # for i in range(num_columns):
    #     with st.columns(num_columns)[i]:
    #         st.header(names[i])
    #         st.image(posters[i])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


