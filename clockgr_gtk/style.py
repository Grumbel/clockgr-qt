import cairo


class Style:

    def __init__(self):
        self.font = "DejaVu Sans"
        self.font_slant = cairo.FONT_SLANT_NORMAL
        self.font_weight = cairo.FONT_WEIGHT_NORMAL

        self.background_color = (1.0, 1.0, 1.0)
        self.midcolor = (0.5, 0.5, 0.5)
        self.foreground_color = (0, 0, 0)

# EOF #
