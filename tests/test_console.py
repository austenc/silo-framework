import unittest
import os
from Hako.Console.Kernel import Kernel
from Hako.Console.Parser import Parser


class TestConsoleKernel(unittest.TestCase):
    def test_loads_commands_from_framework(self):
        path = os.path.join(os.path.dirname(__file__), '../Hako/Console/Commands')
        loaded = Kernel(__file__).load_from_path(path)
        print(loaded)
        # // get files from directory, test that each name is in loaded commands


# class TestConsoleParser(unittest.TestCase):
#     def test_parse_command_only(self):
#         command, args = Parser.parse('cmd:name ')
#         self.assertEqual(command, 'cmd:name')

#     def test_parse_description(self):
#         command, args = Parser.parse('cmd:name {example : Example description }')
#         self.assertEqual(command, 'cmd:name')
#         self.assertEqual('Example description', args['example'].description)

#     def test_parse_arguments_and_options(self):
#         command, args = Parser.parse('cmd:name {argument} {--option}')
#         self.assertEqual(command, 'cmd:name')
#         self.assertEqual('argument', args['argument'].name)
#         self.assertEqual('option', args['option'].name)
    
#     def test_parse_optional_argument_and_default_value(self):
#         command, args = Parser.parse('cmd:name {arg1?} {arg2=testing}')
#         self.assertEqual(command, 'cmd:name')
#         self.assertEqual('arg1', args['arg1'].name)
#         self.assertTrue(args['arg1'].is_optional)
#         self.assertIsNone(args['arg1'].default)
#         self.assertEqual('arg2', args['arg2'].name)
#         self.assertTrue(args['arg2'].is_optional)
#         self.assertEqual('testing', args['arg2'].default)

#     def test_parse_option_with_default_value(self):
#         command, args = Parser.parse('cmd:name {--opt : description} {--opt2=testing}')
#         self.assertEqual(command, 'cmd:name')
#         self.assertEqual('opt', args['opt'].name)
#         self.assertEqual('description', args['opt'].description)
#         self.assertTrue(args['opt'].is_optional)
#         self.assertEqual('opt2', args['opt2'].name)
#         self.assertEqual('testing', args['opt2'].default)
#         self.assertTrue(args['opt2'].is_optional)

#     def test_parse_option_with_shortcut(self):
#         command, args = Parser.parse('cmd:name {--O|opt : description}')
#         self.assertEqual(command, 'cmd:name')
#         self.assertEqual('opt', args['opt'].name)
#         self.assertEqual('O', args['opt'].shortcut)
#         self.assertEqual('description', args['opt'].description)
#         self.assertTrue(args['opt'].is_optional)
