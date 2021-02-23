# -*- coding: utf-8 -*-
# プログラム実行中画面
# Copyright (C) 2021 Yukio Nozawa <personal@nyanchangames.com>

import wx
import pywintypes

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


class RunningView(BaseView):
    def __init__(self):
        super().__init__("mainView")
        self.log.debug("created")
        self.app = globalVars.app
        self.events = Events(self, self.identifier)
        title = _("プログラム実行中") + "-" + constants.APP_NAME
        super().Initialize(
            title,
            self.app.config.getint(self.identifier, "sizeX", 800, 400),
            self.app.config.getint(self.identifier, "sizeY", 600, 300),
            self.app.config.getint(self.identifier, "positionX", 50, 0),
            self.app.config.getint(self.identifier, "positionY", 50, 0)
        )
        self.setupWidgets()

    def setupWidgets(self):
        creator = views.ViewCreator.ViewCreator(
            self.viewMode,
            self.hPanel,
            self.creator.GetSizer(),
            wx.VERTICAL,
            style=wx.EXPAND | wx.ALL,
            proportion=1)
        self.runningStatic = creator.staticText(_("プログラムを実行中"))
        self.abortButton = creator.cancelbutton(
            _("実行中止"), event=self.events.abort)


class Events(BaseEvents):
    def abort(self, event=None):
        self.parent.hFrame.Destroy()
