import cairo
import math

from ..desklet import *

class AnalogClock(Desklet):
    def __init__(self):
        self.background_color = (.75,.75,.75)
        self.midcolor = (0.5, 0.5, 0.5)
        self.foreground_color = (0,0,0)

    def draw(self, cr, now, x, y, width, height):
        cr.set_source_rgb(*self.foreground_color)
        cr.new_path()
        cr.set_line_width(6.0)
        cr.arc(x, y, width, 0, 2 * math.pi)
        cr.stroke()

        cr.set_source_rgb(*self.midcolor)
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

        cr.set_source_rgb(*self.foreground_color)
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
        cr.set_source_rgb(*self.foreground_color)
        cr.new_path()
        cr.set_line_width(16.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(hour)*width*0.0,
                   y + math.sin(hour)*width*0.0)
        cr.line_to(x + math.cos(hour)*width*0.45,
                   y + math.sin(hour)*width*0.45)
        cr.stroke()

        # minute
        cr.set_source_rgb(*self.foreground_color)
        cr.new_path()
        cr.set_line_width(12.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(minute)*width*0.0,
                   y + math.sin(minute)*width*0.0)
        cr.line_to(x + math.cos(minute)*width*0.8,
                   y + math.sin(minute)*width*0.8)
        cr.stroke()

        # second
        cr.set_source_rgb(*self.midcolor)
        cr.new_path()
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + math.cos(second)*width*0.0,
                   y + math.sin(second)*width*0.0)
        cr.line_to(x + math.cos(second)*width*0.8,
                   y + math.sin(second)*width*0.8)
        cr.stroke()

        cr.set_source_rgb(*self.background_color)
        cr.new_path()
        cr.arc(x,y,4, 0, 2.0*math.pi)
        cr.fill()

# EOF #
