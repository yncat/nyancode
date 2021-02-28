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
追加で、 [nyancode-runtime-std](https://github.com/yncat/nyancode-runtime-std) を、このリポジトリの1個上にディレクトリにクローンしておく。 nyancode と nyancode-runtime-std のディレクトリが並ぶ状態にする。

# run
make

# run with a sample loaded
make run-sample1

サンプル1を読み込んだ状態で起動します。別のサンプルも、数字を変えれば読み込めます。

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
