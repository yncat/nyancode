# -*- coding: utf-8 -*-
# float input dialog

import wx
import globalVars
import views.ViewCreator
import simpleDialog
from views.baseDialog import *
import constants


class dialog(BaseDialog):
    def __init__(self):
        super().__init__("StringInputDialog")

    def Initialize(self, parameter_display_name, default_value):
        self.log.debug("created")
        super().Initialize(None, _("数値引数の入力"))
        self.parameter_display_name = parameter_display_name
        self.default_value = default_value
        self.InstallControls()
        return True

    def InstallControls(self):
        """いろんなwidgetを設置する。"""
        creator = views.ViewCreator.ViewCreator(
            self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20)
        self.input, static = creator.inputbox(
            self.parameter_display_name,
            defaultValue=self.default_value,
            x=100
        )
        footerCreator = views.ViewCreator.ViewCreator(
            self.viewMode,
            self.panel,
            self.sizer,
            style=wx.ALIGN_RIGHT | wx.ALL,
            margin=20)
        self.okBtn = footerCreator.okbutton(_("OK"), event=self.checkInput)
        self.okBtn.SetDefault()
        self.closeBtn = footerCreator.cancelbutton(_("キャンセル"))

    def Destroy(self, events=None):
        self.log.debug("destroy")
        self.wnd.Destroy()

    def getData(self):
        return float(self.input.GetValue())

    def checkInput(self, event):
        try:
            v = float(self.input.GetValue())
        except BaseException:
            simpleDialog.dialog(
                _("エラー"),
                _("%(value)s は、数値として扱えない形式です。入力し直してください。") % {
                    "value": self.input.GetValue()})
            return
        # end error
        event.Skip()
