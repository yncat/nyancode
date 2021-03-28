# -*- coding: utf-8 -*-
# audio file path input dialog

import glob
import os
import wx
import constants
import globalVars
import simpleDialog
import views.ViewCreator
from views.baseDialog import *


class dialog(BaseDialog):
    extensions = [
        "wav",
        "mp3",
        "ogg"
    ]

    def __init__(self):
        super().__init__("StringInputDialog")

    def Initialize(self, parameter_display_name, default_value):
        self.log.debug("created")
        super().Initialize(None, _("サウンドファイルパスの入力"))
        self.parameter_display_name = parameter_display_name
        self.default_value = default_value
        self.prepareFileList()
        self.InstallControls()
        return True

    def InstallControls(self):
        """いろんなwidgetを設置する。"""
        creator = views.ViewCreator.ViewCreator(
            self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20)
        self.filesList, static = creator.listbox(
            _("サウンドファイル一覧"), choices=self.files, size=(300, 300))
        footerCreator = views.ViewCreator.ViewCreator(
            self.viewMode,
            self.panel,
            self.sizer,
            style=wx.ALIGN_RIGHT | wx.ALL,
            margin=20)
        self.okBtn = footerCreator.okbutton(_("OK"), event=self.checkInput)
        self.okBtn.SetDefault()
        self.closeBtn = footerCreator.cancelbutton(_("キャンセル"))

    def prepareFileList(self):
        lst = []
        for e in self.extensions:
            lst.extend([os.path.basename(f)
                        for f in glob.glob("data\\sound\\*." + e)])
        # end make list
        self.files = lst

    def Destroy(self, events=None):
        self.log.debug("destroy")
        self.wnd.Destroy()

    def getData(self):
        if self.filesList.GetSelection == -1:
            return ""
        # end no selection
        return os.path.join("sound", self.files[self.filesList.GetSelection()])

    def checkInput(self, event):
        val = self.getData()
        if val == "":
            simpleDialog.dialog(
                _("エラー"),
                _("一覧から、サウンドファイルを一つ選択してください。")
            )
            return
        # end no selection
        full_path = os.path.join(constants.DATA_DIRECTORY, val)
        if not os.path.isfile(full_path):
            simpleDialog.dialog(
                _("エラー"),
                _("%(path)s というファイルが存在しません。") % {
                    "path": full_path})
            return
            # end error
        event.Skip()
