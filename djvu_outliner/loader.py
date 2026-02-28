import re
from djvu_outliner.structures import TreeNode, NodeData
from pathlib import Path


def parser(inputfile: Path):
    with open(inputfile, "r") as f:
        shift = 0
        root = TreeNode(NodeData("Root 0", shift))
        root.parent = root
        root.data.indent = -1
        rootdict = {-1: root}
        current = root
        previous = root
        while x := f.readline():
            if x.startswith("#SHIFT"):
                match = re.match(r"#SHIFT\s*([0-9]+)", x)
                assert match is not None
                shift = int(match.group(1))
            elif not x.startswith("#") and x != " " and x != "\n":
                current = TreeNode(NodeData(x, shift))
                isChild = False
                isSibling = False
                isAncestor = False
                if current.data.indent > previous.data.indent:
                    isChild = True
                elif current.data.indent == previous.data.indent:
                    isSibling = True
                elif current.data.indent < previous.data.indent:
                    isAncestor = True

                if isChild:
                    current.parent = previous
                    previous.add_child(current)
                    previous = current
                    rootdict.update(
                        {current.data.indent: current, previous.data.indent: previous}
                    )
                elif isSibling:
                    current.parent = previous.parent
                    current.parent.add_child(current)
                    previous = current
                    rootdict.update(
                        {current.data.indent: current, previous.data.indent: previous}
                    )
                elif isAncestor:
                    key = None
                    for i in sorted(rootdict.keys(), reverse=True):
                        if i < current.data.indent:
                            key = i
                            break
                        else:
                            key = None
                    assert key is not None
                    current_par = rootdict[key]
                    current.parent = current_par
                    (current.parent).add_child(current)

                    rootdict2 = rootdict.copy()
                    [
                        rootdict2.pop(i)
                        for i in rootdict.keys()
                        if i > current.data.indent
                    ]
                    rootdict = rootdict2.copy()

                    rootdict.update({current.data.indent: current})
                    previous = current
    return root
