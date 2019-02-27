from Hako.Console.Command import Command

class RouteListCommand(Command):
    def __init__(self):
        self.signature = '''route:list 
            {arg1 : This is an example argument description!} 
            {--O|option1 : This option might do stuff}
        '''

    def handle(self):
        print('Running route:list command with these args and options:')
        print(self.arguments())
        print(self.options())
        name = self.ask('What is your name?')
        print('Hello '+name)
        password = self.secret('What is the password?')
        print('You entered "'+password+'"')