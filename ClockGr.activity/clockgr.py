from gi.repository import GLib
from gi.repository import Gtk

from sugar3.activity import activity


class ClockGrActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

	button = Gtk.Button("Button")
	self.set_canvas(button)
