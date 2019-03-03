from werkzeug.routing import Rule
import inflect


class Route:
    def __init__(self):
        self.url = None
        self.action = None
        self._name = None
        self.methods = ['HEAD', 'GET']

    def get(self, url, action):
        return self.match(['HEAD', 'GET'], url, action)

    def post(self, url, action):
        return self.match(['POST'], url, action)

    def put(self, url, action):
        return self.match(['PUT'], url, action)

    def patch(self, url, action):
        return self.match(['PATCH'], url, action)

    def delete(self, url, action):
        return self.match(['DELETE'], url, action)

    def match(self, methods, url, action):
        return self.setup(url, action, methods=methods)
    
    def resource(self, model, controller):
        return Resource(model, controller)
    
    def name(self, value):
        self._name = value
        return self

    def setup(self, url, action, **options):
        self.url = url if url.startswith('/') else '/' + url
        self.action = action
        self.__dict__.update(options)
        return self


class Resource:
    def __init__(self, model, controller):
        str = inflect.engine()
        self.plural = str.plural(model) if str.singular_noun(model) == False else model
        self.model = str.singular_noun(self.plural)
        self.controller = controller
        self.endpoints = {
            'index': Route().get(self.plural, self.controller+'@index').name(self.plural+'.index'),
            'create': Route().get(self.plural+'/create', self.controller+'@create').name(self.plural+'.create'),
            'store': Route().post(self.plural, self.controller+'@store').name(self.plural+'.store'),
            'show': Route().get(self.plural+'/{'+self.model+'}', self.controller+'@show').name(self.plural+'.show'),
            'edit': Route().get(self.plural+'/{'+self.model+'}/edit', self.controller+'@edit').name(self.plural+'.edit'),
            'update': Route().match(['PUT', 'PATCH'], self.plural+'/{'+self.model+'}', self.controller+'@update').name(self.plural+'.update'),    
            'destroy': Route().delete(self.plural+'/{'+self.model+'}', self.controller+'@destroy').name(self.plural+'.destroy')
        }

    def routes(self):
        return list(self.endpoints.values())

    def keys(self):
        return list(self.endpoints.keys())
    
    def exclude(self, verbs):
        self.endpoints = {k: v for k, v in self.endpoints.items() if k not in verbs}
        return self
        
    def only(self, verbs):
        self.endpoints = {key: self.endpoints[key] for key in verbs}
        return self
    
    def api(self):
        self.exclude(['create', 'edit'])
        return self
