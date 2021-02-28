# -*- coding: utf-8 -*-
# main view
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
# Copyright (C) 2019-2020 yamahubuki <itiro.ishino@gmail.com>

import sys
import wx

import block
import constants
import errorCodes
import defaultKeymap
import globalVars
import keymap
import menuItemsStore
import node
import nodeIO
import project

from .base import *
from simpleDialog import *

from views import strInputDialog, floatInputDialog, intInputDialog, audioFilePathInputDialog
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
        self.setupNewOrExistingProject()
        self.updateTitleBarBasedOnProject()
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
        self.codeBlockList.InsertColumn(0, _("名前"), width=280)
        self.codeBlockList.InsertColumn(1, _("パラメータ"), width=780)
        self.codeBlockList.InsertColumn(2, _("コードブロック"), width=150)
        self.codeBlockList.loadColumnInfo(self.identifier, "codeBlockList")
        self.codeBlockList.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.events.openNode)

    def setupNewOrExistingProject(self):
        l = getLogger("%s.%s" % (constants.LOG_PREFIX, "ProjectManager"))
        nio = nodeIO.NodeIO()
        pio = project.IO()
        self.projectManager = project.Manager(
            logger=l, nodeIO=nio, projectIO=pio)
        # コマンドライン引数にファイル名が入っていれば、それをプロジェクトとして読もうと試みる。成功したらそのプロジェクトを使い、失敗したら新規プロジェクトにフォールバックする。
        if len(sys.argv) == 1:
            self._setupNewProject()
            return
        # end 引数がないのでさっさと帰る
        load_ok = True
        try:
            self.projectManager.load(sys.argv[1])
        except BaseException:
            load_ok = False
        # end 読み込み失敗
        if not load_ok:
            self._setupNewProject()

    def _setupNewProject(self):
        self.projectManager.new(_("新規プロジェクト"))

    def updateTitleBarBasedOnProject(self):
        pn = _("新規プロジェクト") if self.projectManager.getProjectName(
        ) == "" else self.projectManager.getProjectName()
        self.hFrame.SetTitle(pn + " - " + constants.APP_NAME)

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
        self.hMoveMenu = wx.Menu()
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
            "EDIT_OPENNODE",
        ])
        self.RegisterMenuCommand(self.hEditMenu, [
            "EDIT_DELETENODE",
        ])

        # 挿入メニュー
        # 入出力
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_MESSAGE",
        ])
        self.RegisterMenuCommand(submenu, [
            "INSERT_QUESTION_BRANCH",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("入出力"), submenu)

        # 条件分岐
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_QUESTION_BRANCH",
        ])
        self.RegisterMenuCommand(submenu, [
            "INSERT_FIFTY_FIFTY_BRANCH",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("条件分岐"), submenu)

        # 繰り返し
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_LOOP",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("繰り返し"), submenu)

        # サウンド
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_PLAYONESHOT",
        ])
        self.RegisterMenuCommand(submenu, [
            "INSERT_PLAYONESHOTANDWAIT",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("サウンド"), submenu)

        # 時間
        submenu = wx.Menu()
        self.RegisterMenuCommand(submenu, [
            "INSERT_WAIT",
        ])
        self.RegisterMenuCommand(self.hInsertMenu, "", _("時間"), submenu)

        # 移動メニュー
        self.RegisterMenuCommand(self.hMoveMenu, [
            "MOVE_LEAVE",
        ])
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
        self.hMenuBar.Append(self.hMoveMenu, _("移動"))
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
        if selected == menuItemsStore.getRef("EDIT_OPENNODE"):
            self.openNode()

        # ノード関係
        if selected == menuItemsStore.getRef("INSERT_MESSAGE"):
            self.addNode(node.new("MessageNode"))
        if selected == menuItemsStore.getRef("INSERT_QUESTION_BRANCH"):
            self.addNode(node.new("QuestionBranchNode"))
        if selected == menuItemsStore.getRef("INSERT_FIFTY_FIFTY_BRANCH"):
            self.addNode(node.new("FiftyFiftyBranchNode"))
        if selected == menuItemsStore.getRef("INSERT_LOOP"):
            self.addNode(node.new("LoopNode"))
        if selected == menuItemsStore.getRef("INSERT_PLAYONESHOT"):
            self.addNode(node.new("PlayOneShotNode"))
        if selected == menuItemsStore.getRef("INSERT_PLAYONESHOTANDWAIT"):
            self.addNode(node.new("PlayOneShotAndWaitNode"))
        if selected == menuItemsStore.getRef("INSERT_WAIT"):
            self.addNode(node.new("WaitNode"))

        # 移動関係
        if selected == menuItemsStore.getRef("MOVE_LEAVE"):
            self.leave()
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

    def addNode(self, nd):
        input_index = 0
        parameter_count = len(nd.parameter_constraints)
        parameter_names = list(nd.parameter_constraints.keys())
        canceled = False

        while input_index != parameter_count:
            if input_index == -1:
                canceled = True
                break
            # end cancel

            parameter_name = parameter_names[input_index]
            value, inner_canceled = self.getNodeParameterBasedOnType(
                nd, parameter_name)
            if inner_canceled:
                input_index -= 1
                continue
            # end cancel
            nd.setSingleParameter(parameter_name, value)
            input_index += 1
        # end while

        # パラメータ入力を全部キャンセルされたら、ブロックの追加をやめる
        if canceled:
            dialog(_("取り消し"), _("ブロックの追加を取り消しました。"))
            return
        # end cancel

        # 必要なブロックを追加
        for elem in nd.child_block_constraints:
            nd.setSingleChildBlock(
                elem, block.Block(
                    parent_node=nd))
        # end for
        b = list(nd.child_block_display_names.values())
        # 1: display_name_1\n2: display_name2... のような文字を作る、表示用
        bs = "\n".join(["%d: %s" % (i + 1, b[i]) for i in range(len(b))])
        if len(b) > 0:
            dialog(_("サブブロック追加"), _("%(num)d個のサブブロックが追加されました。") %
                   {"num": len(b)} + "\n" + bs)
        # end ブロック追加したのでメッセージ表示
        index = self.parent.codeBlockList.GetFocusedItem() + 1
        self.parent.projectManager.insertNodeToCurrentBlock(nd, index=index)
        self.parent.updateList()
        self.parent.codeBlockList.Focus(index)
        self.parent.codeBlockList.Select(index)

    def getNodeParameterBasedOnType(self, nd, parameter_name):
        # すでに値が入っている場合は、それを初期値として読み込む
        default_value = nd.parameterOrBlankString(parameter_name)

        # パラメータの型に応じた入力ダイアログを出す
        dialog_map = {
            node.ParameterTypes.STR_SINGLELINE: strInputDialog.dialog,
            node.ParameterTypes.STR_MULTILINE: strInputDialog.dialog,
            node.ParameterTypes.INT: intInputDialog.dialog,
            node.ParameterTypes.FLOAT: floatInputDialog.dialog,
            node.ParameterTypes.PATH_AUDIOFILE: audioFilePathInputDialog.dialog
        }
        d = dialog_map[nd.parameter_constraints[parameter_name]]()
        d.Initialize(
            nd.parameter_display_names[parameter_name],
            default_value)
        r = d.Show()
        if r == wx.ID_CANCEL:
            return None, True
        # end cancel
        return d.getData(), False

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

    def openNode(self, event=None):
        index = self.parent.codeBlockList.GetFocusedItem()
        if index == -1:
            return
        nd = self.parent.projectManager.getNodeAt(index)
        menu = wx.Menu()
        i = 10000  # ブロックパラメータの編集は ID 10000から
        for elem in list(nd.parameter_display_names.values()):
            menu.Append(i, _("%(parameter)sを編集") % {"parameter": elem})
            i += 1
        # end ブロックパラメータ編集の選択肢
        i = 20000  # サブブロックへの移動は ID 20000から
        for elem in list(nd.child_block_display_names.values()):
            menu.Append(i, _("%(block)s サブブロックに入る") % {"block": elem})
            i += 1
        # end サブブロックに入る選択肢
        selected = self.parent.codeBlockList.GetPopupMenuSelectionFromUser(
            menu)
        if selected >= 10000 and selected < 20000:
            self.editSingleParameter(nd, list(
                nd.parameters)[selected - 10000])
        # end edit single parameter
        if selected >= 20000:
            self.parent.projectManager.enterSubBlock(
                index, list(nd.child_blocks)[selected - 20000])
        # end サブブロックに入る
        self.parent.updateList()

    def editSingleParameter(self, nd, parameter_name):
        value, canceled = self.getNodeParameterBasedOnType(
            nd, parameter_name)
        if canceled:
            return
        nd.setSingleParameter(parameter_name, value)

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
        self.parent.updateTitleBarBasedOnProject()
        self.parent.updateList()

    def run(self):
        try:
            runner = self.parent.projectManager.prepairRun()
            runner.run()
        except Exception as e:
            dialog(_("実行時エラー"), _("プログラムの実行中にエラーが起きました。\n%s" % e))

    def leave(self):
        ret = self.parent.projectManager.leaveSubBlock()
        if ret is None:
            return
        self.parent.updateList()
        self.parent.codeBlockList.Focus(ret)
        self.parent.codeBlockList.Select(ret)

    def Exit(self, event=None):
        if self.parent.projectManager.has_changes:
            dlg = wx.MessageDialog(
                self.parent.hFrame,
                _("プロジェクトが変更されています。保存してから終了しますか？"),
                _("確認"),
                wx.YES_NO | wx.ICON_QUESTION)
            ret = dlg.ShowModal()
            if ret == wx.ID_YES:
                self.save()
        # end save
        self.parent.codeBlockList.saveColumnInfo()
        BaseEvents.Exit(self, event)
