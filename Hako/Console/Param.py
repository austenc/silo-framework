class Param:
    def __init__(self, name, **kwargs):
        # Set defaults
        self.name = name.strip()
        self.default = None
        self.description = ''
        self.is_optional = False
        self.shortcut = None

        # Override with any args passed in
        for key, value in kwargs.items():
            self.__dict__[key] = value
        
        # If something has a default, it is optional
        if (self.default is not None):
            self.is_optional = True
    
    def to_args(self, parser):
        if self.shortcut is not None:
            parser.add_argument(
                self.arg_name(self.shortcut),
                self.arg_name(self.name),
                default=self.default,
                help=self.description
            )
        else:
            parser.add_argument(
                self.arg_name(self.name), 
                default=self.default,
                help=self.description
            )

    def arg_name(self, name):
        if (self.is_optional and name[:2] is not '--'):
            return '--' + name
        return name