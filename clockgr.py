#! /usr/bin/env python
import pygtk
import math
from datetime import datetime, timedelta
pygtk.require('2.0')
import gtk, gobject, cairo

background_color = (0,0,0)
foreground_color = (1,1,1)

foreground_color = (0,0,0)
background_color = (1,1,1)

system_font = "DejaVu Sans"
# system_font = "DejaVu Serif"
# system_font = "Inconsolata"
# system_font = "Arial"
# system_font = "Segoe UI"
system_font = "Calibri"
# system_font = "Corbel"
# system_font = "Candara"

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):
    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    def __init__(self, *args):
        gtk.DrawingArea.__init__(self, *args)
        
        self.stop_watch = False
        self.stop_watch_start_time  = None
        self.stop_watch_stop_time  = None

        self.world = cairo.ImageSurface.create_from_png("world.png")

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
        cr.set_source_rgb(*background_color)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        now = datetime.now()
        weekday = now.strftime("%A, %d. %B %Y")
        time    = now.strftime("%H:%M")
        seconds = now.strftime("%S")       

        cr.select_font_face(system_font,
                cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        cr.set_source_rgb(*foreground_color)

        cr.set_font_size(192)
        cr.move_to(32, 770)
        cr.show_text(time)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192 * 0.6)
        cr.move_to(32 + width + 32, 770)
        cr.show_text(seconds)

        cr.set_font_size(56)
        cr.move_to(32, 840)
        cr.show_text(weekday)

        self.draw_analog(cr, now, 900, 300, 256, 256)

        if self.stop_watch_start_time:
            if self.stop_watch_stop_time:
                t = self.stop_watch_stop_time - self.stop_watch_start_time
            else:
                t = now - self.stop_watch_start_time

            time    = "%02d:%02d" % (t.seconds/60, t.seconds%60)
            seconds = "%02d" % (t.microseconds/10000)

            cr.select_font_face(system_font,
                    cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

            cr.set_source_rgb(*foreground_color)

            cr.set_font_size(24)
            cr.move_to(32, 64)
            cr.show_text("Stopwatch:")

            cr.set_font_size(192/2)
            cr.move_to(32, 150)
            cr.show_text(time)

            cr.set_font_size(192/4)
            cr.move_to(315, 150)
            cr.show_text(seconds)
        else:
            self.draw_calender(cr, now, 80, 100)
            
        
        cr.set_source_surface(self.world, 
                              1200 - self.world.get_width()  - 16, 
                              900  - self.world.get_height() - 32)
        cr.paint_with_alpha(0.125)

    def draw_calender(self, cr, now, x_pos, y_pos):
        cr.select_font_face(system_font,
                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        cell_width  = 75
        cell_height = 60

        cr.set_source_rgb(0.75,0.75,0.75)
        cr.set_font_size(48)
        s = now.strftime("%B %Y")
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)
        cr.move_to(x_pos + 232 - width/2, y_pos - 16)
        cr.show_text(s)

        cr.set_source_rgb(*foreground_color)
        cr.set_font_size(32)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for x in range(0,7):
                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(days[x])
                cr.move_to(x_pos + x * cell_width - width/2, 
                           y_pos + 32 + 0 * cell_height)
                cr.show_text(days[x])
            
        cr.move_to(x_pos - cell_width/2,   y_pos + height*2)
        cr.line_to(x_pos + cell_width * 6.5, y_pos + height*2)
        cr.stroke()

        start = datetime(now.year, now.month, 1)
        start = start - timedelta(start.weekday())
        today = start

        cr.select_font_face(system_font,
                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        for y in range(0,6):
            for x in range(0,7):
                s = "%d" % today.day
                                
                if today.month != now.month:
                    cr.set_source_rgb(0.75, 0.75, 0.75)
                else:
                    if today.day == now.day and today.month == now.month:
                        # cr.set_source_rgb(*foreground_color)
                        cr.set_source_rgb(0.9, 0.9, 0.9)
                        cr.rectangle(x_pos + x * cell_width - cell_width/2, 
                                     y_pos + 32 + cell_height + y * cell_height - cell_height/2 - 10, 
                                     cell_width, cell_height)
                        cr.fill()
                        # cr.set_source_rgb(*background_color)
                        cr.set_source_rgb(*foreground_color)
                        cr.select_font_face(system_font,
                                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    else:
                        cr.select_font_face(system_font,
                                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                        cr.set_source_rgb(*foreground_color)

                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)

                cr.move_to(x_pos + x * cell_width - width/2, 
                           y_pos + 32 + cell_height + y * cell_height)
                # now.day, now.month
                # now.weekday()
                cr.show_text(s)
                today = today + timedelta(days=1)

    def draw_analog(self, cr, now, x, y, width, height):
        cr.set_source_rgb(*foreground_color)
        cr.new_path()
        cr.set_line_width(6.0)
        cr.arc(x, y, width, 0, 2 * math.pi)
        cr.stroke()

        cr.set_source_rgb(0.5,0.5,0.5)
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0,60):
            angle = i*2.0*math.pi/60.0
            cr.move_to(x + math.cos(angle)*width*0.90,
                       y + math.sin(angle)*width*0.90)
            cr.line_to(x + math.cos(angle)*width*0.95,
                       y + math.sin(angle)*width*0.95)
        cr.stroke()

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(6.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0,12):
            angle = i*2.0*math.pi/12.0
            cr.move_to(x + math.cos(angle)*width*0.85,
                       y + math.sin(angle)*width*0.85)
            cr.line_to(x + math.cos(angle)*width*0.95,
                       y + math.sin(angle)*width*0.95)
        cr.stroke()

        hour   = (now.hour   / 12.0 + now.minute / 60.0 / 12.0) * 2.0 * math.pi - math.pi/2.0
        minute = (now.minute / 60.0 + now.second / 60.0 / 60.0) * 2.0 * math.pi - math.pi/2.0
        second = (now.second / 60.0) * 2.0 * math.pi - math.pi/2.0

        # hour
        cr.set_source_rgb(*foreground_color)
        cr.new_path()
        cr.set_line_width(14.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(hour)*width*0.0,
                   y + math.sin(hour)*width*0.0)
        cr.line_to(x + math.cos(hour)*width*0.45,
                   y + math.sin(hour)*width*0.45)
        cr.stroke()

        # minute
        cr.set_source_rgb(*foreground_color)
        cr.new_path()
        cr.set_line_width(14.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(minute)*width*0.0,
                   y + math.sin(minute)*width*0.0)
        cr.line_to(x + math.cos(minute)*width*0.8,
                   y + math.sin(minute)*width*0.8)
        cr.stroke()

        # second
        cr.set_source_rgb(0.5,0.5,0.5)
        cr.new_path()
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(second)*width*0.0,
                   y + math.sin(second)*width*0.0)
        cr.line_to(x + math.cos(second)*width*0.8,
                   y + math.sin(second)*width*0.8)
        cr.stroke()

        cr.set_source_rgb(*background_color)
        cr.new_path()
        cr.arc(x,y,4, 0, 2.0*math.pi)
        cr.fill()

    def update(self):
        self.queue_draw()
        return True

    def update_fast(self):
        self.queue_draw_area(0,0,400,180)
        if self.stop_watch:
            return True
        else:
            return False

    def start_stop_watch(self):
        if self.stop_watch:
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

        self.queue_draw_area(0,0,400,180)

    def clear_stop_watch(self):
        self.queue_draw()
        self.stop_watch = False
        self.stop_watch_start_time = None
        self.stop_watch_stop_time  = None

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
    window.add_accel_group(accelgroup)

    window.set_size_request(1200,900)
    window.connect("delete-event", gtk.main_quit)
    window.connect("realize", realize_cb)

    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    #window.fullscreen()
    gobject.timeout_add (1000, widget.update)

    gtk.main()

if __name__ == "__main__":
    run(Screen)

# EOF #
