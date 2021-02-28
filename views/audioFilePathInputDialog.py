# -*- coding: utf-8 -*-
# audio file path input dialog

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
        self.InstallControls()
        return True

    def InstallControls(self):
        """いろんなwidgetを設置する。"""
        creator = views.ViewCreator.ViewCreator(
            self.viewMode, self.panel, self.sizer, wx.VERTICAL, 20)
        self.input, static = creator.inputbox(
            self.parameter_display_name,
            defaultValue=self.default_value,
            x=400
        )
        self.browseButton = creator.button(
            _("参照"), event=self.browse, size=(100, 100))
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
        return self.input.GetValue()

    def checkInput(self, event):
        val = self.input.GetValue()
        full_path = os.path.join(constants.DATA_DIRECTORY, val)
        if not os.path.isfile(full_path):
            simpleDialog.dialog(
                _("エラー"),
                _("%(path)s というファイルが存在しません。") % {
                    "path": full_path})
            return
            # end error
        if not self._checkDataPath(val):
            return
        event.Skip()

    def browse(self, event):
        ext = ";".join(["*." + elem for elem in self.extensions])
        dir = os.path.join(os.getcwd(), "data\\sound")
        with wx.FileDialog(self.wnd, _("サウンドファイルを選択"), wildcard=_("サウンドファイル") + "(" + ext + ")|" + ext, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, defaultDir=dir) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        # end dialog
        if not self._checkDataPath(path):
            return
        self.input.ChangeValue(
            os.path.relpath(
                path, start=constants.DATA_DIRECTORY))

    def _checkDataPath(self, path):
        # ポータビリティを高めるために、 data ディレクトリの外にあるファイルは読み込めないようにする。
        # ただし、data ディレクトリからの相対パスで観て、ちゃんとファイルがある場合はOKとする
        # エラーがある場合は、ここでダイアログを出して、 False を返す。
        # True を返した場合は、呼び出し元は処理を続行してよい。
        exists = os.path.isfile(os.path.join(constants.DATA_DIRECTORY, path))
        if not path.startswith(constants.DATA_DIRECTORY) and not exists:
            simpleDialog.dialog(_("エラー"), _(
                "このファイルを使いたい場合は、アプリケーションの data ディレクトリ、またはそのサブディレクトリにファイルをコピーしてから、コピーしたファイルを選択してください。"))
            return False
        # end だめ
        return True
