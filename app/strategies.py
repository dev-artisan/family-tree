from rich.tree import Tree
from typing import Callable

from app.classes import NodeClass


def traverse_nodes(root_node: NodeClass, fn: Callable):
    fn(f"{root_node}")
    for child_node in root_node.children:
        traverse_nodes(child_node, fn)


def add_node_to_tree(root_node: NodeClass, tree: Tree):
    new_node = tree.add(f"{root_node}", guide_style="bold bright_blue")
    for child_node in root_node.children:
        add_node_to_tree(child_node, new_node)


def find_node(root_node: NodeClass, relation_id: int, traversed: set) -> tuple[NodeClass | None, set]:
    return_node = None
    if root_node in traversed:
        return return_node, traversed

    if root_node.id == relation_id:
        return root_node, traversed

    traversed = traversed.union({root_node})

    if root_node.spouse:
        return_node, traversed = find_node(root_node.spouse, relation_id, traversed)

    if not return_node:
        for child in root_node.children:
            return_node, traversed = find_node(child, relation_id, traversed)
            if return_node:
                break
    if not return_node:
        for sibling in root_node.siblings:
            return_node, traversed = find_node(sibling, relation_id, traversed)
            if return_node:
                break

    return return_node, traversed


