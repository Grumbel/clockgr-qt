import cairo

from ..desklet import *

class WorldDesklet(Desklet):
    def __init__(self):
        super(WorldDesklet, self).__init__()

        self.world = cairo.ImageSurface.create_from_png("world.png")

    def draw(self, cr):
        cr.set_source_surface(self.world, self.x, self.y)
        cr.paint_with_alpha(0.125)

# EOF #
