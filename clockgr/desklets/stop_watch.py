from ..desklet import *

class StopWatch(Desklet):
    def __init__(self):
        pass
        
    def start_stop_watch(self):
        if self.stop_watch:
            self.update_fast()
            self.stop_watch = False            
            self.stop_watch_stop_time = datetime.now()
        else:
            self.stop_watch = True
            if not self.stop_watch_stop_time:
                self.stop_watch_start_time = datetime.now()
            else:
                self.stop_watch_start_time = datetime.now() - (self.stop_watch_stop_time - self.stop_watch_start_time)
                self.stop_watch_stop_time  = None
            gobject.timeout_add(31, self.update_fast)
            self.queue_draw()

    def clear_stop_watch(self):
        self.queue_draw()
        self.stop_watch = False
        self.stop_watch_start_time = None
        self.stop_watch_stop_time  = None
        self.calendar_offset = 0

    def draw(self, cr, now):
        if self.stop_watch_stop_time:
            t = self.stop_watch_stop_time - self.stop_watch_start_time
        else:
            t = now - self.stop_watch_start_time

        time    = "%02d:%02d" % (t.seconds/(60*60), (t.seconds%(60*60))/60)
        seconds = "%02d'%02d" % (t.seconds%60, t.microseconds/10000)

        cr.select_font_face(system_font,
                            cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        cr.set_source_rgb(*foreground_color)

        cr.set_font_size(24)
        cr.move_to(32, 64)
        cr.show_text("Stopwatch:")

        cr.set_font_size(192/2)
        cr.move_to(32, 150)
        cr.show_text(time)

        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192/2 * 0.6)
        cr.move_to(32 + width + 16, 150)
        cr.show_text(seconds)        

# EOF #
