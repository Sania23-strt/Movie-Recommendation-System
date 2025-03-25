import joblib
import streamlit as st 
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path', None)  # Handle missing poster
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750.png?text=No+Image"
    
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found in dataset!")
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters
st.header("Movie Recommendation System using ML")
 
movies=joblib.load('artifacts/movie_list.pkl','rb')
similarity=joblib.load('artifacts/similarity.pkl','rb')

movie_list=movies['title'].values
selected_movie=st.selectbox(
    'Type/select movie to get recommendation',
    movie_list
)
if st.button('Show Some Recommendations Bro!'):
    recommended_movies_name,recommended_movies_poster=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])


