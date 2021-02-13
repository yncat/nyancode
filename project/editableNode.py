class EditableNode:
    """このクラスを経由してノードを編集する"""

    def __init__(self, node):
        self.node = node

    def getParameterDisplayNames(self):
        return list(self.node.parameter_display_names.values())
