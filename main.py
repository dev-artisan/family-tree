from rich.console import Console

from app.classes import NodeClass
from app.functions import clear, add_person, get_info

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
    muhammad.add_parent(junayd)

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
            print("3: Exit")

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
                        root_node = {node for node in nodes if node.id == 1}.pop()
                        relation_id = input("Selet person ID: ")
                        get_info(root_node, int(relation_id))

                case _:
                    Console(style="bold red").print("Quitting!")
                    exit(1)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)


if __name__ == '__main__':
    main()
