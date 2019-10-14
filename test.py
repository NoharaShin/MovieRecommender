import sys

from engine.content_based import ContentBasedRecommender


if __name__ == '__main__':
    # Get the movie to get similar movies recommendation for from terminal
    movie = sys.argv[1]
    features = ['keywords', 'cast', 'genres', 'director']

    content_based = ContentBasedRecommender()
    similar_movies = content_based.get_similar_movies(movie, features)

    print(f'Top 10 similar movies to {movie}:')
    for similar_movie in similar_movies:
        print(f'\t{similar_movie}')
