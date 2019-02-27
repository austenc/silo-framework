class Command:
    """Handles arguments and options of CLI commands.

    Extend this class with your own to easily retrieve options 
    and arguments related to the given console command.

    Attributes:
        _params: Internally used, use arguments() or options() instead
        _param_values: Use argument() or option() to get values instead
    """

    def __init__(self):
        self._params = {}
        self._values = {}

    def arguments(self):
        """Fetch user supplied values for this command's arguments.

        Retrieves values (or defaults) for arguments defined in this
        command's signature attribute.

        Returns:
            A dict mapping argument names to their corresponding values.
            For example:
            {'argument': 'Some user supplied value'}
        """
        arguments = {}
        for name, param in self._params.items():
            if not param.is_optional:
                arguments[name] = getattr(self._values, name, param.default)
        return arguments

    def argument(self, key):
        """Fetch a single argument from user supplied values.
        
        Args:
            key: The argument name to retrieve the value of

        Returns:
            The value for a key, falling back to its default or None
        """
        return self.arguments().get(key)
    
    def options(self):
        """Fetch user supplied values for this command's options.

        Retrieves values (or defaults) for options defined in this
        command's signature attribute.

        Returns:
            A dict mapping option names to their corresponding values.
            For example:
            {'option': 'Some user supplied value'}
        """
        options = {}
        for name, param in self._params.items():
            if param.is_optional:
                default = getattr(self._values, name, param.default)
                shortcut_value = getattr(self._values, param.shortcut)
                if shortcut_value:
                    options[name] = shortcut_value
                    options[param.shortcut] = shortcut_value
                else:
                    options[name] = default

        return options

    def option(self, key):
        """Fetch a single option from user supplied values.

        Args:
            key: The option name to retrieve the value of

        Returns:
            The value for a key, falling back to its default or None
        """
        return self.options().get(key)
