#!/usr/bin/env python3

import sys
from datetime import datetime
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem)

from clockgrqt.analogclock import AnalogClock


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

        self.clock = AnalogClock()
        self.clock.update(datetime.now())
        self.scene.addItem(self.clock.get_item())

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.my_update)
        self.timer.start()

        self.setFixedSize(640, 640)

    def my_update(self, *args):
        self.clock.update(datetime.now())

    def closeEvent(self, event):
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    QApplication.instance().exec()


if __name__ == "__main__":
    main()


# EOF #
