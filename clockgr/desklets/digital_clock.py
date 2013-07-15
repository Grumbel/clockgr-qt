import cairo

from ..desklet import *

class DigitalClock(Desklet):
    def __init__(self):
        self.font        = "DejaVu Sans"
        self.font_slant  = cairo.FONT_SLANT_NORMAL
        self.font_weight = cairo.FONT_WEIGHT_NORMAL
        self.color = (0, 0, 0)

    def draw(self, cr, now):
        date    = now.strftime("%A, %d. %B %Y")
        time    = now.strftime("%H:%M")
        seconds = now.strftime("%S")

        cr.select_font_face(self.font, self.font_slant, self.font_weight)
        cr.set_source_rgb(*self.color)

        cr.set_font_size(192 * 0.75)
        cr.move_to(32, 770)
        cr.show_text(time)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192 * 0.6)
        cr.move_to(32 + width + 32, 770)
        cr.show_text(seconds)

        cr.set_font_size(56)
        cr.move_to(32, 840)
        cr.show_text(date)

# EOF #
