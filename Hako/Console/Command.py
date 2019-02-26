class Command:
    def __init__(self):
        self._params = {}
        self._param_values = {}

    def arguments(self):
        arguments = {}
        for name, param in self._params.items():
            if not param.is_optional:
                arguments[name] = getattr(self._param_values, name, param.default)
        return arguments

    def argument(self, argument):
        return self.arguments().get(argument)
    
    def options(self):
        options = {}
        for name, param in self._params.items():
            if param.is_optional:
                options[name] = getattr(self._param_values, name, param.default)
        return options

    def option(self, option):
        return self.options().get(option)