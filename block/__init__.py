class Block():
    """コードのまとまりを表す。"""

    def __init__(self):
        self.nodes = []

    def append(self, nd):
        self.nodes.append(nd)
