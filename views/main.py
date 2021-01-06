# -*- coding: utf-8 -*-
# main view
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
# Copyright (C) 2019-2020 yamahubuki <itiro.ishino@gmail.com>

import logging
import os
import sys
import wx
import re
import ctypes
import pywintypes

import constants
import errorCodes
import globalVars
import menuItemsStore
import projectManager

from .base import *
from simpleDialog import *

from views import mkDialog
from views import sample
from views import versionDialog


class MainView(BaseView):
    def __init__(self):
        super().__init__("mainView")
        self.log.debug("created")
        self.app = globalVars.app
        self.events = Events(self, self.identifier)
        title = constants.APP_NAME
        super().Initialize(
            title,
            self.app.config.getint(self.identifier, "sizeX", 800, 400),
            self.app.config.getint(self.identifier, "sizeY", 600, 300),
            self.app.config.getint(self.identifier, "positionX", 50, 0),
            self.app.config.getint(self.identifier, "positionY", 50, 0)
        )
        self.InstallMenuEvent(Menu(self.identifier), self.events.OnMenuSelect)
        self.setupWidgets()
        self.setupNewProject()
        self.updateList()

    def setupWidgets(self):
        creator = views.ViewCreator.ViewCreator(self.viewMode, self.hPanel, self.creator.GetSizer(
        ), wx.VERTICAL, style=wx.EXPAND | wx.ALL, proportion=1)
        self.codeBlockList, self.codeBlockListStatic = creator.listCtrl(
            _("コードブロック"), None, wx.LC_REPORT, proportion=1, sizerFlag=wx.EXPAND)
        self.codeBlockList.InsertColumn(0, _("名前"))
        self.codeBlockList.InsertColumn(1, _("パラメータ"))
        self.codeBlockList.InsertColumn(2, _("コードブロック"))

    def setupNewProject(self):
        self.projectManager = projectManager.ProjectManager()
        self.projectManager.new()

    def updateList(self):
        self.codeBlockList.DeleteAllItems()
        for elem in self.projectManager.getList():
            self.codeBlockList.Append(elem)


class Menu(BaseMenu):
    def Apply(self, target):
        """指定されたウィンドウに、メニューを適用する。"""

        # メニューの大項目を作る
        self.hFileMenu = wx.Menu()
        self.hHelpMenu = wx.Menu()

        # ファイルメニュー
        self.RegisterMenuCommand(self.hFileMenu, [
            "FILE_EXIT",
        ])

        # ヘルプメニューの中身
        self.RegisterMenuCommand(self.hHelpMenu, [
            "HELP_UPDATE",
            "HELP_VERSIONINFO",
        ])

        # メニューバーの生成
        self.hMenuBar.Append(self.hFileMenu, _("ファイル"))
        self.hMenuBar.Append(self.hHelpMenu, _("ヘルプ"))
        target.SetMenuBar(self.hMenuBar)


class Events(BaseEvents):
    def OnMenuSelect(self, event):
        """メニュー項目が選択されたときのイベントハンドら。"""
        # ショートカットキーが無効状態のときは何もしない
        if not self.parent.shortcutEnable:
            event.Skip()
            return

        selected = event.GetId()  # メニュー識別しの数値が出る

        if selected == menuItemsStore.getRef("FILE_EXIT"):
            self.Exit()
        if selected == menuItemsStore.getRef("HELP_UPDATE"):
            globalVars.update.update()

        if selected == menuItemsStore.getRef("HELP_VERSIONINFO"):
            d = versionDialog.dialog()
            d.Initialize()
            r = d.Show()
