# clockgr - A fullscreen clock for Qt
# Copyright (C) 2015 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import math
from datetime import datetime
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
from PyQt5.QtCore import QRectF, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem,
                             QGraphicsSimpleTextItem)

from .desklet import Desklet


class DigitalClock(Desklet):

    def __init__(self):
        super().__init__()

        self.seconds = QGraphicsSimpleTextItem("00", self.root)
        self.time = QGraphicsSimpleTextItem("00:00", self.root)
        self.date = QGraphicsSimpleTextItem("  ", self.root)

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
