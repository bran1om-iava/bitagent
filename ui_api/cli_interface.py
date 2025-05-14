class CLIInterface:
    """
    Command-line interface for interacting with the agent system.
    """

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print("CLI started. Type 'exit' to quit.")
        while self.running:
            cmd = input("agent> ")
            if cmd.strip() == 'exit':
                self.running = False
            else:
                self.handle_command(cmd)

    def handle_command(self, command: str):
        print(f"Handling command: {command}")
