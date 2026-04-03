import streamlit as st
import pickle
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🎨 UI Styling
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.main { background-color: #0e1117; }
h1 { text-align: center; color: #ff4b4b; }
.movie-card {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 🔐 API Key
API_KEY = "a3ba3105b1a3c9705c98d1c91efdf428"


# 🎬 Fetch Poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# 📦 Load Data
movies = pickle.load(open('movies.pkl', 'rb'))


# 🔥 Compute Similarity (SAFE VERSION)
@st.cache_data
def compute_similarity(movies):
    movies['tags'] = movies['tags'].fillna('').astype(str)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()

    return cosine_similarity(vectors)


similarity = compute_similarity(movies)


# 🎯 Recommendation Function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# 🎨 UI
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.write(names[i])