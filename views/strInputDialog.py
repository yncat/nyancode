# -*- coding: utf-8 -*-
# string input dialog

import wx
import globalVars
import views.ViewCreator
from logging import getLogger
from views.baseDialog import *
import constants


class dialog(BaseDialog):
    def __init__(self):
        # まだglobalVars.appが未精製の状態での軌道の可能性があるのであえて呼ばない
        # super().__init__()
        self.identifier = "StringInputDialog"
        self.log = getLogger("%s.%s" % (constants.LOG_PREFIX, self.identifier))
        self.value = None
        self.viewMode = "white"

    def Initialize(self, parameter_display_name):
        self.log.debug("created")
        super().Initialize(None, _("文字列引数の入力"), 0)
        self.parameter_display_name = parameter_display_name
        self.InstallControls()
        return True

    def InstallControls(self):
        """いろんなwidgetを設置する。"""
        creator = views.ViewCreator.ViewCreator(
            self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20)
        self.input, static = creator.inputbox(
            self.parameter_display_name,
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
