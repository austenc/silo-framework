import os
from werkzeug.wsgi import SharedDataMiddleware
from Hako.Routing import Router

class App:
    def __init__(self, routes, app_path):
        self.routes = routes
        self.app_path = app_path

    def wsgi_app(self, environ, start_response):
        response = Router(self.routes).dispatch_request(environ)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
            '/':  os.path.join(os.path.dirname(self.app_path), 'public')
        })
        return self.wsgi_app(environ, start_response)