__all__ = ['app_config']

import os

try: import ConfigParser as configparser
except ImportError: import configparser

from .base_utils import try_int

class AppConfig(configparser.RawConfigParser):
    config_filename = 'app.ini'
    main_section = 'main'
    def __init__(self, *args, **kw):
        configparser.RawConfigParser.__init__(self, *args, **kw)
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.read(os.path.join(self.base_dir, self.config_filename))
        self.log_level = self.opt_string(self.main_section, 'log-level', 'info').strip().upper()
        self.is_debug = self.log_level == 'DEBUG'
        self.base_url = self.opt_string(self.main_section, 'base-url', 'http://localhost:8080')
        self.secret = self.opt_string(self.main_section, 'secret', '1234')

    def opt_string(self, section, key, fallback=None):
        return self.get(section, key) if self.has_option(section, key) else fallback

    def opt_int(self, section, key, fallback=0):
        return try_int(self.opt_string(section, key, str(fallback)), fallback)

app_config = AppConfig()
