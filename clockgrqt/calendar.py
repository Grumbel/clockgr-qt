import math
from datetime import datetime, timedelta
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont, QFontMetrics
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import (QGraphicsScene, QMainWindow, QWidget,
                             QVBoxLayout, QGraphicsView, QApplication,
                             QGraphicsItemGroup, QGraphicsRectItem,
                             QGraphicsEllipseItem, QGraphicsLineItem,
                             QGraphicsSimpleTextItem)


class CalendarDesklet:

    def __init__(self):
        super().__init__()
        self.calendar_offset = 0
        self.width = 512
        self.height = 512
        self.build_scene()

    def get_item(self):
        return self.group

    def next_month(self):
        self.calendar_offset += 1
        self.update(datetime.now())

    def previous_month(self):
        self.calendar_offset -= 1
        self.update(datetime.now())

    def update(self, now):
        year = now.year
        month = now.month
        month += self.calendar_offset

        pos_x = 0
        pos_y = 0

        # update header
        s = datetime(year, month, 1).strftime("%B %Y")

        fm = QFontMetrics(self.header_text.font())
        rect = fm.boundingRect(s)
        self.header_text.setPos(pos_x + self.width / 2 - rect.width() / 2, pos_y)
        self.header_text.setText(s)

        # update days

    def build_scene(self):
        self.group = QGraphicsItemGroup()

        # cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

        pos_x = 0
        pos_y = 0

        self.cell_width = (self.width) / 7.0
        self.cell_height = (self.height - 64) / 7.0

        now = datetime.now()
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

        self._draw_header()
        self._draw_weekdays(pos_x, pos_y + 64)
        self._draw_days(pos_x, pos_y + 66, year, month, today, now)

    def _draw_header(self):
        # Print "July 2013" header
        brush = QBrush(QColor.fromRgbF(0.75, 0.75, 0.75))
        font = QFont("Arial", 48, -1, False)

        self.header_text = QGraphicsSimpleTextItem(self.group)
        self.header_text.setFont(font)

    def _draw_weekdays(self, pos_x, pos_y):
        # cr.set_source_rgb(*self.style.foreground_color)
        brush = QBrush(QColor.fromRgbF(0.75, 0.75, 0.75))
        font = QFont("Arial", 26, -1, False)
        fm = QFontMetrics(font)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for x, day in enumerate(days):
            # xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(days[x])
            text = QGraphicsSimpleTextItem(self.group)
            rect = fm.boundingRect(day)
            text.setPos(pos_x + x * self.cell_width - rect.width() / 2 + self.cell_width / 2.0,
                        pos_y + 32 + 0 * self.cell_height)
            text.setFont(font)
            text.setText(day)

        line = QGraphicsLineItem(self.group)
        line.setLine(pos_x + 3, pos_y + fm.height() * 2,
                     pos_x + self.width - 3, pos_y + fm.height() * 2)

        # cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

    def _draw_days(self, pos_x, pos_y, year, month, today, now):
        brush = QBrush(QColor.fromRgbF(0.75, 0.75, 0.75))
        font = QFont("Arial", 32, -1, False)

        for y in range(0, 6):
            for x in range(0, 7):
                s = "%d" % today.day

                if today.month != month:
                    brush = QBrush(QColor.fromRgbF(0.75, 0.75, 0.75))
                else:
                    if today.day == now.day and today.month == now.month and self.calendar_offset == 0:
                        # cr.set_source_rgb(*self.style.foreground_color)
                        brush = QBrush(QColor.fromRgbF(1, 1, 1))

                        rect = QGraphicsRectItem(pos_x + x * self.cell_width - self.cell_width / 2 + self.cell_width / 2.0,
                                                 pos_y + 32 + self.cell_height + y * self.cell_height - self.cell_height / 2 - 10,
                                                 self.cell_width, self.cell_height,
                                                 self.group)
                        # cr.fill()
                        # cr.set_source_rgb(*self.style.background_color)
                        brush = QBrush(QColor.fromRgbF(0, 0, 0))
                        # cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                    else:
                        # cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                        # cr.set_source_rgb(*self.style.foreground_color)
                        brush = QBrush(QColor.fromRgbF(0, 0, 0))

                fm = QFontMetrics(font)
                width = fm.width(s)
                heigth = fm.height()

                text = QGraphicsSimpleTextItem(self.group)
                text.setPos(pos_x + x * self.cell_width - width / 2 + self.cell_width / 2.0,
                            pos_y + 32 + self.cell_height + y * self.cell_height)
                text.setText(s)
                text.setBrush(brush)
                text.setFont(font)
                today = today + timedelta(days=1)


# EOF #
