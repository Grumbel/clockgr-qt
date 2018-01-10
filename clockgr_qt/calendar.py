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


from datetime import timedelta, date
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QFont, QFontMetrics
from PyQt5.QtWidgets import (QGraphicsRectItem, QGraphicsLineItem,
                             QGraphicsSimpleTextItem)
from .desklet import Desklet


class CalendarModel:

    def __init__(self, year=None, month=None, today=None):

        if today is None:
            self.today = date.today()
        else:
            self.today = today

        if year is None:
            self.year = self.today.year
        else:
            self.year = year

        if month is None:
            self.month = self.today.month
        else:
            self.month = month

    def update(self, now):
        self.today = now.date()

    def next_month(self):
        self.month += 1

        while self.month > 12:
            self.year += 1
            self.month -= 12

    def previous_month(self):
        self.month -= 1

        while self.month < 1:
            self.year -= 1
            self.month += 12


class CalendarDesklet(Desklet):

    def __init__(self):
        super().__init__()

        self.model = CalendarModel()

        self.cursor_pos = None

        self.cursor = QGraphicsRectItem(self.root)
        self.header = QGraphicsSimpleTextItem(self.root)

        self.weekdays = []
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            self.weekdays.append(QGraphicsSimpleTextItem(day, self.root))

        self.header_line = QGraphicsLineItem(self.root)

        self.days = []
        for _ in range(0, 6 * 7):
            self.days.append(QGraphicsSimpleTextItem(self.root))

    def next_month(self):
        self.model.next_month()
        self.layout()

    def previous_month(self):
        self.model.previous_month()
        self.layout()

    def set_rect(self, rect):
        super().set_rect(rect)
        self.layout()

    def set_style(self, style):
        super().set_style(style)

        font = QFont(style.font)
        font.setPixelSize(48)
        self.header.setBrush(style.midcolor)
        self.header.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(32)

        self.header_line.setPen(style.foreground_color)

        self.cursor.setBrush(style.midcolor)
        self.cursor.setPen(QPen(Qt.NoPen))

        for widget in self.weekdays:
            widget.setFont(font)
            widget.setBrush(style.foreground_color)

        for widget in self.days:
            widget.setFont(font)
            widget.setBrush(self.style.foreground_color)

        self.layout()

    def layout(self):
        cell_width = (self.rect.width()) / 7.0
        cell_height = (self.rect.height() - 64) / 7.0

        x = self.rect.left()
        y = self.rect.top()

        fm = QFontMetrics(self.header.font())
        rect = fm.boundingRect(self.header.text())
        self.header.setPos(x + self.rect.width() / 2 - rect.width() / 2,
                           y)

        y += fm.height()

        for row, day in enumerate(self.weekdays):
            fm = QFontMetrics(day.font())
            rect = fm.boundingRect(day.text())
            day.setPos(x + row * cell_width + cell_width / 2 - rect.width() / 2,
                       y)

        y += fm.height()
        self.header_line.setLine(x, y,
                                 x + self.rect.width() - 3, y)

        y += 8

        for n, widget in enumerate(self.days):
            col = n % 7
            row = n // 7

            rect = fm.boundingRect(widget.text())
            widget.setPos(x + col * cell_width + cell_width / 2 - rect.width() / 2,
                          y + row * cell_height + cell_height / 2 - fm.height() / 2)

            # if day.month != self.now.month:
            #    widget.setBrush(self.style.midcolor)
            # else:

        if self.cursor_pos is not None:
            self.cursor.setRect(x + self.cursor_pos[0] * cell_width,
                                y + self.cursor_pos[1] * cell_height,
                                cell_width,
                                cell_height)
            self.cursor.show()
        else:
            self.cursor.hide()

    def update(self, now):
        self.model.update(now)

        # update header
        self.header.setText(
            date(self.model.year, self.model.month, 1).strftime("%B %Y"))

        # calculate the date of the top/left calendar entry
        current_date = date(self.model.year, self.model.month, 1)
        current_date = current_date - timedelta(current_date.weekday())

        self.cursor_pos = None
        for n, widget in enumerate(self.days):
            col = n % 7
            row = n // 7

            if current_date == self.model.today:
                self.cursor_pos = (col, row)

            widget.setText("%d" % current_date.day)
            self.days[n] = widget
            current_date += timedelta(days=1)

        self.layout()


# EOF #
