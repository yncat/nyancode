from .base import *


class WaitNode(BaseNode):
    """一定時間待つ。"""
    parameter_constraints = {
        "time": float,  # 待つ時間
    }
    parameter_display_names = {
        "time": "秒数",
    }
    display_name = "一定時間待つ"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst, "nyancode.wait(%s)" % self.parameters["time"], indent_level)
        return lst
