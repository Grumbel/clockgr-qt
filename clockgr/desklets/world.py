import cairo

from ..desklet import *

class WorldDesklet(Desklet):
    def __init__(self):
        super(WorldDesklet, self).__init__()

        self.world = cairo.ImageSurface.create_from_png("world.png")

    def on_draw(self, cr, now):
        cr.set_source_surface(self.world, 
                              self.width/2.0 - self.world.get_width()/2.0,
                              self.height/2.0 - self.world.get_height()/2.0)
        cr.paint_with_alpha(0.125)

# EOF #
