from game.station import Station
from utils.helpers import clear_screen
import sys


class Parser:
    def __init__(self):
        self.station = Station()
        self.commands = {
            "STATUS": self.status,
            "HELP": self.help,
            "QUIT": self.quit,
            "MENU": self.menu,
            "EXIT": self.quit,
        }

    def parse_command(self, user_input: str):
        command = user_input.upper().strip()

        if command in self.commands:
            self.commands[command]()
        else:
            clear_screen()
            print(f"Unknown command: '{command}'. Type HELP for available commands.")

        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

    def status(self):
        station_status = self.station.get_status()
        clear_screen()
        print("\n=== STATION STATUS ===")
        for metric, value in station_status.items():
            print(f"{metric.title()}: {value}%")
        print("===================")

    def quit(self):
        clear_screen()
        sys.exit()

    def menu(self):
        while True:
            clear_screen()
            print("\n=== CAT STATION 0 ===")
            print("1. Start New Game")
            print("2. How to Play")
            print("3. Quit")

            choice = input("\n> ").upper().strip()

            if choice == "1":
                clear_screen()
                self.command_interface()
                break
            elif choice == "2" or choice == "HOW TO PLAY":
                self.help()
            elif choice == "3" or choice == "QUIT":
                sys.exit()

    def help(self):
        clear_screen()
        print("\n=== How to Play ===")
        print("You're the captain of Kitty Station 0")
        print("Manage your space station by maintaining crucial systems:")
        print("- Monitor oxygen, power, hull integrity, and crew morale")
        print("- Complete tasks to keep systems running")
        print("- Manage resources carefully")
        input("\nPress Enter to return to menu...")

    def command_interface(self):
        while True:
            clear_screen()
            print("\n=== COMMAND INTERFACE ===")
            print("> STATUS")
            print("> TASKS")
            print("> RESOURCES")
            print("> ASSIGN")
            print("> COMPLETE")
            print("\n> HELP")
            print("> EXIT")

            choice = input("\n> ").upper().strip()
            self.parse_command(choice)
