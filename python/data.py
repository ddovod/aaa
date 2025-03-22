

class LotData:
    def __init__(self, lot_json):
        self._time_left_xpath = lot_json.get('time_left_xpath', '')
        self._best_bid_xpath = lot_json.get('best_bid_xpath', '')
        self._my_bid_xpath = lot_json.get('my_bid_xpath', '')
        self._open_bid_btn_xpath = lot_json.get('open_bid_btn_xpath', '')
        self._seconds_left_min = lot_json.get('seconds_left_min', 60)

    def to_json(self):
        return {
            'time_left_xpath': self._time_left_xpath,
            'best_bid_xpath': self._best_bid_xpath,
            'my_bid_xpath': self._my_bid_xpath,
            'open_bid_btn_xpath': self._open_bid_btn_xpath,
            'seconds_left_min': self._seconds_left_min
        }

    @property
    def time_left_xpath(self):
        return self._time_left_xpath

    @time_left_xpath.setter
    def time_left_xpath(self, value):
        self._time_left_xpath = value

    @property
    def best_bid_xpath(self):
        return self._best_bid_xpath

    @best_bid_xpath.setter
    def best_bid_xpath(self, value):
        self._best_bid_xpath = value

    @property
    def my_bid_xpath(self):
        return self._my_bid_xpath

    @my_bid_xpath.setter
    def my_bid_xpath(self, value):
        self._my_bid_xpath = value

    @property
    def open_bid_btn_xpath(self):
        return self._open_bid_btn_xpath

    @open_bid_btn_xpath.setter
    def open_bid_btn_xpath(self, value):
        self._open_bid_btn_xpath = value

    @property
    def seconds_left_min(self):
        return self._seconds_left_min

    @seconds_left_min.setter
    def seconds_left_min(self, value):
        self._seconds_left_min = value


class Data:
    def __init__(self, data_json):
        self._trade_url = data_json.get('trade_url', '')
        self._close_bid_btn_xpath = data_json.get('close_bid_btn_xpath', '')
        self._close_bid_error_btn_xpath = data_json.get('close_bid_error_btn_xpath', '')
        self._seconds_refresh = data_json.get('seconds_refresh', 120)
        self._lots = []
        for lot_json in data_json.get('lots', []):
            self._lots.append(LotData(lot_json))

    def to_json(self):
        result = {
            'trade_url': self._trade_url,
            'close_bid_btn_xpath': self._close_bid_btn_xpath,
            'close_bid_error_btn_xpath': self._close_bid_error_btn_xpath,
            'seconds_refresh': self._seconds_refresh,
            'lots': []
        }
        for lot in self._lots:
            result['lots'].append(lot.to_json())
        return result

    @property
    def trade_url(self):
        return self._trade_url

    @trade_url.setter
    def trade_url(self, value):
        self._trade_url = value

    @property
    def close_bid_btn_xpath(self):
        return self._close_bid_btn_xpath

    @close_bid_btn_xpath.setter
    def close_bid_btn_xpath(self, value):
        self._close_bid_btn_xpath = value

    @property
    def close_bid_error_btn_xpath(self):
        return self._close_bid_error_btn_xpath

    @close_bid_error_btn_xpath.setter
    def close_bid_error_btn_xpath(self, value):
        self._close_bid_error_btn_xpath = value

    @property
    def seconds_refresh(self):
        return self._seconds_refresh

    @seconds_refresh.setter
    def seconds_refresh(self, value):
        self._seconds_refresh = value

    @property
    def lots(self):
        return self._lots

    @lots.setter
    def lots(self, value):
        self._lots = value

    def add_new_lot(self):
        self._lots.append(LotData({}))
