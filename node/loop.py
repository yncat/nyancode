from .base import *


class LoopNode(BaseNode):
    """指定回数繰り返し"""
    parameter_constraints = {
        "count": int  # 繰返し回数
    }
    parameter_display_names = {
        "count": "繰返し回数"
    }
    child_block_constraints = {
        "block"  # 繰り返す処理
    }
    child_block_display_names = {
        "block": "繰り返す処理"
    }
    display_name = "指定回数繰り返し"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst,
            "for i in range(%d):" %
            (self.parameters["count"]),
            indent_level)
        lst.extend(self.child_blocks["block"].generate(indent_level + 1))
        return lst
