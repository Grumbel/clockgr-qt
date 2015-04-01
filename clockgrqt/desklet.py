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


from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import (QGraphicsItemGroup, QGraphicsRectItem)

from .style import Style

class Desklet(object):

    def __init__(self):
        self.rect = QRectF()
        self.style = Style()
        self.root = QGraphicsItemGroup()

        self.debug_rect = QGraphicsRectItem(self.root)
        self.debug_rect.setPen(QPen(QColor(255, 0, 0)))

    def set_style(self, style):
        self.style = style

    def set_rect(self, rect):
        self.rect = rect
        if self.debug_rect:
            self.debug_rect.setRect(rect)

# EOF #
