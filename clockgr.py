#! /usr/bin/env python
import pygtk
import math
from datetime import datetime
pygtk.require('2.0')
import gtk, gobject, cairo

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()
        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        now = datetime.now()
        weekday = now.strftime("%A, %d. %B %Y")
        time    = now.strftime("%H:%M")
        seconds = now.strftime("%S")
        

        cr.select_font_face("DejaVu Sans",
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        cr.set_source_rgb(1,1,1)

        cr.set_font_size(192)
        cr.move_to(32, 750)
        cr.show_text(time)

        cr.set_font_size(192/2)
        cr.move_to(600, 750)
        cr.show_text(seconds)

        cr.set_font_size(64)
        cr.move_to(32, 840)
        cr.show_text(weekday)

        self.draw_analog(cr, now, 900, 300, 256, 256)

    def draw_analog(self, cr, now, x, y, width, height):
        cr.set_source_rgb(1,1,1)
        cr.new_path()
        cr.set_line_width(6.0)
        cr.arc(x, y, width, 0, 2 * math.pi)
        cr.stroke()

        hour   = (now.hour   / 12.0) * 2.0 * math.pi - math.pi/2.0
        minute = (now.minute / 60.0) * 2.0 * math.pi - math.pi/2.0
        second = (now.second / 60.0) * 2.0 * math.pi - math.pi/2.0

        # second
        cr.set_source_rgb(0.5,0.5,0.5)
        cr.new_path()
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x,y)
        cr.line_to(x + math.cos(second)*width*0.9,
                   y + math.sin(second)*width*0.9)
        cr.stroke()

        # minute
        cr.set_source_rgb(0.75,0.75,0.75)
        cr.new_path()
        cr.set_line_width(12.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x,y)
        cr.line_to(x + math.cos(minute)*width*0.9,
                   y + math.sin(minute)*width*0.9)
        cr.stroke()

        # hour
        cr.set_source_rgb(1,1,1)
        cr.new_path()
        cr.set_line_width(12.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x,y)
        cr.line_to(x + math.cos(hour)*width*0.45,
                   y + math.sin(hour)*width*0.45)
        cr.stroke()

    def update(self):
        self.queue_draw()
        return True

def realize_cb(widget):
    pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
    color = gtk.gdk.Color()
    cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
    widget.window.set_cursor(cursor)

# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget):
    window = gtk.Window()

    accelgroup = gtk.AccelGroup()
    key, modifier = gtk.accelerator_parse('Escape')
    accelgroup.connect_group(key,
                             modifier,
                             gtk.ACCEL_VISIBLE,
                             gtk.main_quit)
    window.add_accel_group(accelgroup)

    window.set_size_request(1200,900)
    window.connect("delete-event", gtk.main_quit)
    window.connect("realize", realize_cb)

    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    window.fullscreen()
    gobject.timeout_add (1000, widget.update)

    gtk.main()

if __name__ == "__main__":
    run(Screen)

# EOF #
