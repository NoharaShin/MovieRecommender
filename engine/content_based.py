"""Movie recommender class that implements the content-based recommendation algorithm."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from engine.recommender import Recommender


class ContentBasedRecommender(Recommender):
    """
    Class that recommends a list of movie similar to the input movie based on the similarity of its content with
    the content of each movie of the dataset. The similarity of the content is based on the following criteria:
    'budget', 'genres', 'homepage', 'keywords', 'original_language', 'original_title', 'overview', 'popularity',
    'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages',
    'status', 'tagline', 'title', 'vote_average', 'vote_count', 'cast', 'crew', 'director'.
    """
    def __init__(self, movies_dataset_path=None):
        """
        :param movies_dataset_path: Full path to the movie dataset CSV file.
        :type movies_dataset_path: str
        """
        super().__init__(movies_dataset_path)

    def get_similar_movies(self, target_movie, features, limit=10):
        """
        Run the content-based similarity recommendation and return the movies similar to the input movie.
        :param target_movie:
        :type target_movie: str
        :param features: List of features for which the content-based similarity movie recommendation is going to run.
            The features must be included in the header of the movies dataset.
        :type: list
        :param limit: Number of similar movies to the input movie to return. Default value is set to 10 similar movies.
        :type: int
        :return: List of the movies similar to the input one.
        :rtype: list
        """
        # Creating a deep copy of the original movies dataset DataFrame to avoid unwanted operations on iy
        movies_df = self.movies_df.copy()

        # Adding a new column `combined_features` that is the concatenation of all the columns matching the features
        # we would like to base the content-based recommendation system
        movies_df['combined_features'] = ''
        for feature in features[:-1]:
            movies_df['combined_features'] += movies_df[feature] + ' '
        movies_df['combined_features'] += movies_df[features[-1]]

        count_vectorizer = CountVectorizer()
        count_matrix = count_vectorizer.fit_transform(movies_df['combined_features'])

        # Deleting the deep copy of the movies dataset to free memory, as it won't be used anymore
        del movies_df

        # Applying the cosine similarity to get the similarity score of all movies according to the provided features
        cosine_sim = cosine_similarity(count_matrix)

        movie_index = self._get_index_from_title(target_movie)
        similar_movies = list(enumerate(cosine_sim[movie_index]))

        # Get list of similar movies in descending order of similarity score
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        if self._get_title_from_index(sorted_similar_movies[0][0]) == target_movie:
            del sorted_similar_movies[0]

        if len(sorted_similar_movies) <= limit:
            return [self._get_title_from_index(movie[0]) for movie in sorted_similar_movies]

        return [self._get_title_from_index(movie[0]) for movie in sorted_similar_movies[:limit]]
