# nyancode
GUIでプログラミング的なことができる教材を目指してます。

名前はまだ適当です。とりあえず、気に入ってないことだけここに書いておきます。そしたら、ましな名前が思いつくかもしれないし、どこかから降ってくるかもしれないので。

# requirements
- Windows
- Python 3.8

# setup
コマンドプロンプトなどで、

pip install -r requirements.txt

# run
python application.py

Windows用のMSIインストーラでPythonを入れた場合は、 py application.py かも。

# test
python -m unittest discover tests

GUI部分を除いたロジックのテストです。
