import os
import pandas as pd
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import functions as func
# キャンバスクラス
class Canvas(QWidget):
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        # information.csvファイルの存在確認と読み込み
        if os.path.isfile("pictures/information.csv"):
            print("CSVファイルが存在します")
            df = pd.read_csv("pictures/information.csv")
            df = df[["filename", "label"]]
            self.filelist = df.values.tolist()
            print(self.filelist)
        else:
            self.filelist=[]

        self.pen_color = QColor(255, 255, 255, 255)
        self.pen_size = 2
        self.eraser_size = 4

        self.draw_size = self.pen_size
        self.pen = True



        self.canvas_size = 32 #キャンバスの一辺のピクセル数
        self.canvas_magni = 4 #表示するキャンバスの倍率
        self.grid_area_size = self.canvas_size * self.canvas_magni

        self.draging = False #ドラッグ中かのフラグ
        #どの画像を編集しているかのフラグ
        self.drag_on_image = 0
        self.drag_on_grid = 0

        #キャンバスをまとめるリスト
        self.canvas_images = []
        self.grid_images = []
        self.grid_areas = []
        self.example_images = []
        self.example_areas = []
        self.image_total = 9

        #線を描き始めた始点と終点
        self.pen_start_x = 0
        self.pen_start_y = 0
        self.pen_end_x = 0
        self.pen_end_y = 0

        #画像を編集したかのフラグの初期化
        self.edit_flag = [False] * self.image_total

        #UIの表示
        for i in range(self.image_total):
            example_image = QImage()
            example_image.load("system/" + str(i + 1) + ".png")
            self.example_images.append(example_image)
            if i < 5:
                example_area = QRect(50 + (self.grid_area_size + 10) * i, 0, self.grid_area_size, self.grid_area_size)
            else:
                example_area = QRect(50 + (self.grid_area_size + 10) * (i - 5), (self.grid_area_size + 10) * 2, self.grid_area_size, self.grid_area_size)
            self.example_areas.append(example_area)

            canvas_image = QImage(self.canvas_size, self.canvas_size, QImage.Format_ARGB32)
            canvas_image.fill(QColor(0, 0, 0, 255))
            self.canvas_images.append(canvas_image)

            grid = QImage(self.grid_area_size, self.grid_area_size, QImage.Format_ARGB32)
            if i < 5:
                grid_area = QRect(50 + (self.grid_area_size + 10) * i, self.grid_area_size + 10, self.grid_area_size, self.grid_area_size)
            else:
                grid_area = QRect(50 + (self.grid_area_size + 10) * (i - 5), (self.grid_area_size + 10) * 3, self.grid_area_size, self.grid_area_size)
            self.grid_images.append(grid)
            self.grid_areas.append(grid_area)

            self.draw_grid(self.grid_images[i])
    
    #ペンのサイズを設定する関数
    def set_pen_size(self,size):
        self.pen_size=size
    
    #ペンの色を設定する関数
    def set_pen_color(self,color):
        self.pen_color=color

    #消しゴムのサイズを設定する関数
    def set_eraser_size(self,size):
        self.pen_size=size

    def set_pen_flag(self,flag):
        self.pen=flag


    # グリッドを描画する
    def draw_grid(self, grid):
        grid.fill(qRgba(255, 255, 25, 0))
        grid_color = QColor(150, 150, 150, 255)
        for i in range(0, self.grid_area_size, self.canvas_magni):
            for j in range(self.grid_area_size):
                grid.setPixelColor(i, j, grid_color)
                grid.setPixelColor(j, i, grid_color)
        for j in range(self.grid_area_size):
            grid.setPixelColor(self.grid_area_size - 1, j, grid_color)
            grid.setPixelColor(j, self.grid_area_size - 1, grid_color)

    # 指定されたマウス座標に点を描画する
    def drawpoint(self, image, area, mouse_x, mouse_y):
        canvas_x = int((mouse_x - area.left()) / self.canvas_magni)
        canvas_y = int((mouse_y - area.top()) / self.canvas_magni)
        for i in range(canvas_x - self.draw_size, canvas_x + self.draw_size):
            for j in range(canvas_y - self.draw_size):
                if 0 <= i < self.canvas_size and 0 <= j < self.canvas_size:
                    if abs(canvas_x - i) + abs(canvas_y - j) < self.draw_size:
                        image.setPixelColor(i, j, self.pen_color)
        self.update()

    # 始点と終点の間に線を描画する
    def drawline(self, image, area):
        canvas_start_x = int((self.pen_start_x - area.left()) / self.canvas_magni)
        canvas_start_y = int((self.pen_start_y - area.top()) / self.canvas_magni)
        canvas_end_x = int((self.pen_end_x - area.left()) / self.canvas_magni)
        canvas_end_y = int((self.pen_end_y - area.top()) / self.canvas_magni)

        draw_list = func.bresenham(canvas_start_x, canvas_start_y, canvas_end_x, canvas_end_y)

        if self.pen:
            self.draw_size = self.pen_size
        else:
            self.draw_size = self.eraser_size

        for drx, dry in draw_list:
            for i in range(drx - self.draw_size, drx + self.draw_size):
                for j in range(dry - self.draw_size, dry + self.draw_size):
                    if 0 <= i < self.canvas_size and 0 <= j < self.canvas_size:
                        if abs(drx - i) + abs(dry - j) < self.draw_size:
                            image.setPixelColor(i, j, self.pen_color)
        self.update()

    # キャンバスをクリアする
    def clear_canvas(self):
        for k in range(self.image_total):
            self.edit_flag[k] = False
            for i in range(self.canvas_size):
                for j in range(self.canvas_size):
                    self.canvas_images[k].setPixelColor(i, j, QColor(0, 0, 0, 255))
                    self.update()

    # 画像を保存する
    def save_image(self):
        #すべての画像に書き込まれていなければ保存しない
        for i in range(self.image_total):
            if not self.edit_flag[i]:
                print("すべての画像を模写してから保存してください")
                return

        for i in range(self.image_total):
            name = func.randomname(10)
            while os.path.isfile("pictures/" + name + ".png"):
                name = func.randomname(10)

            self.canvas_images[i].save("pictures/" + name + ".png")
            self.filelist.append([name + ".png", i + 1])

        save_df = pd.DataFrame(self.filelist, columns=["filename", "label"])
        save_df.to_csv("pictures/information.csv")
        self.clear_canvas()

    # ペイントイベント
    def paintEvent(self, event):
        # お手本の描画
        example_painter = QPainter(self)
        example_rect = QRect(0, 0, self.canvas_size, self.canvas_size)
        for i in range(self.image_total):
            example_painter.drawImage(self.example_areas[i], self.example_images[i], example_rect)

        # 画像の描画
        canvas_painter = QPainter(self)
        canvas_rect = QRect(0, 0, self.canvas_size, self.canvas_size)
        for i in range(self.image_total):
            canvas_painter.drawImage(self.grid_areas[i], self.canvas_images[i], canvas_rect)

        # グリッドの描画
        grid_painter = QPainter(self)
        grid_rect = QRect(0, 0, self.grid_area_size, self.grid_area_size)
        for i in range(self.image_total):
            grid_painter.drawImage(self.grid_areas[i], self.grid_images[i], grid_rect)

    # マウスを押したときの処理
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.position().toPoint()
            mx = self.mousePos.x()
            my = self.mousePos.y()
            for i in range(self.image_total):
                if self.grid_areas[i].left() <= mx <= self.grid_areas[i].right() and self.grid_areas[i].top() <= my <= self.grid_areas[i].bottom():
                    if not self.edit_flag[i]:
                        self.edit_flag[i] = True
                    self.pen_start_x = mx
                    self.pen_end_x = mx
                    self.pen_start_y = my
                    self.pen_end_y = my
                    self.draging = True
                    self.drawpoint(self.canvas_images[i], self.grid_areas[i], mx, my)
                    self.drag_on_image = self.canvas_images[i]
                    self.drag_on_grid = self.grid_areas[i]

    # マウスが動いた時の処理
    def mouseMoveEvent(self, event):
        self.mousePos = event.position().toPoint()
        mx = self.mousePos.x()
        my = self.mousePos.y()
        if self.draging:
            self.pen_end_x = mx
            self.pen_end_y = my
            self.drawline(self.drag_on_image, self.drag_on_grid)
            self.pen_start_x = mx
            self.pen_start_y = my

    # マウスを離した時の処理
    def mouseReleaseEvent(self, event):
        self.draging = False