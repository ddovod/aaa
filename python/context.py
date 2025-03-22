

class Context:
    _data = None
    _config = None
    _gui = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance

    def set_data(self, data):
        self._data = data

    def set_config(self, config):
        self._config = config

    def set_gui(self, gui):
        self._gui = gui

    def data(self):
        return self._data

    def config(self):
        return self._config

    def gui(self):
        return self._gui
