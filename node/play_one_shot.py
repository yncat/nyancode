from .base import *


class PlayOneShotNode(BaseNode):
    """効果音を再生する。"""
    parameter_constraints = {
        "path": ParameterTypes.PATH_AUDIOFILE  # 再生する効果音ファイル
    }
    parameter_display_names = {
        "path": "再生する効果音ファイル"
    }
    display_name = "効果音を再生"

    def generate(self, indent_level=0, for_direct_run=False):
        lst = []
        self._generate(
            lst, "nyancode.playOneShot(\"%s\")" %
            (self.parameters["path"]), indent_level)
        return lst
