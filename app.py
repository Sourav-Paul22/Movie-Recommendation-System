import streamlit as st
import pickle
import pandas as pd
import base64
import requests
from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def fetch_posters(movie_id):
    # api_key = "f1d66794f004465a371e164fe664da74"  # Replace with your TMDB API key
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f1d66794f004465a371e164fe664da74&language=en-US".format(movie_id)
    # st.write(url)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            poster_url = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            return poster_url
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster+Available"
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/300x450?text=Timeout+Error"
    except requests.exceptions.RequestException as e:
        return f"https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    mov_ind = movies[movies['title'] == movie].index[0]
    distances = similarity[mov_ind]
    mov_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies_posters = []
    recommended_movies = []

    for i in mov_list:
        mov_id = movies.iloc[i[0]].movie_id
        #fetching poster
        poster_url = fetch_posters(mov_id)
        recommended_movies_posters.append(poster_url)
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


movieDict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movieDict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Sidebar Content
with st.sidebar:
    # Display Cover Image
    st.image('./icons/image.png', width=250)

    # Title and Links
    st.markdown("<h2 style='text-align: center;'>Movie Recommendation System</h2>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://github.com/Sourav-Paul22" target="_blank">
                <img src="https://skillicons.dev/icons?i=github" alt="GitHub" style="height: 50px; margin-right: 10px;"/>
            </a>
            <a href="https://github.com/Sourav-Paul22/Movie-Recommendation-System" target="_blank">
                <img src="https://img.shields.io/badge/github-repo-white" alt="repo"/>
            </a>
            <a href="https://colab.research.google.com/drive/1XCFg3jcTL70S4mYXXfalA_s-OVUE6E5c?usp=chrome_ntp" target="_blank">
                <img src="https://img.shields.io/badge/colab-notebook-orange" alt="Colab"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.header('Movie Recommender System', divider="red")
titles_list = movies['title'].tolist()
titles_list.insert(0, "search")

selected_movie_name = st.selectbox(
    "What are you looking for today?",
    titles_list,
)
st.write("You selected:", selected_movie_name)
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

    for i in range(2):
        st.markdown('#')
    st.markdown('#####')
    st.markdown('---')

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.empty()
        st.empty()
        st.markdown("<a href='https://docs.streamlit.io/'><img src='data:image/png;base64,{}' class='img-fluid' width=100%/></a>".format(img_to_bytes('./icons/streamlit.png')), unsafe_allow_html=True)
    with col2:
        st.markdown("<a href='https://www.themoviedb.org/'><img src='data:image/png;base64,{}' class='img-fluid' width=60%/></a>".format(img_to_bytes('./icons/tmdb.png')), unsafe_allow_html=True)
    with col3:
        st.markdown("<a href='https://colab.google/'><img src='data:image/png;base64,{}' class='img-fluid' width=50%/></a>".format(img_to_bytes('./icons/colab.png')), unsafe_allow_html=True)