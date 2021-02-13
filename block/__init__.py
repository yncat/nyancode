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
