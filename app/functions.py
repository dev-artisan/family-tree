import os

from rich.console import Console
from rich.tree import Tree
from rich import print as rprint

from app.classes import NodeClass
from app.exceptions import ValidationException
from app.strategies import find_node, add_node_to_tree


def clear(nodes):
    os.system('cls' if os.name == 'nt' else 'clear')
    if nodes:
        root_node = {node for node in nodes if node.id == 1}.pop()
        display_tree_from_node(root_node)

def display_tree_from_node(root_node: NodeClass):
    tree = Tree("[bold green]Family Tree", guide_style="bold bright_blue")
    add_node_to_tree(root_node, tree)
    rprint(tree)


def get_identifiers(nodes: set) -> set:
    identifiers = {node.id for node in nodes}
    return identifiers

def add_root(nodes: set) -> NodeClass:
    if len({node for node in nodes if node.id == 1}):
        raise ValidationException("There is already a root node")

    name = input("Name: ")
    node = NodeClass(name=name, identifier=1)
    Console(style="bold green").print(f"Added {node}!")

    return node


def add_node(nodes: set) -> NodeClass:
    if not nodes:
        raise ValidationException("There is no root node")

    name = input("Name: ")
    print("1: Is child of")
    print("2: Is spouse of")
    relationship = input("Relationship: ")

    root_node = {node for node in nodes if node.id == 1}.pop()

    display_tree_from_node(root_node)

    relation_id = input("Select person ID: ")
    relation_node, _ = find_node(root_node, int(relation_id), set())
    if not relation_node:
        raise ValidationException("Relationship does not exist")

    node = NodeClass(name=name, identifier=max(get_identifiers(nodes)) + 1)
    match relationship:
        case "1":
            node.add_parent(parent=relation_node)
        case "2":
            node.add_spouse(spouse=relation_node)

    Console(style="bold green").print(f"Added {node}!")
    return node


def add_person(nodes: set):
    print("1: Add root")
    print("2: Add node")
    print("3: Go back")
    option = input("Select option: ")
    clear(nodes)
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


def get_info(root_node: NodeClass,identifier: int):
    person, _ = find_node(root_node, int(identifier), set())
    rprint(f"[bold]Name: {person}")
    if person.parent:
        rprint(f"[bold]Parent: {person.parent}")
    if person.children:
        rprint("[bold]Children")
        for child in person.children:
            rprint(f"  -: {child}")
    if person.siblings:
        rprint("[bold]Siblings")
        for sibling in person.siblings:
            rprint(f"  -: {sibling}")
