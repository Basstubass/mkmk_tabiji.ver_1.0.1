app.pyの名前変更：export FLASK_APP=application.py

仮想環境に切り替えたい時：source myenv/bin/activate
仮想環境から出たい時；deactivate

仮想環境をインストール：python3.10 -m venv myenv

pipとpip3は別のもの

#Gitメモ
gitでブランチを変更：git checkout 〇〇
ローカルのブランチ一覧：git branch
リモートのブランチ一覧：git branch -r
ローカルのリモートブランチを最新化：git fetch
特定のローカルブランチに特定のリモートブランチの差分をpullする：$ git pull origin REMOTE-BRANCH-NAME:LOCAL-BRANCH-NAME
detached branch(ブランチがない)：git branch 〇〇
他のメンバーがリモートにpushしたブランチをローカルで参照したり動かしたりしたい：git checkout -b <ブランチ名> origin/<ブランチ名>

