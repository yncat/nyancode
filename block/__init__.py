class Block():
    """コードのまとまりを表す。"""

    def __init__(self):
        self.nodes = []

    def insert(self, nd, index=-1):
        if index == -1 or index >= len(self.nodes):
            self.nodes.append(nd)
        else:
            self.nodes.insert(index, nd)

    def __iter__(self):
        return self.nodes.__iter__()
