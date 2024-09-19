from queue import Queue, LifoQueue
from typing import Protocol, Optional

from rich.console import Console

from app.classes import NodeClass


class CountStrategy:
    count: int
    traversed: LifoQueue[NodeClass]

    def __init__(self, **kwargs):
        self.count = 0
        self.traversed = LifoQueue()

    def execute(self, **kwargs):
        node = kwargs.get('node')
        if node:
            self.traversed.put(node)
        self.count += 1

    def print(self, **kwargs):
        Console(style="bold green").print(f"Count: {self.count - 1}")
        nodes = []
        while not self.traversed.empty():
            nodes.append(self.traversed.get().name)

        Console(style="bold yellow").print(f"{' <--> '.join([node for node in reversed(nodes)])}")

    def reverse(self, **kwargs):
        self.traversed.get()
        self.count -= 1


class TraverseStragegy(Protocol):
    helper: Optional[CountStrategy]

    def __init__(self, helper: CountStrategy, **kwargs): ...

    def run(self, **kwargs): ...


class TraverseDepthFirstStrategy:
    def __init__(self, helper: CountStrategy):
        self.helper = helper

    def run(self, root_node: NodeClass, end_node: NodeClass):
        self.helper.execute(node=root_node)
        node = self.find_node(root_node, end_node.id)
        self.helper.print()
        return node

    def find_node(self, root_node: NodeClass, relation_id: int) -> NodeClass | None:
        return_node = None

        if root_node.id == relation_id:
            return root_node

        current_set = root_node.children
        current_set = current_set.union({child.spouse for child in root_node.children if child.spouse})
        sibling_set = set()
        for child in root_node.children:
            if child.spouse:
                sibling_set = sibling_set.union(child.spouse.siblings)
        current_set = current_set.union(sibling_set)

        if not return_node:
            for child in current_set: #root_node.children:
                self.helper.execute(node=child)
                return_node = self.find_node(child, relation_id)
                if return_node:
                    break
                self.helper.reverse()

        # if not return_node:
        #     if root_node.spouse:
        #         return_node = self.find_node(root_node.spouse, relation_id)

        # if not return_node:
        #     for sibling in root_node.siblings:
        #         return_node = self.find_node(sibling, relation_id)
        #         if return_node:
        #             break
        return return_node


class TraverseBreadthFirstStrategy:
    traverse_queue: Queue[tuple]
    traversed_set: set[NodeClass]

    def __init__(self, helper: CountStrategy):
        self.helper = helper
        self.traverse_queue = Queue()
        self.traversed_set = set()

    def run(self, root_node: NodeClass, end_node: NodeClass):
        self.traverse_queue.put((root_node, 1))
        self.traversed_set.add(root_node)
        self.helper.execute(node=root_node)
        node = self.find_node(end_node.id)
        self.helper.print()
        return node

    def find_node(self, relation_id: int) -> NodeClass | None:
        return_node = None
        prev_depth = 1
        while not self.traverse_queue.empty():
            current_node, current_depth = self.traverse_queue.get()

            if current_depth < prev_depth:
                self.helper.reverse()

            if current_depth > prev_depth:
                self.helper.execute(node=current_node)

            prev_depth = current_depth
            # print("GET", current_node.name, current_depth, prev_depth, depth)

            if current_node.id == relation_id:
                return current_node


            for node in current_node.children:
                if node not in self.traversed_set:
                    self.traversed_set.add(node)
                    self.traverse_queue.put((node, current_depth + 1))

            current_set = {child.spouse for child in current_node.children if child.spouse}
            for node in current_set:
                if node not in self.traversed_set:
                    self.traversed_set.add(node)
                    self.traverse_queue.put((node, current_depth + 2))

            sibling_set = set()
            for child in current_node.children:
                if child.spouse:
                    sibling_set = sibling_set.union(child.spouse.siblings)

            for node in sibling_set:
                if node not in self.traversed_set:
                    self.traversed_set.add(node)
                    self.traverse_queue.put((node, current_depth + 3))

        return return_node
