
from data import BrowserWindowGeometry


class ReportBrowserWindowGeometry:
    def __init__(self, pos_x, pos_y, size_x, size_y):
        self._geom = BrowserWindowGeometry({})
        self._geom.pos_x = pos_x
        self._geom.pos_y = pos_y
        self._geom.size_x = size_x
        self._geom.size_y = size_y

    @property
    def browser_window_geometry(self):
        return self._geom
