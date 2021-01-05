class Block():
    """コードのまとまりを表す。"""

    def __init__(self):
        self.nodes = []

    def append(self, nd):
        self.nodes.append(nd)

    def __iter__(self):
        return self.nodes.__iter__()
