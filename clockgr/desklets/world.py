import cairo

from ..desklet import *

class World(Desklet):
    def __init__(self):
        self.world = cairo.ImageSurface.create_from_png("world.png")

    def draw(self, cr):
        cr.set_source_surface(self.world, 
                              1200 - self.world.get_width()  - 16,
                              900 - self.world.get_height() - 32)
        cr.paint_with_alpha(0.125)

# EOF #
