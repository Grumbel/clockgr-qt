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
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.Qt import Qt

from .desklet import Desklet


class AnalogClock(Desklet):

    def __init__(self):
        super().__init__()

        self.center_x = 0
        self.center_y = 0
        self.radius = 1

        self.now = datetime.utcfromtimestamp(0)

        # build the clock face
        self.circle = QGraphicsEllipseItem(self.root)

        self.lines = []
        for i in range(0, 60):
            self.lines.append(QGraphicsLineItem(self.root))

        self.hours_hand = QGraphicsLineItem(self.root)
        self.minutes_hand = QGraphicsLineItem(self.root)
        self.seconds_hand = QGraphicsLineItem(self.root)

        self.hand_circle = QGraphicsEllipseItem(self.root)

    def set_style(self, style):
        super().set_style(style)

        # minute
        pen = QPen(self.style.foreground_color)
        pen.setWidth(12)
        pen.setCapStyle(Qt.RoundCap)
        self.minutes_hand.setPen(pen)

        # hour
        pen = QPen(self.style.foreground_color)
        pen.setWidth(16)
        pen.setCapStyle(Qt.RoundCap)
        self.hours_hand.setPen(pen)

        # second
        pen = QPen(self.style.midcolor)
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        self.seconds_hand.setPen(pen)

        # outer circle
        pen = QPen(self.style.foreground_color)
        pen.setWidth(6)
        self.circle.setPen(pen)

        # inner circle
        self.hand_circle.setBrush(QBrush(self.style.background_color))

        # minute lines
        pen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setColor(self.style.midcolor)
        pen.setWidth(4)

        bold_pen = QPen()
        bold_pen.setCapStyle(Qt.RoundCap)
        bold_pen.setColor(self.style.foreground_color)
        bold_pen.setWidth(6)

        for i, line in enumerate(self.lines):
            if i % 5 == 0:
                line.setPen(bold_pen)
            else:
                line.setPen(pen)

    def set_rect(self, rect):
        super().set_rect(rect)

        self.center_x = self.rect.left() + self.rect.width() / 2.0
        self.center_y = self.rect.top() + self.rect.height() / 2.0
        self.radius = min(self.rect.width(), self.rect.height()) / 2.0 - 3.0

        self.circle.setRect(self.center_x - self.radius,
                            self.center_y - self.radius,
                            2 * self.radius,
                            2 * self.radius)
        self.hand_circle.setRect(self.center_x - 5,
                                 self.center_y - 5,
                                 10, 10)

        for i, line in enumerate(self.lines):
            angle = i * 2.0 * math.pi / 60.0
            if i % 5 == 0:
                line.setLine(self.center_x + math.cos(angle) * self.radius * 0.85,
                             self.center_y + math.sin(angle) * self.radius * 0.85,
                             self.center_x + math.cos(angle) * self.radius * 0.95,
                             self.center_y + math.sin(angle) * self.radius * 0.95)
            else:
                line.setLine(self.center_x + math.cos(angle) * self.radius * 0.90,
                             self.center_y + math.sin(angle) * self.radius * 0.90,
                             self.center_x + math.cos(angle) * self.radius * 0.95,
                             self.center_y + math.sin(angle) * self.radius * 0.95)

        self.set_time(self.now)

    def set_time(self, now):
        self.now = now

        hour = (self.now.hour / 12.0 + self.now.minute / 60.0 / 12.0) * 2.0 * math.pi - math.pi / 2.0
        minute = (self.now.minute / 60.0 + self.now.second / 60.0 / 60.0) * 2.0 * math.pi - math.pi / 2.0
        second = (self.now.second / 60.0) * 2.0 * math.pi - math.pi / 2.0

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
