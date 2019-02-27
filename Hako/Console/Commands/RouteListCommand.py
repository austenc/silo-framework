from Hako.Console.Command import Command

class RouteListCommand(Command):
    def __init__(self):
        self.signature = 'route:list {arg1 : This is an example description!} {--O|option1 : This eventually might do stuff}'

    def handle(self):
        print('this is the route list command handling some stuff')
        print(self.arguments())
        print(self.options())