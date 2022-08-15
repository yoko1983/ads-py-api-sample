
import json
from logging import config


class AppSettingsUtil():

    def __init__(self):
        setting_file=open('settings_app.json', 'r')
        self.settings_data = json.load(setting_file)


class LoggerSettingsUtil():

    def __init__(self):
        setting_file=open('settings_logger.json', 'r')
        self.settings_data = json.load(setting_file)
        config.dictConfig(self.settings_data)

_settings_app_util = AppSettingsUtil()

_settings_logger_util = LoggerSettingsUtil()


def get_settings_app_data():
    return _settings_app_util.settings_data

def get_settings_logger_data():
    return _settings_logger_util.settings_data