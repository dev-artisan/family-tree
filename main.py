import os
from rich.console import Console
from app.classes import NodeClass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_tree():
    Console(style="bold magenta").print("Work In Progress!")

def add_person():
    print("1: Add root")
    print("2: Add node")
    print("3: Go back")
    option = input("Select option: ")
    clear()

    if not option in ["1", "2"]:
        return

    Console(style="bold green").print("Added!")


def main():
    clear()

    try:
        while True:
            print("Options:")
            print("1: Display Tree")
            print("2: Add person")
            print("3: Exit")

            option = input("Please select an option: ")
            clear()
            match option:
                case "1":
                    display_tree()
                case "2":
                    add_person()
                case _:
                    Console(style="bold red").print("Quitting!")
                    exit(1)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)

if __name__ == '__main__':
    main()
