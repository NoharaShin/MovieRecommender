import logging
import os
from pathlib import Path

import tornado.ioloop
import tornado.log
import tornado.web
import yaml

from handlers.main_handler import MainHandler

APP_PATH = Path(os.path.abspath(__file__)).parent
APP_CONF = os.path.join(APP_PATH, 'conf', 'movie_recommender.yaml')


class MovieRecommenderApplication(tornado.web.Application):
    def __init__(self, debug=True, autoreload=True):
        """
        :param debug:
        :type debug: bool
        :param autoreload:
        :type autoreload: bool
        """
        handlers = [
            (r'/', MainHandler)
        ]

        settings = {
            'template_path': os.path.join(APP_PATH, 'view', 'templates'),
            'static_path': os.path.join(APP_PATH, 'view', 'static'),
            'debug': debug,
            'autoreload': autoreload
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    with open(APP_CONF) as f:
        conf = yaml.safe_load(f)

    port = conf.get('api').get('port')
    app = MovieRecommenderApplication()
    app.listen(port)

    tornado.log.enable_pretty_logging()
    logging.info(f'API `MovieRecommender` running on port {port}...')
    tornado.ioloop.IOLoop.current().start()
