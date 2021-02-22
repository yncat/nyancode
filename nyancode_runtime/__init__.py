# -*- coding: utf-8 -*-
# Nyancode runtime module

import random
import time
import wx


class Options:
    # 通常実行時の親ウィンドウのハンドルを格納する。外部実行されている場合は None を格納する。
    parent_window = None


options = Options()


def configure(parent_window=None):
    """モジュールの初期設定を受け取って保存する。"""
    options.parent_window = parent_window


def message(title, message):
    """メッセージを表示"""
    dlg = wx.MessageDialog(options.parent_window, message, title, wx.OK)
    dlg.ShowModal()


def question(title, message):
    """質問ダイアログを表示"""
    dlg = wx.MessageDialog(options.parent_window, message, title, wx.YES_NO)
    return dlg.ShowModal() == wx.ID_YES


def wait(t):
    """一定時間待つ"""
    time.sleep(t)


def randomPattern(max):
    """1から max までの整数を生成"""
    return random.randint(1, max)
