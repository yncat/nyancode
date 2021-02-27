# dll path や import path などの大人の事情を解決する
# nyancode.py の一番最初でインポートしている
# 昔は os と sys を先にインポートして直接やっていたのだが、 auto formatter が勝手にインポートの順番を入れ替えちゃってぶっこわれるのでファイルを分けた。

import os, sys

# 開発用に、 nyancode_runtime_std を1個上のディレクトリのリポジトリから読めるようにする
sys.path.append("../nyancode-runtime-std")

# Python3.8対応
# dllやモジュールをカレントディレクトリから読み込むように設定
if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    os.add_dll_directory(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

