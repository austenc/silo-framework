from Hako.Console.Command import Command

class RouteListCommand(Command):
    def __init__(self):
        self.signature = '''route:list 
            {arg1 : This is an example argument description!} 
            {--O|option1 : This option might do stuff}
        '''

    def handle(self):
        print('Running route:list command with these args and options:')
        print('Args: ', end='')
        print(self.arguments())
        print('Options: ', end='')
        print(self.options())
        print()
        self.table(['example', 'header', '123', 'testerlongstuff'], [
            ['data1', 'data2', 'data3', '123'],
            ['abc', 'def', 'xyz', '123']
        ])
        self.info('info 123')
        self.warn('warning 123')
        self.question('info 123??? test?')
        self.error('This is a big fat error')
        name = self.ask('What is your name?')
        print('Hello '+name)
        password = self.secret('What is the password?')
        print('You entered "'+password+'"')
        if (self.confirm('Do you want to continue?', True)):
            print('You continue on your journey.')
        else:
            print('Your journey is complete.')
        selection = self.choice('Example question?', ['one', 'two', 'three'], 'two')
        print(selection)