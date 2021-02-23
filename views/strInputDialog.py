# -*- coding: utf-8 -*-
# string input dialog

import wx
import globalVars
import views.ViewCreator
from views.baseDialog import *
import constants


class dialog(BaseDialog):
    def __init__(self):
        super().__init__("StringInputDialog")

    def Initialize(self, parameter_display_name, default_value):
        self.log.debug("created")
        super().Initialize(None, _("文字列引数の入力"))
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
            style=wx.TE_MULTILINE,
            x=400
        )
        footerCreator = views.ViewCreator.ViewCreator(
            self.viewMode,
            self.panel,
            self.sizer,
            style=wx.ALIGN_RIGHT | wx.ALL,
            margin=20)
        self.okBtn = footerCreator.okbutton(_("OK"))
        self.okBtn.SetDefault()
        self.closeBtn = footerCreator.cancelbutton(_("キャンセル"))
        self.closeBtn.SetDefault()

    def Destroy(self, events=None):
        self.log.debug("destroy")
        self.wnd.Destroy()

    def getData(self):
        return self.input.GetValue()
