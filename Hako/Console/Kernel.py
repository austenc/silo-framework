import importlib
import pkgutil
import os.path


class Kernel:
    def __init__(self, app_path):
        self.app_path = app_path
        self.framework_path = os.path.join(
            os.path.dirname(__file__), 
            './Commands'
        )
        # self.commands = self.load_commands

    def load_commands(self):
        pass
        # load from framework
        # load from app

    def load_from_path(self, path, prefix='Hako.Console.Commands'):
        print(path)
        loaded = {}
        packages = pkgutil.walk_packages(list(path), prefix)
        for finder, modname, ispkg in packages:
            if not ispkg:
                module = importlib.import_module(modname)
                instance = getattr(module, modname.split('.')[-1])
                cmd = instance()
                loaded[cmd.signature] = {
                    'module': instance,
                    'signature': cmd.signature,
                    'description': 'example description'
                }
        return loaded