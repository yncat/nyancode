# -*- coding: utf-8 -*-
# Nyancode runtime module

import ctypes
import time

# メッセージを表示


def message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)

# 一定時間待つ


def wait(t):
    time.sleep(t)
