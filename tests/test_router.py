import unittest
from werkzeug.routing import Rule
from Hako.Routing import Route, Router


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.route = Route().post('example', 'example@method')
        self.router = Router([
            self.route
        ])

    def test_url_params_parsed_correctly(self):
        self.assertEqual(self.router.parse_url('/a/{param}/b'), '/a/<param>/b')

    def test_endpoint_parsed_correctly(self):
        controller, action = self.router.parse_endpoint('abc@def')
        self.assertEqual(controller, 'abc')
        self.assertEqual(action, 'def')

    def test_routes_mapped_to_rules_on_init(self):
        self.assertIsInstance(self.router.mapped_routes._rules[0], Rule)
        self.assertEqual(len(self.router.mapped_routes._rules), 1)
        self.assertEqual(self.router.mapped_routes._rules[0].endpoint, self.route.action)

    def test_resource_mapped_to_equivalent_rules(self):
        resource = Route().resource('examples', 'example_controller')
        r = Router([resource])
        self.assertEqual(len(r.routes), 7)
