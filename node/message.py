from .base import *


class MessageNode(BaseNode):
    """文字をプリントする。"""
    parameter_constraints = {
        "title": ParameterTypes.STR_SINGLELINE,  # メッセージタイトル
        "message": ParameterTypes.STR_MULTILINE  # プリントする文字
    }
    parameter_display_names = {
        "title": "メッセージタイトル",
        "message": "表示するメッセージの内容"
    }
    display_name = "メッセージを表示"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst, "nyancode.message(\"%s\", \"%s\")" %
            (self.parameters["title"], self.parameters["message"]), indent_level)
        return lst
