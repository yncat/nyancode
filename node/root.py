from .base import *


class RootNode(BaseNode):
    """プログラム全体を表すノード。"""
    parameter_constraints = {}
    child_blocks = {
        "block"  # 処理本体
    }

    def generate(self, indent_level=0, for_direct_run=False):
        ret = [
            "# generated by nyancode.",
        ]
        if not for_direct_run:
            self._generate(ret, "import nyancode_runtime_std as nyancode")
        # end append import for output mode
        ret.append("")

        for elem in self.child_blocks["block"]:
            ret.extend(elem.generate(indent_level, for_direct_run))
        # end for
        return ret
