
from Hako.Console.Command import Command

class TestCommand(Command):
    def __init__(self):
        self.signature = '''test'''

    def handle(self):
        self.info('Running tests... ⌛')
        self.warn('WORK IN PROGRESS - load tests from app and run them')

        # Call another command
        self.call('route:list')

        # Something like this:
        # import unittest
        # import test.test_prog
        # suite = unittest.TestLoader().loadTestsFromModule(test.test_prog)
        # unittest.TextTestRunner().run(suite