from .base import *


class QuestionBranchNode(BaseNode):
    """「はい/いいえ」で分岐。"""
    parameter_constraints = {
        "title": str,  # 質問タイトル
        "message": str,  # 質問内容
    }
    parameter_display_names = {
        "title": "質問タイトル",
        "message": "質問内容"
    }
    child_block_constraints = {
        "yes",  # 「はい」が選択されたときに実行する処理
        "no"  # 「いいえ」が選択されたときに実行する処理
    }
    child_block_display_names = {
        "yes": "「はい」のときの処理内容",
        "no": "「いいえ」のときの処理内容"
    }
    display_name = "「はい/いいえ」で分岐"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst, "if nyancode.question(\"%s\", \"%s\"):" %
            (self.parameters["title"], self.parameters["message"]), indent_level)
        lst.extend(self.child_blocks["yes"].generate(indent_level + 1))
        self._generate(lst, "else:", indent_level)
        lst.extend(self.child_blocks["no"].generate(indent_level + 1))
        return lst
