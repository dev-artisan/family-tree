import os

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint

from app.classes import NodeClass, application
from app.exceptions import ValidationException


def clear(root_node=None):
    nodes = application.nodes
    os.system('cls' if os.name == 'nt' else 'clear')
    if nodes:
        display_tree_from_node(nodes, root_node=root_node)


def add_node_to_tree(root_node: NodeClass, tree: Tree, nodes_added: set) -> set:
    nodes_added = nodes_added.union({root_node})
    new_node = tree.add(f"{root_node}")
    for child_node in root_node.children:
        nodes_added = nodes_added.union(add_node_to_tree(child_node, new_node, nodes_added))
    return nodes_added


def display_tree_from_node(nodes: set, root_node: NodeClass = None):
    if root_node is None:
        root_node = {node for node in nodes if node.id == 1}.pop()

    tree = Tree("[green]Family Tree", guide_style="bright_blue")
    nodes_added = add_node_to_tree(root_node, tree, set())
    rprint(tree)
    remaining_nodes = nodes.difference(nodes_added)
    Console(style="blue").print("Other People not displayed:")
    for node in remaining_nodes:
        Console(style="blue").print(f"\t{node}")


def get_identifiers(nodes: set) -> set:
    identifiers = {node.id for node in nodes}
    return identifiers


def add_root(nodes: set) -> NodeClass:
    if len({node for node in nodes if node.id == 1}):
        raise ValidationException("There is already a root node")

    name = input("Name: ")
    node = NodeClass(name=name, identifier=1)
    Console(style="green").print(f"Added {node}!")

    return node


def add_node(nodes: set) -> NodeClass:
    if not nodes:
        raise ValidationException("There is no root node")

    name = input("Name: ")
    print("1: Is child of")
    print("2: Is spouse of")
    print("3: Is sibling of")
    relationship = input("Relation to (use ID): ")

    display_tree_from_node(nodes)

    relation_id = input("Select person ID: ")
    relation_node = application.get_node(int(relation_id))
    if not relation_node:
        raise ValidationException("Relationship does not exist")

    node = NodeClass(name=name, identifier=max(get_identifiers(nodes)) + 1)
    match relationship:
        case "1":
            node.add_parent(parent=relation_node)
        case "2":
            node.add_spouse(spouse=relation_node)
        case "3":
            node.add_sibling(sibling=relation_node)

    Console(style="green").print(f"Added {node}!")
    return node


def add_person():
    rprint(Panel(
        """1: Add root
2: Add node
3: Go back"""
    ))
    nodes = application.nodes
    option = input("Select option: ")
    clear()
    try:
        match option:
            case "1":
                return add_root(nodes)
            case "2":
                if nodes:
                    return add_node(nodes)
                return None
            case _:
                return None

    except ValidationException as e:
        Console(style="bold red").print(f"{e}")
        return None


def load_data():
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

    return {
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
        sharif
    }