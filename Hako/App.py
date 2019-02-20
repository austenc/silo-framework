from Hako.Routing import Router

class App:
    def __init__(self, routes):
        self.routes = routes

    def wsgi_app(self, environ, start_response):
        response = Router(self.routes).dispatch_request(environ)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)