from clockgr_gtk.desklet import Desklet


class DigitalClock(Desklet):

    def __init__(self):
        super(DigitalClock, self).__init__()

    def on_draw(self, cr, now):
        date = now.strftime("%A, %d. %B %Y")
        time = now.strftime("%H:%M")
        seconds = now.strftime("%S")

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)
        cr.set_source_rgb(*self.style.foreground_color)

        cr.set_font_size(192 * 0.75)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        pos_x = 0
        pos_y = 0

        pos_y += height

        cr.move_to(pos_x, pos_y)
        cr.show_text(time)

        cr.set_font_size(192 * 0.6)
        cr.move_to(pos_x + width + 32, pos_y)
        cr.show_text(seconds)

        pos_y += yadvance
        cr.set_font_size(56)
        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(date)
        pos_y += height

        cr.move_to(pos_x, pos_y)
        cr.show_text(date)

# EOF #
