# -*- coding: utf-8 -*-
# Nyancode runtime module

import ctypes

# メッセージを表示


def print(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)
