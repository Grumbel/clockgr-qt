#! /usr/bin/env python
##
##  clockgr - A fullscreen clock for Gtk+
##  Copyright (C) 2012 Ingo Ruhnke <grumbel@gmail.com>
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
import math
from datetime import datetime, timedelta
pygtk.require('2.0')
import gtk, gobject, cairo

from .desklets.digital_clock import *
from .desklets.analog_clock import *
from .desklets.world import *
from .desklets.calendar import *
from .desklets.stop_watch import *

background_color = (1, 1, 1)
midcolor = (0.5, 0.5, 0.5)
foreground_color = (0,0,0)

system_font = "DejaVu Sans"
# system_font = "DejaVu Serif"
# system_font = "Inconsolata"
# system_font = "Arial"
# system_font = "Segoe UI"
system_font = "Calibri"
# system_font = "Corbel"
# system_font = "Candara"

class ClockWidget(gtk.DrawingArea):
    def __init__(self, *args):
        gtk.DrawingArea.__init__(self, *args)
        
        self.digital_clock = DigitalClock()
        self.analog_clock = AnalogClock()
        self.calendar = CalendarDesklet()
        self.world = World()
        self.stop_watch_desklet = StopWatch()

        self.stop_watch = False
        self.stop_watch_start_time  = None
        self.stop_watch_stop_time  = None

    # Handle the expose-event by drawing
    def do_expose_event(self, event):
        if self.window:
            cr = self.window.cairo_create()
            # cr = gtk.gdk.get_default_root_window().cairo_create()

            # Restrict Cairo to the exposed area; avoid extra work
            if event:
                cr.rectangle(event.area.x, event.area.y,
                             event.area.width, event.area.height)
                cr.clip()

            self.draw(cr, 1680, 1050)

    def queue_draw(self):
        self.do_expose_event(None)

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(*background_color)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        now = datetime.now()

        self.digital_clock.draw(cr, now)
        self.analog_clock.draw(cr, now, 900, 300, 256, 256)
        self.world.draw(cr)

        if self.stop_watch_start_time:
            self.stop_watch_desklet.draw(cr, now)
        else:
            self.calendar.draw(cr, now, 80, 100)
        
    def start_stop_watch(self):
        if self.stop_watch:
            self.update_fast()
            self.stop_watch = False            
            self.stop_watch_stop_time = datetime.now()
        else:
            self.stop_watch = True
            if not self.stop_watch_stop_time:
                self.stop_watch_start_time = datetime.now()
            else:
                self.stop_watch_start_time = datetime.now() - (self.stop_watch_stop_time - self.stop_watch_start_time)
                self.stop_watch_stop_time  = None
            gobject.timeout_add(31, self.update_fast)
            self.queue_draw()

    def clear_stop_watch(self):
        self.queue_draw()
        self.stop_watch = False
        self.stop_watch_start_time = None
        self.stop_watch_stop_time  = None
        self.calendar_offset = 0

    def update(self):
        if not self.stop_watch:
            self.queue_draw()
        return True

    def update_fast(self):
        self.queue_draw_area(0, 0, 500, 180)
        if self.stop_watch:
            return True
        else:
            return False

    def invert(self):
        global foreground_color, background_color
        foreground_color, background_color = background_color, foreground_color
        self.queue_draw()

def realize_cb(widget):
    pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
    color = gtk.gdk.Color()
    cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
    widget.window.set_cursor(cursor)

def main(args):
    window = gtk.Window()
    widget = ClockWidget()
    widget.show()
    window.add(widget)
    window.present()

    window.set_size_request(1200,900)

    accelgroup = gtk.AccelGroup()
    key, modifier = gtk.accelerator_parse('Escape')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             gtk.main_quit)
    key, modifier = gtk.accelerator_parse('f')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: window.fullscreen())
    key, modifier = gtk.accelerator_parse('space')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: widget.start_stop_watch())
    key, modifier = gtk.accelerator_parse('Return')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: widget.clear_stop_watch())

    key, modifier = gtk.accelerator_parse('1')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: widget.calendar.previous_month())
    key, modifier = gtk.accelerator_parse('2')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: widget.calendar.next_month())

    key, modifier = gtk.accelerator_parse('i')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             lambda *args: widget.invert())

    window.add_accel_group(accelgroup)

    window.set_size_request(1200,900)
    window.connect("delete-event", gtk.main_quit)
    window.connect("realize", realize_cb)

    gobject.timeout_add (1000, widget.update)
    
    gtk.main()

# EOF #
