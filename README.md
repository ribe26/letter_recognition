# letter_recognition
CNNを用いて文字認識を行うツールキット


**・CNN_recognition_2.ipynb**

/picturesに入っている画像を基にCNNの文字認識モデルを作成するノートブック

モデルは「letter_recognition_model.pth」として保存される


**・letter_draw.py**

文字認識モデルの学習のためのデータセットを作るツール


お手本として表示された９種類の文字を真似して描き、保存するとキャンバスがリセットされる。

データセットの数の偏りを防ぐため、すべての文字を描いていない場合は保存ができない使用になっている。

**・Canvas.py,functions.py,.py**


letter_daraw.pyのために作成したクラスや関数が定義されている
