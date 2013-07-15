import cairo

from ..desklet import *

class DigitalClock(Desklet):
    def __init__(self):
        super(DigitalClock, self).__init__()

    def draw(self, cr, now):
        date    = now.strftime("%A, %d. %B %Y")
        time    = now.strftime("%H:%M")
        seconds = now.strftime("%S")

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
        cr.set_source_rgb(*self.style.foreground_color)

        cr.set_font_size(192 * 0.75)
        cr.move_to(self.x, self.y)
        cr.show_text(time)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192 * 0.6)
        cr.move_to(self.x + width + 32, self.y)
        cr.show_text(seconds)

        cr.set_font_size(56)
        cr.move_to(self.x, self.y + 70)
        cr.show_text(date)

# EOF #
