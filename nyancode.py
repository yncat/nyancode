# -*- coding: utf-8 -*-
# Application startup file

import init
import traceback
import nyancode_runtime_std  # dummy
import simpleDialog
import app as application
import globalVars
import keymap
import os
import sys

# カレントディレクトリを設定
if hasattr(sys, "frozen"):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.abspath(os.path.dirname(__file__)))


def exchandler(type, exc, tb):
    msg = traceback.format_exception(type, exc, tb)
    print("".join(msg))
    try:
        f = open("errorLog.txt", "a")
        f.writelines(msg)
        f.close()
    except BaseException:
        pass
    simpleDialog.winDialog(
        "error", "An error has occured. Contact the developer for further assistance. Detail:" + "\n".join(msg[-2:]))
    sys.exit(1)


sys.excepthook = exchandler


def main():
    try:
        if os.path.exists("errorLog.txt"):
            os.remove("errorLog.txt")
    except BaseException:
        pass
    app = application.Main()
    globalVars.app = app
    app.initialize()
    app.MainLoop()
    app.config.write()


#global schope
if __name__ == "__main__":
    main()
