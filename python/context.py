

class Context:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def gui(self):
        return self._gui

    @gui.setter
    def gui(self, gui):
        self._gui = gui

    @property
    def webdriver(self):
        return self._webdriver

    @webdriver.setter
    def webdriver(self, webdriver):
        self._webdriver = webdriver
