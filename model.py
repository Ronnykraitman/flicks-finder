from playground import filter_movies
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

"""
A bit about the process:

1. tfidf model: Term Frequency - Inverse Document frequency:
Here Im creating for each movie a vector from the words in all movies plots
calculating each word frequency + making sure it gets a correct score depending on how common that word is

2. Using linear kernel function so I now have a matrix of similar vectors:
each vector (aka- movie) with all the other movies in the data frame

3. Now that we have this connection between a movie and its place in the similarity matrix,
we can filter out movies based on all the other condition the user selected

4. Taking then the similarity vector (based on the title), sorting its similar vectors by the similarity score
and then taking the first 10 movies (excluding the first one - as its the movie itself)

"""

tfidf_model = TfidfVectorizer(stop_words="english")


def _get_plot_vectors(plots: pd.Series):
    return tfidf_model.fit_transform(plots)


def _get_vectors_similarity(plot_vectors_matrix):
    return linear_kernel(plot_vectors_matrix, plot_vectors_matrix)


def _get_movie_to_similarity_index(similarities, title: pd.Series):
    return pd.Series([i for i in range(len(similarities))], index=title, name='similarity_index')


def get_recommend_movies_based_on_plot(movies, filters: dict):
    movie_title = filters["title"]
    idf_vectors = _get_plot_vectors(movies["plot"])
    similarities = _get_vectors_similarity(idf_vectors)
    mapping = _get_movie_to_similarity_index(similarities, movies["title"])
    joined: pd.DataFrame = movies.join(mapping, on="title")

    similarity_index = joined.loc[joined['title'] == movie_title, 'similarity_index'].values[0]

    movies_filtered: pd.DataFrame = filter_movies(joined, filters)

    similarity_score = list(enumerate(similarities[similarity_index]))
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    recommended_movies: list = []

    for score in similarity_score:
        index = score[0]
        title = movies_filtered[movies_filtered['similarity_index'] == index]['title'].values
        if len(title) > 0:
            recommended_movies.append(title[0])

    return recommended_movies[1:11] if recommended_movies else recommended_movies
