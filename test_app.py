import pytest

from app.classes import NodeClass
from app.functions import load_data
from app.strategies import TraverseDepthFirstStrategy, CountStrategy, TraverseBreadthFirstStrategy


@pytest.fixture
def nodes():
    return load_data()


@pytest.mark.parametrize("root_node_name,end_node_name,expected", [
    ("Muhammad", "Hoda", 2),
    ("Marwan", "Hoda", 1),
    ("Muhammad", "Fatima", 2),
    ("Fatima", "Muhammad", 2),
    ("Ahmad", "Kareem", 1),
    ("Muhammad", "Sharif", 2),
])
def test_basic_parent_children_using_depth_first(nodes, root_node_name, end_node_name, expected):
    root_node = {node for node in nodes if node.name == root_node_name}.pop()
    end_node = {node for node in nodes if node.name == end_node_name}.pop()

    traversal = TraverseDepthFirstStrategy(helper=CountStrategy())
    node = traversal.run(root_node=root_node, end_node=end_node)
    if not node:
        traversal = TraverseDepthFirstStrategy(helper=CountStrategy())
        traversal.run(root_node=end_node, end_node=root_node)

    assert traversal.helper.count == expected


@pytest.mark.parametrize("root_node_name,end_node_name,expected", [
    ("Ahmad", "Hoda", 4),
    ("Fatima", "Hoda", 4),
    ("Marwan", "Ahmad", 3),
])
def test_basic_parent_children_using_depth_first_with_upward(nodes, root_node_name, end_node_name, expected):
    root_node = {node for node in nodes if node.name == root_node_name}.pop()
    end_node = {node for node in nodes if node.name == end_node_name}.pop()

    traversal = TraverseDepthFirstStrategy(helper=CountStrategy(), upward=True)
    node = traversal.run(root_node=root_node, end_node=end_node)
    if not node:
        traversal = TraverseDepthFirstStrategy(helper=CountStrategy(), upward=True)
        traversal.run(root_node=end_node, end_node=root_node)

    assert traversal.helper.count == expected


@pytest.mark.parametrize("root_node_name,end_node_name,expected", [
    ("Muhammad", "Khadijah", 1),
    ("Muhammad", "Hany", 3),
    ("Muhammad", "Abdullah", 4),
    ("Muhammad", "Alia", 3),
    ("Abdullah", "Muhammad", 4),
])
def test_basic_sibling_children_using_breadth_first(nodes, root_node_name, end_node_name, expected):
    root_node = {node for node in nodes if node.name == root_node_name}.pop()
    end_node = {node for node in nodes if node.name == end_node_name}.pop()

    traversal = TraverseBreadthFirstStrategy(helper=CountStrategy())
    node = traversal.run(root_node=root_node, end_node=end_node)
    if not node:
        traversal = TraverseBreadthFirstStrategy(helper=CountStrategy())
        traversal.run(root_node=end_node, end_node=root_node)

    assert traversal.helper.count == expected

def test_add_node_sibling_using_breadth_first(nodes):
    atef = NodeClass(name="Atef", identifier=14)
    nodes.add(atef)
    abdullah = {node for node in nodes if node.name == "Abdullah"}.pop()
    atef.add_parent(abdullah)

    root_node = {node for node in nodes if node.name == "Muhammad"}.pop()

    traversal = TraverseBreadthFirstStrategy(helper=CountStrategy())
    node = traversal.run(root_node=root_node, end_node=atef)
    if not node:
        traversal = TraverseBreadthFirstStrategy(helper=CountStrategy())
        traversal.run(root_node=atef, end_node=root_node)

    assert traversal.helper.count == 5
