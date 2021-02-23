# nyancode
GUIでプログラミング的なことができる教材を目指してます。

名前はまだ適当です。とりあえず、気に入ってないことだけここに書いておきます。そしたら、ましな名前が思いつくかもしれないし、どこかから降ってくるかもしれないので。

# requirements
- Windows
- Python 3.8
- makeが動く環境

# setup
make setup
依存ライブラリをインストールして、コミット時にテストが走るように pre-commit フックが設定されます。

# run
make

# コードの自動成形
make fmt
インデントとかが勝手にきれいになります。

# test
make test

GUI部分を除いたロジックのテストです。

# exeファイルと配布用zipをビルド
make build

# キーマップをリセット
make reset-keymap

メニューに新しい項目を追加したときに実行する必要があります。
