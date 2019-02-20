import unittest
from Hako.Routing import Route


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.url = '/example'
        self.action = 'example_controller'

    def test_define_get_route(self):
        self.assert_route_defined(self.url, self.action)

    def test_define_post_route(self):
        self.assert_route_defined(self.url, self.action, ['POST'])

    def test_define_put_route(self):
        self.assert_route_defined(self.url, self.action, ['PUT'])

    def test_define_patch_route(self):
        self.assert_route_defined(self.url, self.action, ['PATCH'])

    def test_define_delete_route(self):
        self.assert_route_defined(self.url, self.action, ['DELETE'])

    def assert_route_defined(self, url, action, methods=['HEAD', 'GET']):
        r = Route().match(methods, url, action)
        self.assertEqual(r.url, url)
        self.assertEqual(r.action, action)
        self.assertEqual(r.methods, methods)
        self.assertIsInstance(r, Route)
    
    def test_url_doesnt_get_double_leading_slash(self):
        r = Route().get('/example', 'controller')
        self.assertEqual(r.url, '/example')
        
    def test_url_gets_leading_slash_when_missing(self):
        r = Route().get('example', 'controller')
        self.assertEqual(r.url, '/example')

    def test_chain_name_method_adds_name(self):
        r = Route().get('example', 'controller').name('example.index')
        self.assertEqual(r._name, 'example.index')

