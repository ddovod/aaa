
import os
import json
from log import log
from data import Data


class Config:
    def __init__(self):
        self._config_path = 'config.json'

        config_json = {}
        if os.path.exists(self._config_path):
            with open(self._config_path, 'r') as f:
                config_str = f.read()
                try:
                    config_json = json.loads(config_str)
                except Exception as e:
                    log.error(traceback.format_exc())
                    log.error('Will create new config')

        if 'data' in config_json:
            self._data = Data(config_json['data'])
        else:
            self._data = Data({})

    def data(self):
        return self._data

    def save(self):
        config_json = {
            'data': self._data.to_json()
        }
        with open(self._config_path, 'w+') as f:
            json.dump(config_json, f, indent=2)
            
