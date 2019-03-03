
from Silo.Console.Command import Command

class TestCommand(Command):
    signature = '''test'''

    def handle(self):
        self.info('Running tests... ⌛')
        self.warn('WORK IN PROGRESS - load tests from app and run them')

        # Call another command
        self.call('route:list', {'arg1': 'test'})

        # Eventually... this command will run tests for the app, something like:
        # import unittest
        # import test.test_prog
        # suite = unittest.TestLoader().loadTestsFromModule(test.test_prog)
        # unittest.TextTestRunner().run(suite