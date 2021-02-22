from .base import *


class FiftyFiftyBranchNode(BaseNode):
    """ランダムで2つに分岐"""
    child_block_constraints = {
        "pattern1",  # パターン1
        "pattern2"  # パターン2
    }
    child_block_display_names = {
        "pattern1": "パターン1",
        "pattern2": "パターン2"
    }
    display_name = "ランダムで2つに分岐"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst, "if nyancode.randomPattern(2) == 1:", indent_level)
        lst.extend(self.child_blocks["pattern1"].generate(indent_level + 1))
        self._generate(lst, "else:", indent_level)
        lst.extend(self.child_blocks["pattern2"].generate(indent_level + 1))
        return lst
