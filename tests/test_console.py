import os
import unittest
from Silo.Console.Command import Command
from Silo.Console.Kernel import Kernel
from Silo.Console.Parser import Parser
from argparse import Namespace


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = Command()
        self.cmd.signature = 'example:cmd { arg1 } {--opt1}'
        name, params = Parser.parse(self.cmd.signature)
        self.cmd._params = params
        self.cmd._values = Namespace(arg1='test arg1', opt1='test opt1')

    def test_can_get_all_arguments(self):
        self.assertTrue('arg1' in self.cmd.arguments())
        self.assertTrue('opt1' not in self.cmd.arguments())
        self.assertEqual(self.cmd.arguments()['arg1'], 'test arg1')

    def test_can_get_single_argument(self):
        self.assertEqual(self.cmd.argument('arg1'), 'test arg1')
        self.assertEqual(self.cmd.argument('other'), None)

    def test_can_get_all_options(self):
        self.assertTrue('opt1' in self.cmd.options())
        self.assertTrue('arg1' not in self.cmd.options())
        self.assertEqual(self.cmd.options()['opt1'], 'test opt1')

    def test_can_get_single_option(self):
        self.assertEqual(self.cmd.option('opt1'), 'test opt1')
        self.assertEqual(self.cmd.option('other'), None)


class TestConsoleKernel(unittest.TestCase):
    def test_loads_commands_from_framework(self):
        loaded = Kernel(__file__).load_commands('tests.commands.')
        self.assertTrue('route:list' in loaded)

    def test_loads_commands_from_app(self):
        loaded = Kernel(__file__).load_commands('tests.commands.')
        self.assertTrue('example:cmd' in loaded)


class TestConsoleParser(unittest.TestCase):
    def test_parse_command_only(self):
        command, args = Parser.parse('cmd:name ')
        self.assertEqual(command, 'cmd:name')

    def test_parse_description(self):
        command, args = Parser.parse('cmd:name {example : Example desc }')
        self.assertEqual(command, 'cmd:name')
        self.assertEqual('Example desc', args['example'].description)

    def test_parse_arguments_and_options(self):
        command, args = Parser.parse('cmd:name {argument} {--option}')
        self.assertEqual(command, 'cmd:name')
        self.assertEqual('argument', args['argument'].name)
        self.assertEqual('option', args['option'].name)

    def test_parse_optional_argument_and_default_value(self):
        command, args = Parser.parse('cmd:name {arg1?} {arg2=testing}')
        self.assertEqual(command, 'cmd:name')
        self.assertEqual('arg1', args['arg1'].name)
        self.assertTrue(args['arg1'].is_optional)
        self.assertIsNone(args['arg1'].default)
        self.assertEqual('arg2', args['arg2'].name)
        self.assertTrue(args['arg2'].is_optional)
        self.assertEqual('testing', args['arg2'].default)

    def test_parse_option_with_default_value(self):
        command, args = Parser.parse('cmd:name {--opt : desc} {--opt2=test}')
        self.assertEqual(command, 'cmd:name')
        self.assertEqual('opt', args['opt'].name)
        self.assertEqual('desc', args['opt'].description)
        self.assertTrue(args['opt'].is_optional)
        self.assertEqual('opt2', args['opt2'].name)
        self.assertEqual('test', args['opt2'].default)
        self.assertTrue(args['opt2'].is_optional)

    def test_parse_option_with_shortcut(self):
        command, args = Parser.parse('cmd:name {--O|opt : description}')
        self.assertEqual(command, 'cmd:name')
        self.assertEqual('opt', args['opt'].name)
        self.assertEqual('O', args['opt'].shortcut)
        self.assertEqual('description', args['opt'].description)
        self.assertTrue(args['opt'].is_optional)
