class Param:
    def __init__(self, name, **kwargs):
        # Set defaults
        self.name = name.strip()
        self.default = None
        self.description = None
        self.is_optional = False
        self.shortcut = None

        # Override with any args passed in
        for key, value in kwargs.items():
            self.__dict__[key] = value
        
        # If something has a default, it is optional
        if (self.default is not None):
            self.is_optional = True