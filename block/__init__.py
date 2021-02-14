INDENT_WIDTH = 4


class Block():
    """コードのまとまりを表す。"""

    def __init__(self):
        self.nodes = []

    def insert(self, nd, index=-1):
        if index == -1 or index >= len(self.nodes):
            self.nodes.append(nd)
        else:
            self.nodes.insert(index, nd)

    def deleteMultipleNodes(self, indexList):
        nodes_to_delete = [self.nodes[i] for i in indexList]
        for elem in nodes_to_delete:
            self.nodes.remove(elem)

    def __iter__(self):
        return self.nodes.__iter__()

    def getNodeAt(self, index):
        return self.nodes[index]

    def isEmpty(self):
        return len(self.nodes) == 0

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        if self.isEmpty():
            self._generate(
                lst, "pass", indent_level)
            return lst
        # end blank
        for elem in self.nodes:
            lst.extend(elem.generate(indent_level, for_direct_run))
        # end for
        return lst

    def _generate(self, out_lst, code, indent_level=0):
        # TODO: delete duplicate (block/base)
        ret = " " * (indent_level * INDENT_WIDTH)
        ret += code
        out_lst.append(ret)
