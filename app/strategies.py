from queue import Queue, LifoQueue

from rich.console import Console

from app.classes import NodeClass


class CountStrategy:
    count: int
    traversed: LifoQueue[NodeClass]

    def __init__(self, **kwargs):
        # Init to -1 as we add the root node first so the distance should be 0 when adding the root
        self.count = -1
        self.traversed = LifoQueue()

    def execute(self, **kwargs):
        node = kwargs.get('node')
        if node:
            self.traversed.put(node)
        self.count += 1

    def print(self, **kwargs):
        Console(style="bold green").print(f"Distance Count: {self.count}")
        print_nodes = []
        while not self.traversed.empty():
            print_nodes.append(self.traversed.get().name)
        # Console(style="bold yellow").print(f"{' :left_right_arrow: '.join([node for node in reversed(print_nodes)])}")

    def reverse(self, **kwargs):
        self.traversed.get()
        self.count -= 1


class TraverseDepthFirstStrategy:
    def __init__(self, helper: CountStrategy, upward: bool = False):
        self.helper = helper
        self.upward = upward

    def run(self, root_node: NodeClass, end_node: NodeClass):
        node = None
        self.helper.execute(node=root_node)
        if self.upward:
            current_node = root_node
            while current_node.parent is not None:
                current_node = current_node.parent
                self.helper.execute(node=current_node)
                node = self.find_node(current_node, end_node)
                if node:
                    break
        else:
            node = self.find_node(root_node, end_node)

        if node:
            self.helper.print()

        return node

    def find_node(self, root_node: NodeClass, end_node: NodeClass) -> NodeClass | None:
        return_node = None

        if root_node == end_node:
            return root_node

        if not return_node:
            for child in root_node.children:
                self.helper.execute(node=child)
                return_node = self.find_node(child, end_node)
                if return_node:
                    break
                self.helper.reverse()

        return return_node


class TraverseBreadthFirstStrategy:
    traverse_queue: Queue[tuple]
    traversed_set: set[NodeClass]

    def __init__(self, helper: CountStrategy, upward: bool = False):
        self.helper = helper
        self.traverse_queue = Queue()
        self.traversed_set = set()
        self.upward = upward

    def run(self, root_node: NodeClass, end_node: NodeClass):
        self.push_to_queue({root_node}, 0)
        self.helper.execute(node=root_node)
        node = self.find_node(end_node)
        if node:
            self.helper.print()
        return node

    def find_node(self, end_node: NodeClass) -> NodeClass | None:
        return_node = None
        prev_depth = 1
        while not self.traverse_queue.empty():
            current_node, current_depth = self.traverse_queue.get()

            if current_depth == prev_depth:
                self.helper.reverse()
                self.helper.execute(node=current_node)

            decrement = prev_depth - current_depth
            while decrement > 0:
                self.helper.reverse()
                decrement -= 1

            decrement = current_depth - prev_depth
            while decrement > 0:
                self.helper.execute(node=current_node)
                decrement -= 1

            # print("GET", current_node.name, current_depth, prev_depth)
            prev_depth = current_depth

            if current_node == end_node:
                return current_node

            self.push_to_queue(current_node.children, current_depth)

        return return_node

    def push_to_queue(self, queue_nodes, current_depth):
        print(self.traverse_queue.queue)
        for node in queue_nodes:
            if node not in self.traversed_set:
                self.traversed_set.add(node)
                self.traverse_queue.put((node, current_depth + 1))

        current_set = {child.spouse for child in queue_nodes if child.spouse}
        for node in current_set:
            if node not in self.traversed_set:
                self.traversed_set.add(node)
                self.traverse_queue.put((node, current_depth + 2))

        sibling_set = set()
        for child in queue_nodes:
            if child.spouse:
                sibling_set = sibling_set.union(child.spouse.siblings)

        for node in sibling_set:
            if node not in self.traversed_set:
                self.traversed_set.add(node)
                self.traverse_queue.put((node, current_depth + 3))
