import gobject
from datetime import datetime, timedelta

from ..desklet import Desklet


class Timer(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.stop_time = None

    def is_running(self):
        return self.start_time is not None and self.stop_time is None

    def get_time(self):
        if self.start_time:
            if self.stop_time:
                return self.stop_time - self.start_time
            else:
                return datetime.now() - self.start_time
        else:
            return timedelta(0)

    def start(self):
        if self.stop_time is None:
            self.start_time = datetime.now()
        else:
            self.start_time = datetime.now() - (self.stop_time - self.start_time)
            self.stop_time = None

    def stop(self):
        if self.stop_time is None:
            self.stop_time = datetime.now()

    def start_stop(self):
        if self.is_running():
            self.stop()
        else:
            self.start()


class StopWatch(Desklet):

    def __init__(self):
        super(StopWatch, self).__init__()
        self.timer = Timer()
        self.timeout_handle = None

    def on_timeout(self):
        self.queue_draw()
        return True

    def is_running(self):
        return self.timer.is_running()

    def start_stop_watch(self):
        self.timer.start_stop()

        if self.timer.is_running():
            if not self.timeout_handle:
                self.timeout_handle = gobject.timeout_add(31, self.on_timeout)
        else:
            if self.timeout_handle:
                gobject.source_remove(self.timeout_handle)
                self.timeout_handle = None

        self.queue_draw()

    def clear_stop_watch(self):
        self.timer.reset()
        self.queue_draw()

    def on_draw(self, cr, now):
        t = self.timer.get_time()

        time = "%02d:%02d" % (t.seconds / (60 * 60), (t.seconds % (60 * 60)) / 60)
        seconds = "%02d'%02d" % (t.seconds % 60, t.microseconds / 10000)

        cr.select_font_face(self.style.font, self.style.font_slant, self.style.font_weight)

        cr.set_source_rgb(*self.style.foreground_color)

        cr.set_font_size(24)
        cr.move_to(0, 0)
        cr.show_text("Stopwatch:")

        cr.set_font_size(192 / 2)
        cr.move_to(0, 0 + 86)
        cr.show_text(time)

        xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(time)

        cr.set_font_size(192 / 2 * 0.6)
        cr.move_to(0 + width + 16, 0 + 86)
        cr.show_text(seconds)

# EOF #
