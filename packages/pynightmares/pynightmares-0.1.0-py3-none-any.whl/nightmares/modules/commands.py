class CommandRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance.commands = {}
        return cls._instance

    def register(self, name, aliases=None, help_text=None):
        aliases = aliases or []
        def decorator(func):
            self.commands[name] = {
                "func": func,
                "help": help_text or func.__doc__
            }
            for alias in aliases:
                self.commands[alias] = self.commands[name]
            return func
        return decorator

    def execute(self, command_name):
        command = self.commands.get(command_name)
        if command:
            command["func"]()
        else:
            raise ValueError(f"Команда '{command_name}' не найдена.")
