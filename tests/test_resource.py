import unittest
from Hako.Routing import Route


class TestResource(unittest.TestCase):
    def setUp(self):
        self.resource = Route().resource('example', 'example_controller')

    def test_routes_returns_list_of_route_objects(self):
        self.assertIsInstance(self.resource.routes(), list)
        self.assertIsInstance(self.resource.routes()[0], Route)
        self.assertEqual(
            self.resource.keys(), 
            ['index', 'create', 'store', 'show', 'edit', 'update', 'destroy']
        )

    def test_exclude_removes_endpoints(self):    
        self.resource.exclude(['show', 'destroy'])
        self.assertEqual(
            self.resource.keys(),
            ['index', 'create', 'store', 'edit', 'update']
        )

    def test_only_filters_other_endpoints(self):
        self.resource.only(['index', 'create'])
        self.assertEqual(
            self.resource.keys(),
            ['index', 'create']
        )

    def test_api_excludes_create_and_edit(self):
        self.resource.api()
        self.assertEqual(
            self.resource.keys(),
            ['index', 'store', 'show', 'update', 'destroy']
        )

    def test_model_is_inflected_when_creating_resource(self):
        self.assertEqual(self.resource.plural, 'examples')
        self.assertEqual(self.resource.model, 'example')
