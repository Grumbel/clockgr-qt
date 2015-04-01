#!/usr/bin/env python3

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


import sys
from datetime import datetime
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import QRectF, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem)

from clockgrqt.analog_clock import AnalogClock
from clockgrqt.digital_clock import DigitalClock
from clockgrqt.calendar import CalendarDesklet
from clockgrqt.style import Style


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        central = QWidget()

        self.graphics_view = QGraphicsView(central)
        self.graphics_view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.scene = QGraphicsScene()

        self.graphics_view.setScene(self.scene)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphics_view)
        central.setLayout(layout)

        self.setCentralWidget(central)
        self.show()

        style = Style()

        self.analog_clock = AnalogClock()
        self.analog_clock.set_rect(QRectF(900 - 256, 32, 512, 512))
        self.analog_clock.set_style(style)
        self.analog_clock.set_time(datetime.now())
        self.scene.addItem(self.analog_clock.root)

        self.digital_clock = DigitalClock()
        self.digital_clock.set_rect(QRectF(32, 670, 640, 200))
        self.digital_clock.set_style(style)
        self.digital_clock.update(datetime.now())
        self.scene.addItem(self.digital_clock.root)

        self.calendar = CalendarDesklet()
        self.calendar.set_rect(QRectF(32, 32, 512, 412))
        self.calendar.set_style(style)
        self.calendar.update(datetime.now())
        self.scene.addItem(self.calendar.root)
        # self.calendar.root.setPos(-400, 0)

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.my_update)
        self.timer.start()

        # self.world = self.add_desklet(WorldDesklet(),    (1200 - 540 - 32, 900 - 276 - 32, 540, 276))
        # self.stopwatch = self.add_desklet(StopWatch(),       (32, 64, 500, 180))

        self.setFixedSize(1200, 900)

    def my_update(self, *args):
        now = datetime.now()
        self.analog_clock.set_time(now)
        self.digital_clock.update(now)

    def closeEvent(self, event):
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    QApplication.instance().exec()


if __name__ == "__main__":
    main()


# EOF #
