# -*- coding: utf-8 -*-
# Nyancode runtime module

import ctypes
import time
import wx

# メッセージを表示


def message(title, message):
    dlg = wx.MessageDialog(None, message, title, wx.OK)
    dlg.ShowModal()

# 質問ダイアログを表示


def question(title, message):
    dlg = wx.MessageDialog(None, message, title, wx.YES_NO)
    return dlg.ShowModal() == wx.ID_YES

# 一定時間待つ


def wait(t):
    time.sleep(t)
