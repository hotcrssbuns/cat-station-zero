from game.station import Station
from utils.helpers import clear_screen

import sys


class Parser:
    def __init__(self):
        self.station = Station()
        self.commands = {
            "STATUS": self.status,
            "QUIT": self.quit,
            "MENU": self.menu,
            "EXIT": self.quit,
            "TASKS": self.tasks,
            "RESOURCES": self.resources,
            "ASSIGN": self.assign,
            "COMPLETE": self.complete,
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

    def resources(self):
        station_resources = self.station.get_resources()
        clear_screen()
        print("\n=== RESOURCES ===")
        for metric, value in station_resources.items():
            print(f"{metric.title()}: {value}")
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
            print("\n> EXIT")

            choice = input("\n> ").upper().strip()
            self.parse_command(choice)

    def tasks(self):
        clear_screen()
        print("\n=== ACTIVE TASKS ===")
        tasks = self.station.get_tasks()
        if not tasks:
            print("No active tasks.")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        print("===================\n")

    def assign(self):
        clear_screen()
        tasks = self.station.task_manager.active_tasks
        if tasks:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")
                for resource_name, amount in task.required_resources.items():
                    print(
                        f"    Required Resources: {resource_name.replace('_', ' ').title()}: {amount}"
                    )
        else:
            print("No tasks currently available")

        selection = input("> ").strip().upper()

        if selection == "EXIT":
            return

        task_num = int(selection) - 1

        if 0 <= task_num < len(tasks):
            selected_task = tasks[task_num]
            clear_screen()
            print(f"\n Selected Task: {selected_task}")
            print("\n Required Resources: ")
            for resource, amount in selected_task.required_resources.items():
                resource_name = resource.replace("_", " ").title()
                current_amount = getattr(self.station, f"_{resource}")
                print(f"{resource_name}: {amount} (You have: {current_amount})")

            can_afford = True
            missing_resources = []
            for resource, amount in selected_task.required_resources.items():
                current_amount = getattr(self.station, f"_{resource}")
                if current_amount < amount:
                    can_afford = False
                    missing_resources.append(f"{resource.replace('_', ' ').title()}")
            if can_afford:
                confirm = input("\nAssign resources? (y/n): ").lower()
                if confirm == "y":
                    for resource, amount in selected_task.required_resources.items():
                        current = getattr(self.station, f"_{resource}")
                        setattr(self.station, f"_{resource}", current - amount)
                    print("\nResources assigned succesfully!")
                else:
                    print("\nResource assignment cancelled.")
            else:
                print("\nInsufficient resources!")
                print(f"Missing: {', '.join(missing_resources)}")

    def complete(self):
        clear_screen()
        tasks = self.station.task_manager.active_tasks

        if tasks:
            # Display all active tasks with their details
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task}")
                for resource_name, amount in task.required_resources.items():
                    print(
                        f"    Required Resources: {resource_name.replace('_', ' ').title()}: {amount}"
                    )

            while True:
                try:
                    selection = input(
                        "\nSelect task to complete (or 'back' to return): "
                    )

                    if selection.lower() == "back":
                        return

                    # Convert selection to task index
                    task_num = int(selection) - 1

                    if 0 <= task_num < len(tasks):
                        selected_task = tasks[task_num]

                        # Show selected task details
                        clear_screen()
                        print(f"\nSelected Task: {selected_task}")

                        # Here we would check if task can be completed
                        # For now, we'll just simulate success
                        # You can add more complex success conditions later
                        success = True

                        if success:
                            # Apply success effects to station
                            for system, change in selected_task.success_effects.items():
                                self.station.update_system(system, change)
                                print(
                                    f"\n{system.title()} {'increased' if change > 0 else 'decreased'} by {abs(change)}"
                                )

                            # Remove task from active tasks
                            self.station.task_manager.remove_task(selected_task)
                            print("\nTask completed successfully!")
                        else:
                            # Apply failure effects
                            for system, change in selected_task.failure_effects.items():
                                self.station.update_system(system, change)
                                print(
                                    f"\n{system.title()} {'increased' if change > 0 else 'decreased'} by {abs(change)}"
                                )

                            # Remove failed task
                            self.station.task_manager.remove_task(selected_task)
                            print("\nTask failed!")

                        break
                    else:
                        print("\nInvalid task number. Please try again.")

                except ValueError:
                    print("\nPlease enter a valid number.")

            input("\nPress Enter to continue...")

        else:
            print("No tasks currently available")
            input("\nPress Enter to continue...")
