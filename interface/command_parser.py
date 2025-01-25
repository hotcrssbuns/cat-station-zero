from game.station import Station


class Parser:
    def __init__(self):
        self.station = Station()
        self.commands = {"STATUS": self.status, "HELP": self.help}

    def parse_command(self, user_input: str):
        command = user_input.upper().strip()

        if command in self.commands:
            self.commands[command]()
        else:
            print(f"Unknown command: '{command}'. Type HELP for available commands.")

    def status(self):
        station_status = self.station.get_status()
        print("\n=== Station Status ===")
        print("===================\n")

    def help(self):
        print("\n=== Available Commands===")
        print("STATUS - Display station metrics")
        print("HELP  - Show this help message")
        print("=====================\n")
