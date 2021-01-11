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
import defaultKeymap
import globalVars
import keymap
import menuItemsStore
import node
import projectManager

from .base import *
from simpleDialog import *

from views import strInputDialog
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
        creator = views.ViewCreator.ViewCreator(
            self.viewMode,
            self.hPanel,
            self.creator.GetSizer(),
            wx.VERTICAL,
            style=wx.EXPAND | wx.ALL,
            proportion=1)
        self.codeBlockList, self.codeBlockListStatic = creator.listCtrl(
            _("コードブロック"), None, wx.LC_REPORT, proportion=1, sizerFlag=wx.EXPAND)
        self.codeBlockList.InsertColumn(0, _("名前"))
        self.codeBlockList.InsertColumn(1, _("パラメータ"))
        self.codeBlockList.InsertColumn(2, _("コードブロック"))

    def setupNewProject(self):
        self.projectManager = projectManager.ProjectManager()
        self.projectManager.new(_("新規プロジェクト"))

    def updateList(self):
        self.codeBlockList.DeleteAllItems()
        for elem in self.projectManager.getList():
            self.codeBlockList.Append(elem)

    def getSelectedIndices(self):
        first = self.codeBlockList.GetFirstSelected()
        if first == -1:
            return None
        lst = [first]
        next = first
        while True:
            next = self.codeBlockList.GetNextSelected(next)
            if next == -1:
                break
            lst.append(next)
        # end while
        return lst


class Menu(BaseMenu):
    def Apply(self, target):
        """指定されたウィンドウに、メニューを適用する。"""

        # メニューの大項目を作る
        self.hFileMenu = wx.Menu()
        self.hEditMenu = wx.Menu()
        self.hInsertMenu = wx.Menu()
        self.hExecMenu = wx.Menu()
        self.hHelpMenu = wx.Menu()

        # ファイルメニュー
        self.RegisterMenuCommand(self.hFileMenu, [
            "FILE_OPEN",
        ])
        self.RegisterMenuCommand(self.hFileMenu, [
            "FILE_SAVE",
        ])
        self.RegisterMenuCommand(self.hFileMenu, [
            "FILE_SAVEAS",
        ])
        self.RegisterMenuCommand(self.hFileMenu, [
            "FILE_EXIT",
        ])

        # 編集メニュー
        self.RegisterMenuCommand(self.hEditMenu, [
            "EDIT_DELETENODE",
        ])

        # 挿入メニュー
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_IO_PRINT",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("入出力"), submenu)

        # 実行メニュー
        self.RegisterMenuCommand(self.hExecMenu, [
            "EXEC_RUN",
        ])
        self.RegisterMenuCommand(self.hExecMenu, [
            "EXEC_OUTPUTPROGRAM",
        ])

        # ヘルプメニュー
        self.RegisterMenuCommand(self.hHelpMenu, [
            "HELP_UPDATE",
            "HELP_VERSIONINFO",
        ])

        # メニューバーの生成
        self.hMenuBar.Append(self.hFileMenu, _("ファイル"))
        self.hMenuBar.Append(self.hEditMenu, _("編集"))
        self.hMenuBar.Append(self.hInsertMenu, _("挿入"))
        self.hMenuBar.Append(self.hExecMenu, _("実行"))
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

        # ファイル関係
        if selected == menuItemsStore.getRef("FILE_OPEN"):
            self.open()
        if selected == menuItemsStore.getRef("FILE_SAVE"):
            self.save()
        if selected == menuItemsStore.getRef("FILE_SAVEAS"):
            self.saveAs()

        if selected == menuItemsStore.getRef("FILE_EXIT"):
            self.Exit()

        # 編集操作
        if selected == menuItemsStore.getRef("EDIT_DELETENODE"):
            self.deleteNode()

        # ノード関係
        if selected == menuItemsStore.getRef("INSERT_IO_PRINT"):
            self.addNode(node.new("PrintNode"))

        # 実行関係
        if selected == menuItemsStore.getRef("EXEC_RUN"):
            self.run()
        if selected == menuItemsStore.getRef("EXEC_OUTPUTPROGRAM"):
            self.outputProgram()

        # その他
        if selected == menuItemsStore.getRef("HELP_UPDATE"):
            globalVars.update.update()
        if selected == menuItemsStore.getRef("HELP_VERSIONINFO"):
            d = versionDialog.dialog()
            d.Initialize()
            r = d.Show()

    def addNode(self, node):
        input_index = 0
        parameter_count = len(node.parameter_constraints)
        parameter_names = list(node.parameter_constraints.keys())
        canceled = False

        while input_index != parameter_count:
            if input_index == -1:
                canceled = True
                break
            # end cancel

            parameter_name = parameter_names[input_index]

            # パラメータの型に応じた入力ダイアログを出す
            if node.parameter_constraints[parameter_name] == str:
                d = strInputDialog.dialog()
                d.Initialize(node.parameter_display_names[parameter_name])
                r = d.Show()
            # end str

            if r == wx.ID_CANCEL:
                input_index -= 1
                continue
            # end cancel
            node.setSingleParameter(parameter_name, d.getData())
            input_index += 1
        # end while
        index = self.parent.codeBlockList.GetFocusedItem() + 1
        self.parent.projectManager.insertNodeToCurrentBlock(node, index=index)
        self.parent.updateList()
        self.parent.codeBlockList.Focus(index)
        self.parent.codeBlockList.Select(index)

    def deleteNode(self):
        selected = self.parent.getSelectedIndices()
        if not selected or len(selected) == 0:
            dialog(_("エラー"), _("削除する項目が選択されていません。"))
            return
        # end nothing is selected
        res = yesNoDialog(
            _("確認"),
            _("選択中の%(num)d項目を削除してもよろしいですか？") % {
                "num": len(selected)})
        if res == wx.ID_NO:
            return
        # end canceled
        self.parent.projectManager.deleteMultipleNodes(selected)
        self.parent.updateList()

    def outputProgram(self):
        with wx.FileDialog(self.parent.hFrame, _("Python コードを保存"), wildcard=_("Python スクリプト") + "(*.py)|*.py", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        # end dialog
        try:
            self.parent.projectManager.savePythonProgram(path)
        except Exception as e:
            dialog(_("エラー"), "プログラムの出力中にエラーが発生しました。\n%s" % e)
        # end except

    def save(self):
        if self.parent.projectManager.mustSaveAs():
            self.saveAs()
            return
        # end must save as
        try:
            self.parent.projectManager.save()
        except Exception as e:
            dialog(_("エラー"), _("プロジェクトの保存に失敗しました。\n%s" % e))
        # end except

    def saveAs(self):
        with wx.FileDialog(self.parent.hFrame, _("プロジェクトを保存"), wildcard=_("プロジェクトファイル") + "(*.ncp)|*.ncp", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        # end dialog
        try:
            self.parent.projectManager.saveAs(path)
        except Exception as e:
            dialog(_("エラー"), _("プロジェクトの保存に失敗しました。\n%s" % e))
        # end except

    def open(self):
        with wx.FileDialog(self.parent.hFrame, _("プロジェクトを開く"), wildcard=_("プロジェクトファイル") + "(*.ncp)|*.ncp", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        # end dialog
        try:
            self.parent.projectManager.load(path)
        except Exception as e:
            dialog(_("エラー"), _("プロジェクトの読み込みに失敗しました。\n%s" % e))
        # end except
        self.parent.updateList()

    def run(self):
        try:
            self.parent.projectManager.run()
        except Exception as e:
            dialog(_("実行時エラー"), _("プログラムの実行中にエラーが起きました。\n%s" % e))
            