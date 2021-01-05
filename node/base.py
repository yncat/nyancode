class BaseNode:
    """基本となるノード。共通メソッドだけ定義。"""
    # 必要な引数の型を指定
    parameter_constraints = {}

    def __init__(self):
        self.parameters = {}
        self.child_nodes = {}
        self.name = self.__class__.__name__

    def setSingleParameter(self, name, value):
        self.parameters[name] = value

    def setSingleChildNode(self, name, child_node):
        self.child_nodes[name] = child_node

    def countChildNodes(self):
        """子ノードの数を返す。"""
        return len(self.child_nodes)
