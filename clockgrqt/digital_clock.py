import math
from datetime import datetime
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem,
                             QGraphicsSimpleTextItem)
from PyQt5.Qt import Qt


class DigitalClock:

    def get_item(self):
        return self.group

    def __init__(self):
        super().__init__()

        self.group = QGraphicsItemGroup()

        self.seconds = QGraphicsSimpleTextItem("00", self.group)
        self.time = QGraphicsSimpleTextItem("00:00", self.group)
        self.date = QGraphicsSimpleTextItem("  ", self.group)

        # pen = QPen(QColor(255, 0, 0))
        # pen.setWidth(6)

        # self.seconds.setPen(pen)
        # self.time.setPen(pen)
        # self.date.setPen(pen)

        self.seconds.setFont(QFont("Arial", 192 * 0.6, -1, False))
        self.time.setFont(QFont("Arial", 192 * 0.75, -1, False))
        self.date.setFont(QFont("Arial", 56, -1, False))

        x = -200
        y = 500

        # FIXME: Text alignment is all fudged up, see:
        # http://www.cesarbs.org/blog/2011/05/30/aligning-text-in-qgraphicstextitem/
        self.date.setPos(x, y + self.time.boundingRect().height() - 30)
        self.time.setPos(x, y)
        self.seconds.setPos(x + self.time.boundingRect().width() + 32,
                            y + self.time.boundingRect().height() - self.seconds.boundingRect().height() - 10)

        # cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
        # cr.set_source_rgb(*self.style.foreground_color)

        # cr.set_font_size(192 * 0.75)
        # xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

    def update(self, now):
        date = now.strftime("%A, %d. %B %Y")
        time = now.strftime("%H:%M")
        seconds = now.strftime("%S")

        print(date, time, seconds)

        # pos_x = 0
        # pos_y = 0

        # pos_y += height

        # cr.move_to(pos_x, pos_y)
        self.time.setText(time)

        # cr.set_font_size(192 * 0.6)
        # cr.move_to(pos_x + width + 32, pos_y)
        self.seconds.setText(seconds)

        # pos_y += yadvance
        # cr.set_font_size(56)
        # xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(date)
        # pos_y += height

        # cr.move_to(pos_x, pos_y)
        self.date.setText(date)


# EOF #
