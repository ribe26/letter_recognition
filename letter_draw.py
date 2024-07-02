import os
import sys
import Canvas as cvs
import pandas as pd
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import functions as func


# picturesディレクトリの存在確認と作成
if os.path.isdir("pictures/"):
    print("ディレクトリが存在します")
else:
    os.mkdir("pictures/")

# メインウィンドウクラス
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.canvas = cvs.Canvas()
        self.setCentralWidget(self.canvas)
        self.initUI()

    # UIの初期化
    def initUI(self):
        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle("PAINTapl")
        self.setupRadioButtons()
        self.setupButtons()

    # ラジオボタンの設定
    def setupRadioButtons(self):
        self.radioGroup = QButtonGroup(self)
        self.radio2_id = 2
        radio1 = QRadioButton(self)
        radio1.setText("ペン")
        radio1.move(800, 380)
        self.radioGroup.addButton(radio1, self.radio2_id)

        self.radio3_id = 3
        radio2 = QRadioButton(self)
        radio2.setText("消しゴム")
        radio2.move(800, 410)
        self.radioGroup.addButton(radio2, self.radio3_id)

        radio1.setChecked(True)
        self.radioGroup.buttonClicked.connect(self.onRadioButtonChanged)

    # ラジオボタンの状態変化を処理する
    def onRadioButtonChanged(self):
        if self.radioGroup.checkedId() == self.radio2_id:
            self.canvas.set_pen_color(QColor(255, 255, 255, 255))
            #self.canvas.set_pen_size(4)
            self.canvas.set_pen_flag(True)

        elif self.radioGroup.checkedId() == self.radio3_id:
            self.canvas.set_pen_color(QColor(0, 0, 0, 255))
            self.canvas.set_pen_flag(False)

    # ボタンの設定
    def setupButtons(self):
        button_clear = QPushButton(self)
        button_clear.setText("全部消す")
        button_clear.move(800, 500)
        button_clear.pressed.connect(self.canvas.clear_canvas)

        button_save = QPushButton(self)
        button_save.setText("保存")
        button_save.move(800, 550)
        button_save.pressed.connect(self.canvas.save_image)


# メイン関数
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
