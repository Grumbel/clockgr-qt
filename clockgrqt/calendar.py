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


from datetime import datetime, timedelta
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QFont, QFontMetrics
from PyQt5.QtWidgets import (QGraphicsRectItem, QGraphicsLineItem,
                             QGraphicsSimpleTextItem)
from .desklet import Desklet


class CalendarDesklet(Desklet):

    def __init__(self):
        super().__init__()

        self.calendar_offset = 0
        self.weekdays = []
        self.days = []  # [(daytime, widget), ...]

        self.header = None
        self.header_line = None

        self.cursor = None

        self.cursor_pos = None
        self.build_scene(datetime.now())

    def build_scene(self, now):
        year = now.year
        month = now.month
        month += self.calendar_offset

        while month < 1:
            year -= 1
            month += 12

        while month > 12:
            year += 1
            month -= 12

        # Print calendar
        start = datetime(year, month, 1)
        start = start - timedelta(start.weekday())
        today = start

        # cursor
        self.cursor = QGraphicsRectItem(self.root)

        # header
        self.header = QGraphicsSimpleTextItem(self.root)

        # weekdays
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            text = QGraphicsSimpleTextItem(self.root)
            text.setText(day)
            self.weekdays.append(text)

        # line
        self.header_line = QGraphicsLineItem(self.root)

        for y in range(0, 6):
            for x in range(0, 7):
                widget = QGraphicsSimpleTextItem("%d" % today.day, self.root)
                self.days.append((today, widget))
                today = today + timedelta(days=1)

    def set_rect(self, rect):
        super().set_rect(rect)

        self.cell_width = (self.rect.width()) / 7.0
        self.cell_height = (self.rect.height() - 64) / 7.0

        x = rect.left()
        y = rect.top()

        fm = QFontMetrics(self.header.font())
        rect = fm.boundingRect(self.header.text())
        self.header.setPos(x + self.rect.width() / 2 - rect.width() / 2,
                           y)

        y += fm.height()

        for row, day in enumerate(self.weekdays):
            fm = QFontMetrics(day.font())
            rect = fm.boundingRect(day.text())
            day.setPos(x + row * self.cell_width + self.cell_width / 2 - rect.width() / 2,
                       y)

        y += fm.height()
        self.header_line.setLine(x, y,
                                 x + self.rect.width() - 3, y)

        for n, (day, widget) in enumerate(self.days):
            col = n % 7
            row = n // 7

            rect = fm.boundingRect(widget.text())
            widget.setPos(x + col * self.cell_width + self.cell_width / 2 - rect.width() / 2,
                          y + row * self.cell_height + self.cell_height / 2 - fm.height() / 2)

        # FIXME: mark current day
        if self.cursor_pos is not None:
            self.cursor.setRect(x + self.cursor_pos[0] * self.cell_width,
                                y + self.cursor_pos[1] * self.cell_height,
                                self.cell_width,
                                self.cell_height)
            self.cursor.show()
        else:
            self.cursor.hide()

    def set_style(self, style):
        super().set_style(style)

        font = QFont(style.font)
        font.setPixelSize(48)
        self.header.setBrush(style.midcolor)
        self.header.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(32)

        self.header_line.setPen(style.foreground_color)

        self.cursor.setBrush(style.foreground_color)
        self.cursor.setPen(QPen(Qt.NoPen))

        for widget in self.weekdays:
            widget.setBrush(style.foreground_color)

        for n, (day, widget) in enumerate(self.days):
            col = n % 7
            row = n // 7
            widget.setFont(font)
            if (col, row) == self.cursor_pos:
                widget.setBrush(style.background_color)
            elif day.month != self.now.month:  # FIXME: doesn't take offset into account
                widget.setBrush(style.midcolor)
            else:
                widget.setBrush(style.foreground_color)

        for widget in self.weekdays:
            widget.setFont(font)

    def next_month(self):
        self.calendar_offset += 1
        self.update(datetime.now())

    def previous_month(self):
        self.calendar_offset -= 1
        self.update(datetime.now())

    def update(self, now):
        self.now = now

        year = now.year
        month = now.month
        month += self.calendar_offset

        while month < 1:
            year -= 1
            month += 12

        while month > 12:
            year += 1
            month -= 12

        # update header
        s = datetime(year, month, 1).strftime("%B %Y")

        self.header.setText(s)

        # Print calendar
        start = datetime(year, month, 1)
        start = start - timedelta(start.weekday())
        today = start

        self.cursor_pos = None

        # update days
        for n, (day, widget) in enumerate(self.days):
            col = n % 7
            row = n // 7

            if day.day == now.day and day.month == now.month and self.calendar_offset == 0:
                self.cursor_pos = (col, row)

            widget.setText("%d" % today.day)
            self.days[n] = (today, widget)
            today = today + timedelta(days=1)

        self.set_style(self.style)
        self.set_rect(self.rect)


# EOF #
