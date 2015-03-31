import math
from datetime import datetime
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem)
from PyQt5.Qt import Qt


class AnalogClock:

    def get_item(self):
        return self.group

    def __init__(self):
        super().__init__()

        self.width = 512
        self.height = 512

        self.pen = QPen()
        self.pen.setWidth(6)
        self.no_pen = QPen(Qt.NoPen)
        self.brush = QBrush(QColor(255, 0, 0))

        self.group = QGraphicsItemGroup()

        self.center_x = self.width / 2.0
        self.center_y = self.height / 2.0
        self.radius = min(self.width, self.height) / 2.0 - 3.0

        center_x = self.center_x
        center_y = self.center_y
        radius = self.radius

        # self.pen.setColor(QColor(*self.style.foreground_color))
        self.pen.setWidth(6)
        circle = QGraphicsEllipseItem(center_x - radius,
                                      center_y - radius,
                                      2 * radius,
                                      2 * radius,
                                      self.group)
        circle.setPen(self.pen)

        # cr.set_source_rgb(*self.style.midcolor)
        # cr.set_line_cap(cairo.LINE_CAP_ROUND)
        self.pen.setCapStyle(Qt.RoundCap)
        for i in range(0, 60):
            angle = i * 2.0 * math.pi / 60.0
            if i % 5 == 0:
                line = QGraphicsLineItem(
                    center_x + math.cos(angle) * radius * 0.85,
                    center_y + math.sin(angle) * radius * 0.85,
                    center_x + math.cos(angle) * radius * 0.95,
                    center_y + math.sin(angle) * radius * 0.95,
                    self.group)
                self.pen.setColor(QColor(0, 0, 0))
                self.pen.setWidth(6)
                line.setPen(self.pen)
            else:
                line = QGraphicsLineItem(
                    center_x + math.cos(angle) * radius * 0.90,
                    center_y + math.sin(angle) * radius * 0.90,
                    center_x + math.cos(angle) * radius * 0.95,
                    center_y + math.sin(angle) * radius * 0.95,
                    self.group)
                self.pen.setColor(QColor(127, 127, 127))
                self.pen.setWidth(4.0)
                line.setPen(self.pen)

        # hour
        self.pen.setColor(QColor(0, 0, 0)) # cr.set_source_rgb(*self.style.foreground_color)
        self.pen.setWidth(16)
        self.pen.setCapStyle(Qt.RoundCap)
        self.hours_hand = QGraphicsLineItem(self.group)
        self.hours_hand.setPen(self.pen)

        # minute
        self.pen.setColor(QColor(0, 0, 0)) # cr.set_source_rgb(*self.style.foreground_color)
        self.pen.setWidth(12)
        self.pen.setCapStyle(Qt.RoundCap)
        self.minutes_hand = QGraphicsLineItem(self.group)
        self.minutes_hand.setPen(self.pen)

        # second
        self.pen.setColor(QColor(127, 127, 127)) # cr.set_source_rgb(*self.style.midcolor)
        self.pen.setWidth(4)
        self.pen.setCapStyle(Qt.RoundCap)
        self.seconds_hand = QGraphicsLineItem(self.group)
        self.seconds_hand.setPen(self.pen)

        self.brush.setColor(QColor(255, 255, 255)) # cr.set_source_rgb(*self.style.background_color)
        circle = QGraphicsEllipseItem(center_x - 5, center_y - 5, 10, 10, self.group)
        circle.setBrush(self.brush)

    def update(self, now):
        hour = (now.hour / 12.0 + now.minute / 60.0 / 12.0) * 2.0 * math.pi - math.pi / 2.0
        minute = (now.minute / 60.0 + now.second / 60.0 / 60.0) * 2.0 * math.pi - math.pi / 2.0
        second = (now.second / 60.0) * 2.0 * math.pi - math.pi / 2.0

        self.set_seconds(second)
        self.set_minutes(minute)
        self.set_hours(hour)

    def set_seconds(self, n):
        self.seconds_hand.setLine(
            self.center_x + math.cos(n) * self.radius * 0.0,
            self.center_y + math.sin(n) * self.radius * 0.0,
            self.center_x + math.cos(n) * self.radius * 0.8,
            self.center_y + math.sin(n) * self.radius * 0.8)

    def set_minutes(self, n):
        self.minutes_hand.setLine(
            self.center_x + math.cos(n) * self.radius * 0.0,
            self.center_y + math.sin(n) * self.radius * 0.0,
            self.center_x + math.cos(n) * self.radius * 0.8,
            self.center_y + math.sin(n) * self.radius * 0.8)

    def set_hours(self, n):
        self.hours_hand.setLine(
            self.center_x + math.cos(n) * self.radius * 0.0,
            self.center_y + math.sin(n) * self.radius * 0.0,
            self.center_x + math.cos(n) * self.radius * 0.45,
            self.center_y + math.sin(n) * self.radius * 0.45)


# EOF #
