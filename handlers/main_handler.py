from engine.content_based import ContentBasedRecommender
# from handlers.base_handler import BaseHandler

from tornado.web import RequestHandler

CONTENT_BASED = ContentBasedRecommender()
LIST_FEATURES = list(CONTENT_BASED.movies_df)
if 'index' in LIST_FEATURES:
    del LIST_FEATURES[LIST_FEATURES.index('index')]


class MainHandler(RequestHandler):
    def get(self):
        self.render('main.html', features=LIST_FEATURES)

    def post(self):
        try:
            movie = self.get_argument('movie_title')
            limit = int(self.get_argument('limit', '10'))
            all_args = self.request.arguments
            features = [feature.decode('utf-8') for feature in all_args.get('features')]

            similar_movies = CONTENT_BASED.get_similar_movies(movie, features, limit)
            # self.send_response({'result': similar_movies})
            self.render('result.html', movie_title=movie, result=similar_movies)
        except Exception as e:
            self.render('error.html', error_message=repr(e))
