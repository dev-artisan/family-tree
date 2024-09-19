from typing import Self, Optional


class App(object):
    nodes: set
    def __init__(self):
        self.nodes = set()

    def add_node(self, node):
        self.nodes.add(node)

application = App()

class NodeClass:
    name: str
    id: int
    parent: Optional[Self]
    spouse: Optional[Self]
    children: set[Self]
    siblings: set[Self]

    def __init__(self, name: str, identifier: int):
        self.name = name
        self.id = identifier
        self.parent = None
        self.spouse = None
        self.children = set()
        self.siblings = set()

    def __str__(self):
        string = f"[blue]{self.id}: {self.name}"
        if self.spouse:
            string += f" ([magenta]spouse=[red]{self.spouse.id}: {self.spouse.name}[blue])"
        return string

    def __repr__(self):
        return f"{self.name}"

    def add_sibling(self, sibling: Self) -> Self:
        self.siblings = self.siblings.union({self, sibling})
        self.siblings = self.siblings.union(sibling.siblings)

        for other_sibling in self.siblings:
            other_sibling.siblings = other_sibling.siblings.union(self.siblings)

        sibling.parent = self.parent or sibling.parent
        if sibling.parent:
            self.parent = sibling.parent
            self.parent.children = self.parent.children.union(self.siblings)

        return sibling

    def add_spouse(self, spouse: Self) -> Self:
        if self.spouse:
            self.spouse.spouse = None

        self.spouse = spouse
        spouse.spouse = self
        return spouse

    def add_parent(self, parent: Self) -> Self:
        self.parent = parent
        parent.children = parent.children.union({self})

        for child in parent.children:
            child.siblings = child.siblings.union({self})

        return parent
