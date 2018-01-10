import cairo
import math

from clockgr_gtk.desklet import Desklet


class AnalogClock(Desklet):

    def __init__(self):
        super(AnalogClock, self).__init__()

    def on_draw(self, cr, now):
        center_x = self.width / 2.0
        center_y = self.height / 2.0
        radius = min(self.width, self.height) / 2.0 - 3.0

        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(6.0)
        cr.arc(center_x, center_y, radius, 0, 2 * math.pi)
        cr.stroke()

        cr.set_source_rgb(*self.style.midcolor)
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0, 60):
            angle = i * 2.0 * math.pi / 60.0
            cr.move_to(center_x + math.cos(angle) * radius * 0.90,
                       center_y + math.sin(angle) * radius * 0.90)
            cr.line_to(center_x + math.cos(angle) * radius * 0.95,
                       center_y + math.sin(angle) * radius * 0.95)
        cr.stroke()

        cr.set_source_rgb(*self.style.foreground_color)
        cr.set_line_width(6.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        for i in range(0, 12):
            angle = i * 2.0 * math.pi / 12.0
            cr.move_to(center_x + math.cos(angle) * radius * 0.85,
                       center_y + math.sin(angle) * radius * 0.85)
            cr.line_to(center_x + math.cos(angle) * radius * 0.95,
                       center_y + math.sin(angle) * radius * 0.95)
        cr.stroke()

        hour = (now.hour / 12.0 + now.minute / 60.0 / 12.0) * 2.0 * math.pi - math.pi / 2.0
        minute = (now.minute / 60.0 + now.second / 60.0 / 60.0) * 2.0 * math.pi - math.pi / 2.0
        second = (now.second / 60.0) * 2.0 * math.pi - math.pi / 2.0

        # hour
        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(16.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(center_x + math.cos(hour) * radius * 0.0,
                   center_y + math.sin(hour) * radius * 0.0)
        cr.line_to(center_x + math.cos(hour) * radius * 0.45,
                   center_y + math.sin(hour) * radius * 0.45)
        cr.stroke()

        # minute
        cr.set_source_rgb(*self.style.foreground_color)
        cr.new_path()
        cr.set_line_width(12.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(center_x + math.cos(minute) * radius * 0.0,
                   center_y + math.sin(minute) * radius * 0.0)
        cr.line_to(center_x + math.cos(minute) * radius * 0.8,
                   center_y + math.sin(minute) * radius * 0.8)
        cr.stroke()

        # second
        cr.set_source_rgb(*self.style.midcolor)
        cr.new_path()
        cr.set_line_width(4.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(center_x + math.cos(second) * radius * 0.0,
                   center_y + math.sin(second) * radius * 0.0)
        cr.line_to(center_x + math.cos(second) * radius * 0.8,
                   center_y + math.sin(second) * radius * 0.8)
        cr.stroke()

        cr.set_source_rgb(*self.style.background_color)
        cr.new_path()
        cr.arc(center_x, center_y, 4, 0, 2.0 * math.pi)
        cr.fill()

# EOF #
