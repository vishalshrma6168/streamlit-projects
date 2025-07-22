# pip install streamlit pandas scikit-learn requests
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movie data
movies = pd.read_csv("movies.csv")

# Fill NaNs
movies["overview"] = movies["overview"].fillna("")

# Vectorize the overview text
vectorizer = TfidfVectorizer(stop_words='english')
overview_vectors = vectorizer.fit_transform(movies["overview"])

# Compute similarity matrix
similarity = cosine_similarity(overview_vectors)

# Recommend function
def recommend(movie_title):
    try:
        index = movies[movies["title"] == movie_title].index[0]
        distances = similarity[index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended = [movies.iloc[i[0]].title for i in movie_list]
        return recommended
    except:
        return []

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation System")
st.write("Select a movie to get recommendations")

movie_selected = st.selectbox("Choose a Movie", movies["title"].values)

if st.button("Recommend"):
    results = recommend(movie_selected)
    if results:
        st.subheader("You might also like:")
        for i, movie in enumerate(results, start=1):
            st.write(f"{i}. {movie}")
    else:
        st.error("Movie not found in database.")
