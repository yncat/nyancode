INDENT_WIDTH = 4


class BaseNode:
    """基本となるノード。共通メソッドだけ定義。"""
    # 必要な引数の型を指定
    parameter_constraints = {}
    # 引数の表示名を指定。ビューで引数を入力するときに、ウィンドウタイトルに表示される。
    parameter_display_names = {}
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

    def generate(self, indent_level=0, for_direct_run=False):
        """コードを生成する。コードは、行ごとに区切ったリストで返すこと。直接実行のためのコードと、出力用のコードを書き分けたい場合は、 for_direct_run を参照して分岐すれば良い。"""
        return ["pass"]

    def _generate(self, out_lst, code, indent_level=0):
        ret = " " * (indent_level * INDENT_WIDTH)
        ret += code
        out_lst.append(code)

    def parameterOrBlankString(self, parameter_name):
        return str(self.parameters[parameter_name]) if parameter_name in self.parameters else ""
