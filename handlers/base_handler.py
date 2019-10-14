import json
import os
from pathlib import Path

from tornado.web import RequestHandler
import yaml

APP_PATH = Path(os.path.abspath(__file__)).parent.parent
APP_CONF = os.path.join(APP_PATH, 'conf', 'movie_recommender.yaml')
with open(APP_CONF) as f:
    conf = yaml.safe_load(f)

CONTENT_TYPE = conf.get('api').get('content_type')
ALLOWED_ORIGIN = conf.get('api').get('allowed_origin')
ALLOWED_HEADERS = tuple(conf.get('api').get('allowed_headers'))
ALLOWED_METHODS = tuple(conf.get('api').get('allowed_method'))
AUTHORIZATION_HEADER = conf.get('api').get('authorization_header')


class BaseHandler(RequestHandler):
    """Base handler inheriting from tornado.web.RequestHandler."""

    def __init__(self, application, request):
        """
        Initialize the BaseHandler object with the HTTP access control values.
        :param application: The application used to hold handlers.
        :type application: api.WebApplication
        :param request: The request received by the API.
        :type request: request
        """
        self.initialize()
        super().__init__(application, request)

    def initialize(self, **kwargs):
        """
        Empty method to override in inheriting classes, eg. can be used to set specific headers for each Handler.
        """
        pass

    def set_default_headers(self):
        """
        Set default headers for every API endpoint inheriting BaseHandler.
        Override RequestHandler.set_default_headers().
        """
        self.set_header('Content-Type', CONTENT_TYPE)
        self.set_header('Access-Control-Allow-Origin', ALLOWED_ORIGIN)
        self.set_header('Access-Control-Allow-Headers', ','.join(ALLOWED_HEADERS))
        self.set_header('Access-Control-Allow-Methods', ','.join(ALLOWED_METHODS))

    def post(self, *args, **kwargs):
        """
        POST methods are used to create new documents for the endpoints resources.
        Successful POST methods return a 201 Created HTTP status.
        """
        self.method_not_allowed_error('POST')

    def get(self, *args, **kwargs):
        """
        GET methods are used to read or fetch resources.
        Successful GET methods return a 200 OK HTTP status.
        Unsuccessful GET methods generally return 404 Not Found or 400 Bad Request HTTP status.
        """
        self.method_not_allowed_error('GET')

    def put(self, *args, **kwargs):
        """
        PUT methods are used to replace resources.
        Successful PUT methods return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful PUT methods generally return a 404 Not Found HTTP status.
        """
        self.method_not_allowed_error('PUT')

    def patch(self, *args, **kwargs):
        """
        PATCH methods are used to update resources.
        Successful PATCH methods return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful PATCH methods generally return a 404 Not Found HTTP status.
        """
        self.method_not_allowed_error('PATCH')

    def delete(self, *args, **kwargs):
        """
        DELETE methods are used to delete resources.
        Successful DELETE methods generally return a 200 OK or a 204 No Content HTTP status.
        Unsuccessful DELETE methods generally return a 404 Not Found HTTP status.
        """
        self.method_not_allowed_error('DELETE')

    def options(self, *args, **kwargs):
        """
        Override RequestHandler.options() to provide a base endpoint for OPTIONS requests.
        Primarily used for CORS policy checking OPTIONS on the server.
        """
        self.set_status(204)
        self.finish()

    def send_response(self, data, status=200):
        """
        Send a response to the client with a RequestHandler.write operation.
        :param data: The data to send as a response.
        :type data: bytes, unicode, dict
        :param status: An HTTP status code for the response. Default value is 200.
        :type status: int
        """
        self.set_status(status)
        if not data:
            return self.finish()

        try:
            self.write(json.dumps(data))
        except (RuntimeError, TypeError):
            self.internal_server_error()

    def write_error(self, status_code, **kwargs):
        """
        Transform an error to a valid response and send it to the client.
        :param status_code: The HTTP status code for the response.
        :type status_code: int
        :param kwargs: Keyword arguments containing a `data` argument holding the error response to send.
        :type kwargs: dict
        """
        data = kwargs.get('data')
        self.send_response(data, status_code)

    def method_not_allowed_error(self, method):
        """
        Encapsulation method.
        Produce an error response when the required method is not allowed.
        """
        error = {
            'data': {
                'status': 405,
                'title': f'The method {method} is not allowed for this request.'
            }
        }
        self.write_error(error.get('data').get('status'), **error)

    def internal_server_error(self):
        """
        Encapsulation method.
        Produce an error response when there is an internal server error.
        """
        error = {
            'data': {
                'status': 500,
                'title': 'Internal Server Error'
            }
        }
        self.write_error(error.get('data').get('status'), **error)
