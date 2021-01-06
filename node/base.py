INDENT_WIDTH = 4


class BaseNode:
    """基本となるノード。共通メソッドだけ定義。"""
    # 必要な引数の型を指定
    parameter_constraints = {}
    # 必要な子ブロックの名前を指定
    child_block_constraints = {}
    # ノードの表示名を指定
    display_name = ""

    def __init__(self):
        self.parameters = {}
        self.child_blocks = {}
        self.name = self.__class__.__name__

    def setSingleParameter(self, name, value):
        self.parameters[name] = value

    def setSingleChildBlock(self, name, child_block):
        self.child_blocks[name] = child_block

    def generate(self):
        """コードを生成する。コードは、行ごとに区切ったリストで返すこと。"""
        return ["pass"]

    def _generate(self, out_lst, code, indent_level=0):
        ret = " " * (indent_level * INDENT_WIDTH)
        ret += code
        out_lst.append(code)
