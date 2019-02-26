import argparse
import importlib
import pkgutil
import os.path
from Hako.Console.Parser import Parser


class Kernel:
    def __init__(self, app_path):
        self.app_path = os.path.dirname(app_path) + '/commands'
        self.framework_path = os.path.join(os.path.dirname(__file__), './Commands')
        self.commands = []
    
    def handle(self):
        self.commands = self.load_commands()
        parent = argparse.ArgumentParser(description='Zen CLI', add_help=False)
        parent.add_argument('command', help='Name of the command you would like to run.')
        args, unknown = parent.parse_known_args()

        try:
            cmd = self.commands[args.command]
            if cmd['params']:
                parser = argparse.ArgumentParser(prog=cmd['module'].__name__)
                parser.add_argument('command', help=argparse.SUPPRESS)
                for key, param in cmd['params'].items():
                    param.to_args(parser)
            
            cmd_args, unknown_cmd_args = parser.parse_known_args()
            # print(cmd_args)
            # Todo: use argparse to add command-specific arguments and options here
            # cmd['module']().handle()
        except KeyError as e:
            print('Command "%s" not found, is it registered?' % (args.command))
            # raise e ?

    def load_commands(self, prefix='commands.'):
        from_framework = self.load_from_path(self.framework_path)
        from_app = self.load_from_path(self.app_path, prefix=prefix)
        return {**from_framework, **from_app}

    def load_from_path(self, path, prefix='Hako.Console.Commands.'):
        loaded = {}
        packages = pkgutil.walk_packages([path], prefix)
        for finder, modname, ispkg in packages:
            if not ispkg:
                module = importlib.import_module(modname)
                instance = getattr(module, modname.split('.')[-1])
                cmd = instance()
                name, params = Parser.parse(cmd.signature)
                loaded[name] = {
                    'module': instance,
                    'name': name,
                    'params': params,
                    'signature': cmd.signature,
                    'description': 'example description'
                }
        return loaded
