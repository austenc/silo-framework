import importlib
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map
from werkzeug.routing import Rule
from Hako.Routing.Route import Resource

class Router:
    def __init__(self, routes):
        self.routes = self.parse_routes(routes)
        self.mapped_routes = Map(list(map(self.make_rule, self.routes)))
        self.request = None

    def dispatch_request(self, environ):
        self.request = Request(environ)
        urls = self.mapped_routes.bind_to_environ(self.request.environ)
        try:
            endpoint, values = urls.match()
            return self.call_endpoint(endpoint, **values)
        except NotFound as e:
            print(e)
            return self.error_404()
        except HTTPException as e:
            return e
    
    def parse_url(self, url):
        return url.replace('{', '<').replace('}', '>')

    def parse_endpoint(self, endpoint):
        return endpoint.split('@')[0], endpoint.split('@')[-1]

    def make_rule(self, route):
        return Rule(self.parse_url(route.url), endpoint=route.action, methods=route.methods)
    
    def parse_routes(self, routes):
        converted = []
        for route in routes:
            if isinstance(route, Resource):
                converted.extend(route.routes())
            else:
                converted.append(route)
        return converted     

    def call_endpoint(self, endpoint, **values):
        # Is this endpoint callable?
        if (callable(endpoint)):
            return Response(endpoint(self.request, **values))

        # Otherwise we probably have a controller and action
        try:
            controller, action = self.parse_endpoint(endpoint)
            module = importlib.import_module('controllers.' + controller)
        except ImportError as e:
            print("\n[ERROR]: Could not find controller - "+controller+"\n")
            return e

        try:
            return Response(getattr(module, action)(self.request, **values))

        except Exception as e:
            print("\n[ERROR]: Problem when calling '"+action+"' method of "+controller)
            print(e.args)
            return e

    def error_404(self):
        return Response('Error 404 - Page Not Found')
