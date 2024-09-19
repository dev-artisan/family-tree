from rich.console import Console

from app.classes import NodeClass
from app.functions import clear, add_person, get_info, get_node
from app.strategies import TraverseDepthFirstStrategy, CountStrategy, TraverseBreadthFirstStrategy

nodes = set()

def load_data():
    global nodes
    muhammad = NodeClass(name='Muhammad', identifier=1)
    khadijah = NodeClass(name='Khadijah', identifier=2)
    kareem = NodeClass(name='Kareem', identifier=3)
    jasmine = NodeClass(name='Jasmine', identifier=4)
    ahmad = NodeClass(name='Ahmad', identifier=5)
    fatima = NodeClass(name='Fatima', identifier=6)
    hoda = NodeClass(name='Hoda', identifier=7)
    ridwan = NodeClass(name='Ridwan', identifier=8)
    hany = NodeClass(name='Hany', identifier=9)
    alia = NodeClass(name='Alia', identifier=10)
    sharif = NodeClass(name='Sharif', identifier=11)
    abdullah = NodeClass(name='Abdullah', identifier=12)
    marwan = NodeClass(name='Marwan', identifier=13)

    khadijah.add_spouse(muhammad)
    kareem.add_parent(muhammad)
    kareem.add_spouse(jasmine)
    fatima.add_parent(kareem)
    ahmad.add_sibling(fatima)
    ridwan.add_parent(marwan)
    fatima.add_spouse(hany)
    alia.add_spouse(ridwan)
    ridwan.add_sibling(hoda)
    ridwan.add_sibling(sharif)
    alia.add_sibling(abdullah)
    marwan.add_parent(muhammad)


    nodes = {
        muhammad,
        khadijah,
        kareem,
        jasmine,
        ahmad,
        fatima,
        hoda,
        ridwan,
        hany,
        alia,
        abdullah,
        marwan,
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
            print("4: Calculate distance between people")
            print("5: Exit")

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
                case "4":
                    if nodes:
                        from_id = input("From person (ID): ")
                        to_id = input("To person (ID): ")
                        from_node = get_node(nodes, int(from_id))
                        to_node = get_node(nodes, int(to_id))

                        node = TraverseBreadthFirstStrategy(
                            helper=CountStrategy()
                        ).run(root_node=from_node, end_node=to_node)

                        # if not node:
                        #     node = TraverseBreadthFirstStrategy(
                        #         helper=CountStrategy()
                        #     ).run(root_node=to_node, end_node=from_node)
                        # if not node:
                        #     node = TraverseBreadthFirstStrategy(
                        #         helper=CountStrategy()
                        #     ).run(root_node=from_node, end_node=to_node)

                        if not node:
                            print("Person not found")
                case _:
                    Console(style="bold red").print("Quitting!")
                    exit(1)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)


if __name__ == '__main__':
    main()