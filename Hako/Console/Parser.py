import re
from Hako.Console.Param import Param


class Parser:
    @classmethod
    def parse(self, signature):
        name = self.name(signature).strip()
        matches = re.findall('\{(.*?)\}', signature)
        if matches:
            return name, self.parameters(matches)

        return name, []

    @classmethod
    def name(self, signature):
        command = re.search('[^\s]+', signature)
        if command:
            return command.group()

        raise Exception('Could not determine command name.')

    @classmethod
    def parameters(self, tokens):
        arguments = {}

        for token in tokens:
            option = re.findall('-{2,}(.*)', token)
            if option:
                param = self.parse_option(option[0])
                arguments[param.name] = param
            else:
                param = self.parse_argument(token)
                arguments[param.name] = param

        return arguments

    @classmethod
    def parse_argument(self, token):
        token, desc = self.get_description(token)
        if token.endswith('?'):
            return Param(token.rstrip('?'), description=desc, is_optional=True)
        
        matches = re.findall('(.+)\=(.+)', token)
        if matches and len(matches[0]) == 2:
            return Param(matches[0][0], description=desc, default=matches[0][1])
        
        return Param(token, description=desc)

    @classmethod
    def parse_option(self, token):
        token, desc = self.get_description(token)
        shortcut, token = self.get_shortcut(token)

        matches = re.findall('(.+)\=(.+)', token)
        if matches and len(matches[0]) == 2:
            return Param(matches[0][0], shortcut=shortcut, description=desc, default=matches[0][1])

        return Param(token, shortcut=shortcut, description=desc, is_optional=True)

    @classmethod
    def get_shortcut(self, token):
        parts = token.split('|')
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

        return None, token.strip()

    @classmethod
    def get_description(self, token):
        parts = token.split(':')
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

        return token.strip(), None