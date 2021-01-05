TAB_WIDTH = 4


class BaseNode:
    """基本となるコード生成ノード。共通メソッドだけ定義。"""

    def _generate(self, code, indent_level):
        ret = " "*(indent_level*TAB_WIDTH)
        return ret+code

    def generate(self, node, indent_level):
        return "# base node"
