import cairo
from datetime import datetime, timedelta

from ..desklet import *

class CalenderDesklet(Desklet):
    def __init__(self):
        self.calendar_offset = 0
        self.font        = "DejaVu Sans"
        self.font_slant  = cairo.FONT_SLANT_NORMAL
        self.font_weight = cairo.FONT_WEIGHT_NORMAL

        self.background_color = (.75,.75,.75)
        self.midcolor = (0.5, 0.5, 0.5)
        self.foreground_color = (0,0,0)

    def next_month(self):
        self.calendar_offset += 1
        self.queue_draw()

    def previous_month(self):
        self.calendar_offset -= 1
        self.queue_draw()

    def draw(self, cr, now, x_pos, y_pos):
        cr.select_font_face(self.font, self.font_slant, self.font_weight)

        cell_width  = 75
        cell_height = 60

        year  = now.year
        month = now.month
        month += self.calendar_offset

        while month < 1:
            year  -= 1
            month += 12

        while month > 12:
            year  += 1
            month -= 12

        start = datetime(year, month, 1)
        start = start - timedelta(start.weekday())
        today = start

        cr.set_source_rgb(0.75,0.75,0.75)
        cr.set_font_size(48)
        s = datetime(year, month, 1).strftime("%B %Y")
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)
        cr.move_to(x_pos + 232 - width/2, y_pos - 16)
        cr.show_text(s)

        cr.set_source_rgb(*self.foreground_color)
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

        cr.select_font_face(self.font,
                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        for y in range(0,6):
            for x in range(0,7):
                s = "%d" % today.day
                                
                if today.month != month:
                    cr.set_source_rgb(0.75, 0.75, 0.75)
                else:
                    if today.day == now.day and today.month == now.month and self.calendar_offset == 0:
                        # cr.set_source_rgb(*self.foreground_color)
                        cr.set_source_rgb(*self.foreground_color)
                        cr.rectangle(x_pos + x * cell_width - cell_width/2, 
                                     y_pos + 32 + cell_height + y * cell_height - cell_height/2 - 10, 
                                     cell_width, cell_height)
                        cr.fill()
                        cr.set_source_rgb(*self.background_color)
                        # cr.set_source_rgb(*self.foreground_color)
                        cr.select_font_face(self.font,
                                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    else:
                        cr.select_font_face(self.font,
                                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                        cr.set_source_rgb(*self.foreground_color)

                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)

                cr.move_to(x_pos + x * cell_width - width/2, 
                           y_pos + 32 + cell_height + y * cell_height)
                # now.day, now.month
                # now.weekday()
                cr.show_text(s)
                today = today + timedelta(days=1)

# EOF #
