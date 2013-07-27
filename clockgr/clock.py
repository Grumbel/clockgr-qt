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

class ClockWidget(gtk.DrawingArea):
    def __init__(self, renderer):
        gtk.DrawingArea.__init__(self)
        self.renderer = renderer
        self.renderer.set_parent(self)
        self.connect("expose-event", self.do_expose_event)

    def do_expose_event(self, widget, event):
        if self.window:
            cr = self.window.cairo_create()

            # Restrict Cairo to the exposed area; avoid extra work
            if event:
                cr.rectangle(event.area.x, event.area.y,
                             event.area.width, event.area.height)
                cr.clip()

            self.renderer.draw(cr, 1680, 1050)

class ClockMode:
    calendar  = 1
    stopwatch = 2

class ClockRenderer(object):
    def __init__(self):
        self.parent = None
        self.my_style = Style()
        self.desklets = []
        self.active_desklets = []

        self.digital_clock = self.add_desklet(DigitalClock(),    (32, 670, 640, 200))
        self.analog_clock  = self.add_desklet(AnalogClock(),     (900-256, 32, 512, 512))
        self.calendar      = self.add_desklet(CalendarDesklet(), (32, 32, 512, 412))
        self.world         = self.add_desklet(WorldDesklet(),    (1200 - 540 - 32, 900 - 276 - 32, 540, 276))
        self.stopwatch    = self.add_desklet(StopWatch(),       (32, 64, 500, 180))
        
        self.mode = ClockMode.calendar
        self.apply_mode()


    def next_mode(self):
        print self.mode

        if self.mode == ClockMode.calendar:
            self.mode = ClockMode.stopwatch
        else:
            self.mode = ClockMode.calendar

        self.apply_mode()
        self.queue_draw()

    def apply_mode(self):
        if self.mode == ClockMode.calendar:
            self.active_desklets = [d for d in self.desklets if d != self.stopwatch]
        elif self.mode == ClockMode.stopwatch:
            self.active_desklets = [d for d in self.desklets if d != self.calendar]

    def add_desklet(self, desklet, rect):
        desklet.set_parent(self)
        desklet.set_style(self.my_style)
        desklet.set_rect(*rect)
        self.desklets.append(desklet)
        return desklet

    def set_parent(self, parent):
        self.parent = parent

    def queue_draw_area(self, x, y, width, height):
        if self.parent: 
            self.parent.queue_draw_area(x, y, width, height)

    def queue_draw(self):
        if self.parent: 
            self.parent.queue_draw()
        else:
            root = gtk.gdk.get_default_root_window()
            rect = root.get_frame_extents()
            root.invalidate_rect(rect, False)
            cr = root.cairo_create()
            self.draw(cr, rect.width, rect.height)

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(*self.my_style.background_color)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        now = datetime.now()

        for desklet in self.active_desklets:
            desklet.draw(cr, now)

    def update(self):
        self.queue_draw()
        return True

    def invert(self):
        self.my_style.background_color, self.my_style.foreground_color = self.my_style.foreground_color, self.my_style.background_color
        self.queue_draw()

def realize_cb(widget):
    print "realize_cb"
    pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
    color = gtk.gdk.Color()
    cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
    widget.window.set_cursor(cursor)

def main(argv):
    import argparse
    
    parser = argparse.ArgumentParser(description='ClockGr - A toy clock application')
    parser.add_argument('--root-window', action='store_true', help='Display the clock on the root window')
    args = parser.parse_args()
    
    use_root_window = args.root_window

    if use_root_window:
        renderer = ClockRenderer()
        renderer.invert()
        gobject.timeout_add (1000, renderer.update)
    else:
        renderer = ClockRenderer()
        widget = ClockWidget(renderer)
        window = gtk.Window()
        window.set_title("ClockGr")
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
                                 lambda *args: renderer.stopwatch.start_stop_watch())
        key, modifier = gtk.accelerator_parse('Return')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 lambda *args: renderer.stopwatch.clear_stop_watch())

        key, modifier = gtk.accelerator_parse('1')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 lambda *args: renderer.calendar.previous_month())
        key, modifier = gtk.accelerator_parse('2')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 lambda *args: renderer.calendar.next_month())

        key, modifier = gtk.accelerator_parse('i')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 lambda *args: renderer.invert())

        key, modifier = gtk.accelerator_parse('m')
        accelgroup.connect_group(key,
                                 modifier,
                                 gtk.ACCEL_VISIBLE,
                                 lambda *args: renderer.next_mode())

        window.add_accel_group(accelgroup)

        window.set_size_request(1200,900)
        window.connect("delete-event", gtk.main_quit)
        window.connect("realize", realize_cb)

        gobject.timeout_add (1000, renderer.update)
    
    gtk.main()

# EOF #
