import cairo
from datetime import datetime, timedelta

from ..desklet import *

class CalendarDesklet(Desklet):
    def __init__(self):
        super(CalendarDesklet, self).__init__()

        self.calendar_offset = 0

    def next_month(self):
        self.calendar_offset += 1
        self.queue_draw()

    def previous_month(self):
        self.calendar_offset -= 1
        self.queue_draw()

    def draw(self, cr, now):
        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

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
        cr.move_to(self.x + 232 - width/2, self.y - 16)
        cr.show_text(s)

        cr.set_source_rgb(*self.style.foreground_color)
        cr.set_font_size(32)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for x in range(0,7):
                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(days[x])
                cr.move_to(self.x + x * cell_width - width/2, 
                           self.y + 32 + 0 * cell_height)
                cr.show_text(days[x])
            
        cr.move_to(self.x - cell_width/2,   self.y + height*2)
        cr.line_to(self.x + cell_width * 6.5, self.y + height*2)
        cr.stroke()

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

        for y in range(0,6):
            for x in range(0,7):
                s = "%d" % today.day
                                
                if today.month != month:
                    cr.set_source_rgb(0.75, 0.75, 0.75)
                else:
                    if today.day == now.day and today.month == now.month and self.calendar_offset == 0:
                        # cr.set_source_rgb(*self.style.foreground_color)
                        cr.set_source_rgb(*self.style.foreground_color)
                        cr.rectangle(self.x + x * cell_width - cell_width/2, 
                                     self.y + 32 + cell_height + y * cell_height - cell_height/2 - 10, 
                                     cell_width, cell_height)
                        cr.fill()
                        cr.set_source_rgb(*self.style.background_color)
                        # cr.set_source_rgb(*self.style.foreground_color)
                        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                    else:
                        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                        cr.set_source_rgb(*self.style.foreground_color)

                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)

                cr.move_to(self.x + x * cell_width - width/2, 
                           self.y + 32 + cell_height + y * cell_height)
                # now.day, now.month
                # now.weekday()
                cr.show_text(s)
                today = today + timedelta(days=1)

# EOF #
