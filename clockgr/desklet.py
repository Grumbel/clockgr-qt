import gtk.gdk

from style import *

class Desklet(object):
    def __init__(self):
        self.parent = None
        
        self.x = 0
        self.y = 0
        self.width  = 0
        self.height = 0

        self.style = Style()
        
    def set_parent(self, parent):
        self.parent = parent

    def set_style(self, style):
        self.style = style

    def set_rect(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height

    def draw(self, cr, now):
        cr.save()
        cr.translate(self.x, self.y)
        self.on_draw(cr, now)
        cr.restore()

        # cr.set_source_rgba(1.0, 1.0, 0, 0.5)
        # cr.rectangle(self.x, self.y, self.width, self.height)
        # cr.fill()

    def queue_draw(self):
        self.parent.queue_draw_area(self.x, self.y, self.width, self.height)

# EOF #
