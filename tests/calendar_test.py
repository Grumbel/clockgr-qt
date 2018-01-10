# ClockGr test cases
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


import unittest

from clockgr_qt.calendar import CalendarModel


class CalendarTestCase(unittest.TestCase):

    def test_calendar(self):
        model = CalendarModel(year=1980, month=11)

        model.next_month()
        model.next_month()
        self.assertEqual(model.month, 1)
        self.assertEqual(model.year, 1981)

        model.previous_month()
        self.assertEqual(model.month, 12)
        self.assertEqual(model.year, 1980)


# EOF #
