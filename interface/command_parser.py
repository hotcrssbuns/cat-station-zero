from game.station import Station
from utils.helpers import clear_screen
from game.tasks import TaskManager, Task, Priority
import random

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
            "NEXT TURN": self.next_turn,
        }

    def parse_command(self, user_input: str):
        command = user_input.upper().strip()

        if command in self.commands:
            self.commands[command]()
        else:
            clear_screen()
            print(f"Unknown command: '{command}'. Type HELP for available commands.")

    def status(self):
        station_status = self.station.get_status()
        clear_screen()
        print("\n=== STATION STATUS ===")
        for metric, value in station_status.items():
            print(f"{metric.title()}: {value}%")
        print("===================")
        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

    def resources(self):
        station_resources = self.station.get_resources()
        clear_screen()
        print("\n=== RESOURCES ===")
        for metric, value in station_resources.items():
            if metric == "crew members":
                cat_faces = "^•ﻌ•^ " * value
                print(f"{metric.title()}: {cat_faces}")
            else:
                print(f"{metric.title()}: {value}")
        print("===================")
        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

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
            print("> NEXT TURN")
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
                print(f"       Description: {task.description}")
        print("===================\n")
        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

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
            input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
            return

        selection = input("> ").strip().upper()

        if selection == "EXIT":
            return

        try:
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
                        missing_resources.append(
                            f"{resource.replace('_', ' ').title()}"
                        )
                if can_afford:
                    confirm = input("\nAssign resources? (y/n): ").lower()
                    if confirm == "y":
                        for (
                            resource,
                            amount,
                        ) in selected_task.required_resources.items():
                            current = getattr(self.station, f"_{resource}")
                            setattr(self.station, f"_{resource}", current - amount)
                        selected_task.resources_assigned = (
                            True  # Mark resources as assigned
                        )
                        print("\nResources assigned succesfully!")
                        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
                    else:
                        print("\nResource assignment cancelled.")
                        input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
                else:
                    print("\nInsufficient resources!")
                    print(f"Missing: {', '.join(missing_resources)}")
                    input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
            else:
                print(f"\nPlease enter a number between 1 and {len(tasks)}")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
        except ValueError:
            print("\nPlease enter a valid task number")
            input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

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

                        if not selected_task.resources_assigned:
                            print(
                                "\nCannot complete task - Resources have not been assigned yet!"
                            )
                            print(
                                "Use the ASSIGN command first to allocate necessary resources."
                            )
                            break

                        # If resources were assigned, continue with success chance calculation
                        base_chance = 0.8  # 80% base chance of success
                        if selected_task.priority == Priority.CRITICAL:
                            base_chance = 0.4  # Critical tasks are harder
                        elif selected_task.priority == Priority.URGENT:
                            base_chance = 0.6  # Urgent tasks are moderate

                        success = random.random() < base_chance

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

            input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

        else:
            print("No tasks currently available")
            input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

    def next_turn(self):
        # First, handle random chance for new task generation
        chance = random.random()
        resource_chance = random.randrange(1, 5)
        self.station.turns_until_resources -= 1

        if self.station.turns_until_resources <= 0:
            self.station.turns_until_resources = 5
            if resource_chance == 1:
                self.station.update_system("spare_parts", 5)
                print("Delivery! You got 5 Spare Parts!")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
            elif resource_chance == 2:
                self.station.update_system("power_cells", 5)
                print("Delivery! You got 5 Power Cells!")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
            elif resource_chance == 3:
                self.station.update_system("medical_supplies", 5)
                print("Delivery! You got 5 Medical Supplies!")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")
            elif resource_chance == 4:
                self.station.update_system("crew_members", 5)
                print("Delivery! You got 1 Crew Members!")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

        if chance < 0.5:  # 50% chance each turn
            self.station.add_random_task()

        # Update all station systems with small degradation
        self.station.update_system("oxygen", -5)
        self.station.update_system("power", -5)
        self.station.update_system("hull_integrity", -5)
        self.station.update_system("crew_morale", -5)

        # Get the current list of tasks
        tasks = self.station.task_manager.active_tasks
        tasks_to_remove = []  # Keep track of expired tasks

        # Update each task's remaining turns
        for task in tasks:
            task.turns_remaining -= 1
            if task.turns_remaining <= 0:
                # If task expires, apply failure effects
                for system, change in task.failure_effects.items():
                    self.station.update_system(system, change)
                    print(
                        f"\n{system.title()} {'increased' if change > 0 else 'decreased'} by {abs(change)}"
                    )
                tasks_to_remove.append(task)
                print(f"\nTask failed: {task.name} - Ran out of time!")
                input("\nPRESS ANY KEY TO RETURN TO COMMAND INTERFACE")

        # Remove expired tasks
        for task in tasks_to_remove:
            self.station.task_manager.remove_task(task)

        # Check if game is over
        if self.station.is_game_over():
            clear_screen()
            print("\nGAME OVER")
            print("\nStation systems critical. All crew evacuated.")
            input("\nPress Enter to quit...")
            sys.exit()

        # Show turn summary if any tasks expired
        if tasks_to_remove:
            input("\nPress Enter to continue...")
