from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

from app.classes import application
from app.functions import clear, add_person, load_data
from app.strategies import CountStrategy, TraverseBreadthFirstStrategy, TraverseDepthFirstStrategy


def main():
    application.nodes = load_data()
    clear()

    try:
        while True:
            rprint(Panel(
        """[bold]Options:
        1: Add person
        2: Get person info
        3: Show tree with different root
        4: Calculate distance between people
        5: Exit"""
            ))

            option = input("Please select an option: ")
            clear()

            match option:
                case "1":
                    node = add_person()
                    if node:
                        application.add_node(node)
                        clear()
                case "2":
                    relation_id = input("Select person ID: ")
                    application.get_info(int(relation_id))

                case "3":
                    relation_id = input("Select person ID: ")
                    clear(root_node=application.get_node(int(relation_id)))
                case "4":
                    if application.nodes:
                        from_id = input("From person (ID): ")
                        to_id = input("To person (ID): ")
                        from_node = application.get_node(int(from_id))
                        to_node = application.get_node(int(to_id))

                        node = TraverseDepthFirstStrategy(
                            helper=CountStrategy()
                        ).run(root_node=from_node, end_node=to_node)

                        if not node:
                            node = TraverseDepthFirstStrategy(
                                helper=CountStrategy()
                            ).run(root_node=to_node, end_node=from_node)

                        if not node:
                            node = TraverseDepthFirstStrategy(
                                helper=CountStrategy(),
                                upward=True
                            ).run(root_node=to_node, end_node=from_node)

                        if not node:
                            node = TraverseBreadthFirstStrategy(
                                helper=CountStrategy()
                            ).run(root_node=from_node, end_node=to_node)

                        if not node:
                            node = TraverseBreadthFirstStrategy(
                                helper=CountStrategy()
                            ).run(root_node=to_node, end_node=from_node)

                        if not node:
                            node = TraverseBreadthFirstStrategy(
                                helper=CountStrategy(),
                                upward=True
                            ).run(root_node=to_node, end_node=from_node)

                        if not node:
                            Console(style="magenta").print("Person not found")
                case _:
                    Console(style="bold red").print("Quitting!")
                    exit(1)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)


if __name__ == '__main__':
    main()
