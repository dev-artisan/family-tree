from typing import Optional, Self

from rich import print as rprint


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
            string += (
                f" ([magenta]spouse=[red]{self.spouse.id}: {self.spouse.name}[blue])"
            )
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


class App:
    """
    This class represents the Singleton objects the Application uses for state management
    """

    nodes: set

    def __init__(self):
        self.nodes = set()

    def add_node(self, node):
        if not self.nodes:
            return

        self.nodes.add(node)

    def get_node(self, relation_id: int) -> Optional[NodeClass]:
        if not self.nodes:
            return None
        return {node for node in self.nodes if node.id == relation_id}.pop()

    def get_info(self, identifier: int):
        person = self.get_node(int(identifier))
        if not person:
            return
        rprint(f"Name: {person}")
        if person.parent:
            rprint(f"Parent: {person.parent}")
        if person.children:
            rprint("Children")
            for child in person.children:
                rprint(f"  -: {child}")
        if person.siblings:
            rprint("Siblings")
            for sibling in person.siblings:
                rprint(f"  -: {sibling}")


application = App()
