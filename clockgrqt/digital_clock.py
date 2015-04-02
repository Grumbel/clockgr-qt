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


from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from .desklet import Desklet


class DigitalClock(Desklet):

    def __init__(self):
        super().__init__()

        self.seconds = QGraphicsSimpleTextItem(self.root)
        self.time = QGraphicsSimpleTextItem(self.root)
        self.date = QGraphicsSimpleTextItem(self.root)

    def set_style(self, style):
        super().set_style(style)

        self.seconds.setBrush(style.foreground_color)
        self.time.setBrush(style.foreground_color)
        self.date.setBrush(style.foreground_color)

        font = QFont(style.font)
        font.setPixelSize(192 * 0.6)
        self.seconds.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(192 * 0.75)
        self.time.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(56)
        self.date.setFont(font)

    def set_rect(self, rect):
        super().set_rect(rect)

        # FIXME: set_rect can't layout properly without style, neither
        # can style without a rect

        time_fm = QFontMetrics(self.time.font())
        seconds_fm = QFontMetrics(self.seconds.font())

        x = self.rect.left()
        y = self.rect.top()

        self.time.setPos(x, y)
        self.seconds.setPos(x + time_fm.width("00:00") + 20,
                            y + time_fm.ascent() - seconds_fm.ascent())
        self.date.setPos(x, y + time_fm.ascent())

    def update(self, now):
        date = now.strftime("%A, %d. %B %Y")
        time = now.strftime("%H:%M")
        seconds = now.strftime("%S")

        self.time.setText(time)
        self.seconds.setText(seconds)
        self.date.setText(date)


# EOF #
