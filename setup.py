# clockgr - A fullscreen clock for Qt
# Copyright (C) 2015-2018 Ingo Ruhnke <grumbel@gmail.com>
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


from distutils.core import setup


setup(
    name="clockgr",
    version="0.1.0",
    description="A fullscreen clock for Qt",
    author="Ingo Ruhnke",
    author_email="grumbel@gmail.com",
    url="https://github.com/Grumbel/clockgr",
    packages=["clockgr_qt", "clockgr_gtk"],
    scripts=["bin/clockgr-gtk"],
    entry_points={
        'console_scripts': [],
        'gui_scripts': [
            'clockgr-qt = clockgr_qt.main:main_entrypoint',
        ]
    },
    long_description=("clockgr is a simple fullscreen clock for"
                      "Gtk+, it includes a calendar, a stopwatch "
                      "and both digital and analog displays."),
    requires=["PyQt5", "pygtk", "gtk", "gobject"]
)


# EOF #
