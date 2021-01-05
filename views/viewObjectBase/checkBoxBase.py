# checkBoxBase for ViewCreator
# Copyright (C) 2019-2020 Hiroki Fujii <hfujii@hisystron.com>


import wx
from views.viewObjectBase import viewObjectUtil, controlBase


class checkBox(controlBase.controlBase, wx.CheckBox):
    def __init__(self, *pArg, **kArg):
        self.focusFromKbd = viewObjectUtil.popArg(
            kArg, "enableTabFocus", True)  # キーボードフォーカスの初期値
        return super().__init__(*pArg, **kArg)
