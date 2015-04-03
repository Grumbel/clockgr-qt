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
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from .desklet import Desklet


class Timer(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.stop_time = None

    def is_running(self):
        return self.start_time is not None and self.stop_time is None

    def get_time(self):
        if self.start_time:
            if self.stop_time:
                return self.stop_time - self.start_time
            else:
                return datetime.now() - self.start_time
        else:
            return timedelta(0)

    def start(self):
        if self.stop_time is None:
            self.start_time = datetime.now()
        else:
            self.start_time = datetime.now() - (self.stop_time - self.start_time)
            self.stop_time = None

    def stop(self):
        if self.stop_time is None:
            self.stop_time = datetime.now()

    def start_stop(self):
        if self.is_running():
            self.stop()
        else:
            self.start()


class StopWatch(Desklet):

    def __init__(self):
        super().__init__()

        self.timer = Timer()
        self.timeout_handle = None

        self.qtimer = QTimer()
        self.qtimer.timeout.connect(self.my_update)

        self.label = QGraphicsSimpleTextItem("Stopwatch:", self.root)
        self.time = QGraphicsSimpleTextItem("00:00", self.root)
        self.seconds = QGraphicsSimpleTextItem("00'00", self.root)

    def update(self):
        t = self.timer.get_time()
        time = "%02d:%02d" % (t.seconds / (60 * 60), (t.seconds % (60 * 60)) / 60)
        seconds = "%02d'%02d" % (t.seconds % 60, t.microseconds / 10000)

        self.time.setText(time)
        self.seconds.setText(seconds)

    def set_style(self, style):
        super().set_style(style)

        font = QFont(style.font)
        font.setPixelSize(24)
        self.time.setFont(font)
        self.label.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(192 / 2)
        self.time.setFont(font)

        font = QFont(style.font)
        font.setPixelSize(192 / 2 * 0.6)
        self.seconds.setFont(font)

        self.label.setBrush(self.style.foreground_color)
        self.time.setBrush(self.style.foreground_color)
        self.seconds.setBrush(self.style.foreground_color)

        self.layout()

    def set_rect(self, rect):
        super().set_rect(rect)
        self.layout()

    def layout(self):
        x = self.rect.left()
        y = self.rect.top()

        fm = QFontMetrics(self.time.font())
        rect = fm.boundingRect("00:00")

        sfm = QFontMetrics(self.seconds.font())

        self.time.setPos(x, y + 20)
        self.seconds.setPos(x + 20 + rect.width(), y + 20 + fm.ascent() - sfm.ascent())

        self.label.setPos(x, y)

    def my_update(self, *args):
        self.update()

    def is_running(self):
        return self.timer.is_running()

    def start_stop_watch(self):
        self.timer.start_stop()

        if self.timer.is_running():
            self.qtimer.setInterval(31)
            self.qtimer.start()
        else:
            self.qtimer.stop()

    def clear_stop_watch(self):
        self.timer.reset()


# EOF #
