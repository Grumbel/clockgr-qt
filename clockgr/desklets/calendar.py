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

    def on_draw(self, cr, now):
        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

        pos_x = 0
        pos_y = 0

        self.cell_width  = (self.width) / 7.0
        self.cell_height = (self.height - 64) / 7.0

        year  = now.year
        month = now.month
        month += self.calendar_offset

        while month < 1:
            year  -= 1
            month += 12

        while month > 12:
            year  += 1
            month -= 12
        
        # Print calendar
        start = datetime(year, month, 1)
        start = start - timedelta(start.weekday())
        today = start

        self._draw_header(cr, pos_x, pos_y, year, month)
        self._draw_weekdays(cr, pos_x, pos_y + 64)
        self._draw_days(cr, pos_x, pos_y + 66, year, month, today, now)

        # TODO: get calendar width, calculate pos_x when calendar is centered

    def _draw_header(self, cr, pos_x, pos_y, year, month):
        # Print "July 2013" header
        cr.set_source_rgb(0.75,0.75,0.75)
        cr.set_font_size(48)
        s = datetime(year, month, 1).strftime("%B %Y")
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)
        pos_y += height
        cr.move_to(pos_x + self.width/2 - width/2, pos_y)
        cr.show_text(s)
        pos_y += 16

    def _draw_weekdays(self, cr, pos_x, pos_y):
        cr.set_source_rgb(*self.style.foreground_color)
        cr.set_font_size(32)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for x, day in enumerate(days):
                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(days[x])
                cr.move_to(pos_x + x * self.cell_width - width/2 + self.cell_width/2.0,
                           pos_y + 32 + 0 * self.cell_height)
                cr.show_text(day)
            
        cr.move_to(pos_x + 3, pos_y + height*2)
        cr.line_to(pos_x + self.width - 3, pos_y + height*2)
        cr.stroke()

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

    def _draw_days(self, cr, pos_x, pos_y, year, month, today, now):
        for y in range(0,6):
            for x in range(0,7):
                s = "%d" % today.day
                                
                if today.month != month:
                    cr.set_source_rgb(0.75, 0.75, 0.75)
                else:
                    if today.day == now.day and today.month == now.month and self.calendar_offset == 0:
                        # cr.set_source_rgb(*self.style.foreground_color)
                        cr.set_source_rgb(*self.style.foreground_color)
                        cr.rectangle(pos_x + x * self.cell_width - self.cell_width/2 + self.cell_width/2.0,
                                     pos_y + 32 + self.cell_height + y * self.cell_height - self.cell_height/2 - 10, 
                                     self.cell_width, self.cell_height)
                        cr.fill()
                        cr.set_source_rgb(*self.style.background_color)
                        # cr.set_source_rgb(*self.style.foreground_color)
                        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                    else:
                        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
                        cr.set_source_rgb(*self.style.foreground_color)

                xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(s)

                cr.move_to(pos_x + x * self.cell_width - width/2 + self.cell_width/2.0, 
                           pos_y + 32 + self.cell_height + y * self.cell_height)
                # now.day, now.month
                # now.weekday()
                cr.show_text(s)
                today = today + timedelta(days=1)

# EOF #
