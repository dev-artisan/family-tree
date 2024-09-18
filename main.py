from rich.console import Console

from app.classes import NodeClass
from app.functions import clear, add_person, get_info
from app.strategies import get_node

nodes = set()

def load_data():
    global nodes
    omar = NodeClass(name='Omar', identifier=1)
    khadijah = NodeClass(name='Khadijah', identifier=2)
    junayd = NodeClass(name='Junayd', identifier=3)
    jwife = NodeClass(name='JWife', identifier=4)
    muhammad = NodeClass(name='Muhammad', identifier=5)
    fatima = NodeClass(name='Fatima', identifier=6)

    khadijah.add_spouse(omar)
    junayd.add_parent(omar)
    junayd.add_spouse(jwife)
    fatima.add_parent(junayd)
    muhammad.add_sibling(fatima)

    nodes = {
        omar, khadijah, junayd, jwife, muhammad, fatima
    }

def main():
    global nodes
    load_data()
    clear(nodes)
    try:
        while True:
            print("Options:")
            print("1: Add person")
            print("2: Get person info")
            print("3: Show tree with different root")
            print("4: Exit")

            option = input("Please select an option: ")
            clear(nodes)
            match option:
                case "1":
                    node = add_person(nodes)
                    if node:
                        nodes = nodes.union({node})
                        clear(nodes)
                case "2":
                    if nodes:
                        relation_id = input("Select person ID: ")
                        get_info(nodes, int(relation_id))

                case "3":
                    if nodes:
                        relation_id = input("Select person ID: ")
                        clear(nodes, root_node=get_node(nodes, int(relation_id)))

                case _:
                    Console(style="bold red").print("Quitting!")
                    exit(1)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)


if __name__ == '__main__':
    main()
