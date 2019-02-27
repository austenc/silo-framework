import getpass
from sty import fg, bg, rs

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
                if param.shortcut:
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

    def ask(self, question):
        return input(self.end_with_prompt(question))
    
    def secret(self, question):
        return getpass.getpass(self.end_with_prompt(question))
    
    def confirm(self, question, default=False):
        yes = ['yes', 'y', 'ye']
        no = ['no', 'n']
        selected = 'yes' if default is True else 'no'
        choice = input('{question} (yes/no) [{selected}]\n> '.format(
            question=question, 
            selected=self.color(selected, 'warn')
        )).lower()
        if choice is '':
            choice = selected
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           self.confirm(question)

    def choice(self, question, choices, default=None):
        selected = default if default in choices else 0
        choice = input(self.list_choices(question, choices, selected))
        if choice is '':
            choice = selected
        
        if choice in choices:
            return choice
        elif int(choice) < len(choices):
            return choices[int(choice)]

        print(self.color('Invalid choice, please try again.', 'error'))
        return self.choice(question, choices, default)

    def list_choices(self, question, choices, selected):
        output = '{question} '.format(question=self.color(question, 'info'))
        output += '[{choice}]:\n'.format(choice=self.color(selected, 'warn'))
        for key, choice in enumerate(choices):
            output += ' [{key}] {choice} \n'.format(key=self.color(key, 'warn'), choice=choice)
        output += '> '
        return output

    def end_with_prompt(self, string):
        if not string.endswith("\n"):
            string += "\n> "
        return string
    
    def color(self, text, color='info'):
        if color is 'info':
            return self.text_color(text, 'green')
        if color is 'warn':
            return self.text_color(text, 'yellow')
        if color is 'question':
            return self.text_color(text, 'black', 'cyan')
        if color is 'error':
            return self.text_color(text, 'white', 'da_red')

    def text_color(self, string, _fg, _bg=None):
        if _bg is None:
            return '{fg}{s}{rs}'.format(fg=fg[_fg], s=string, rs=rs.all)
        return '{fg}{bg}{s}{rs}'.format(fg=fg[_fg], bg=bg[_bg], s=string, rs=rs.all)

    def info(self, text):
        print(self.color(text, 'info'))

    def warn(self, text):
        print(self.color(text, 'warn'))
    
    def question(self, text):
        print(self.color(text, 'question'))

    def error(self, text):
        print(self.color(text, 'error'))
