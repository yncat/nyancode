from .base import *


class PrintNode(BaseNode):
    """文字をプリントする。"""
    parameter_constraints = {
        "message": str  # プリントする文字
    }
    display_name = _("文字を表示")

    def generate(self, indent_level=0):
        lst = []
        self._generate(lst, "print(\"%s\")" %
                       (self.parameters["message"]), indent_level)
        return lst
