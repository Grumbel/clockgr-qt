import cairo
import math

from ..desklet import *

class AnalogClock(Desklet):
    def __init__(self):
        super(AnalogClock, self).__init__()

    def draw(self, cr, now):
        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(6.0)
        cr.arc(self.x, self.y, self.width, 0, 2 * math.pi)
        cr.stroke()

        cr.set_source_rgb(*self.style.midcolor)
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0,60):
            angle = i*2.0*math.pi/60.0
            cr.move_to(self.x + math.cos(angle)*self.width*0.90,
                       self.y + math.sin(angle)*self.width*0.90)
            cr.line_to(self.x + math.cos(angle)*self.width*0.95,
                       self.y + math.sin(angle)*self.width*0.95)
        cr.stroke()

        cr.set_source_rgb(*self.style.foreground_color)
        cr.set_line_width(6.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0,12):
            angle = i*2.0*math.pi/12.0
            cr.move_to(self.x + math.cos(angle)*self.width*0.85,
                       self.y + math.sin(angle)*self.width*0.85)
            cr.line_to(self.x + math.cos(angle)*self.width*0.95,
                       self.y + math.sin(angle)*self.width*0.95)
        cr.stroke()

        hour   = (now.hour   / 12.0 + now.minute / 60.0 / 12.0) * 2.0 * math.pi - math.pi/2.0
        minute = (now.minute / 60.0 + now.second / 60.0 / 60.0) * 2.0 * math.pi - math.pi/2.0
        second = (now.second / 60.0) * 2.0 * math.pi - math.pi/2.0

        # hour
        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(16.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(self.x + math.cos(hour)*self.width*0.0,
                   self.y + math.sin(hour)*self.width*0.0)
        cr.line_to(self.x + math.cos(hour)*self.width*0.45,
                   self.y + math.sin(hour)*self.width*0.45)
        cr.stroke()

        # minute
        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(12.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(self.x + math.cos(minute)*self.width*0.0,
                   self.y + math.sin(minute)*self.width*0.0)
        cr.line_to(self.x + math.cos(minute)*self.width*0.8,
                   self.y + math.sin(minute)*self.width*0.8)
        cr.stroke()

        # second
        cr.set_source_rgb(*self.style.midcolor)
        cr.new_path()
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(self.x + math.cos(second)*self.width*0.0,
                   self.y + math.sin(second)*self.width*0.0)
        cr.line_to(self.x + math.cos(second)*self.width*0.8,
                   self.y + math.sin(second)*self.width*0.8)
        cr.stroke()

        cr.set_source_rgb(*self.style.background_color)
        cr.new_path()
        cr.arc(self.x, self.y, 4, 0, 2.0*math.pi)
        cr.fill()

# EOF #
