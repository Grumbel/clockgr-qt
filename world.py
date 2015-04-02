class World:
    def __init__(self):
        pass

    def draw_world(self, cr):
        cr.set_source_surface(self.world,
                              1680 - self.world.get_width()  - 16,
                              1050 - self.world.get_height() - 32)
        cr.paint_with_alpha(0.125)

# EOF #
