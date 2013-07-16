import cairo
import gobject
from datetime import datetime, timedelta

from ..desklet import *

class StopWatch(Desklet):
    def __init__(self):
        super(StopWatch, self).__init__()

        self.stop_watch = False
        self.stop_watch_start_time = None
        self.stop_watch_stop_time  = None
        
    def is_running(self):
        if self.stop_watch_start_time:
            return True
        else:
            return False

    def update(self):
        self.queue_draw()
        return self.stop_watch

    def start_stop_watch(self):
        if self.stop_watch:
            self.stop_watch = False            
            self.stop_watch_stop_time = datetime.now()
        else:
            self.stop_watch = True
            if not self.stop_watch_stop_time:
                self.stop_watch_start_time = datetime.now()
            else:
                self.stop_watch_start_time = datetime.now() - (self.stop_watch_stop_time - self.stop_watch_start_time)
                self.stop_watch_stop_time  = None
            gobject.timeout_add(31, self.update)

    def clear_stop_watch(self):
        self.stop_watch = False
        self.stop_watch_start_time = None
        self.stop_watch_stop_time  = None
        self.queue_draw()

    def on_draw(self, cr, now):
        if self.stop_watch_stop_time:
            t = self.stop_watch_stop_time - self.stop_watch_start_time
        else:
            t = now - self.stop_watch_start_time

        time    = "%02d:%02d" % (t.seconds/(60*60), (t.seconds%(60*60))/60)
        seconds = "%02d'%02d" % (t.seconds%60, t.microseconds/10000)

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

        cr.set_source_rgb(*self.style.foreground_color)

        cr.set_font_size(24)
        cr.move_to(self.x, self.y)
        cr.show_text("Stopwatch:")

        cr.set_font_size(192/2)
        cr.move_to(self.x, self.y + 86)
        cr.show_text(time)

        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192/2 * 0.6)
        cr.move_to(self.x + width + 16, self.y + 86)
        cr.show_text(seconds)

# EOF #
