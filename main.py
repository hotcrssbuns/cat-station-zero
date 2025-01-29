from interface.command_parser import Parser
from game.station import Station


def main():
    parser = Parser()
    parser.station.add_random_task()
    parser.menu()


if __name__ == "__main__":
    main()
