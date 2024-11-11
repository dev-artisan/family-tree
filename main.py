from app.classes import application
from app.functions import clear, load_data, menu
from rich.console import Console


def main():
    application.nodes = load_data()
    clear()

    try:
        while True:
            menu()
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)


if __name__ == "__main__":
    main()
