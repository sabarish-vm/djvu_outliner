import re


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.ancestor = []
        self.parent: TreeNode

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def print_tree(self, prefix="", is_last=True):
        """Pretty print tree with Unicode lines"""
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(self.data.sub) + f"({self.data.page})")

        new_prefix = prefix + ("    " if is_last else "│   ")
        children_count = len(self.children)

        for i, child in enumerate(self.children):
            child.print_tree(new_prefix, i == children_count - 1)


class NodeData:
    def __init__(self, string, shift):
        match = re.match(r"(.*)\s([+-]?[0-9]+)\s*$", string)
        assert match is not None
        self.shift = shift
        self.page = int(match.group(2)) + shift
        self.sub = match.group(1)
        match = re.match(r"(^\s*)", self.sub)
        assert match is not None
        self.indent = len(match.group(1))
        self.sub = self.sub.strip()
