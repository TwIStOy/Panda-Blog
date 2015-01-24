# -*- coding:utf-8 -*-
__author__ = "TwIStOy FanChing"
"""Load configuration from root path"""

import json
import codecs
import os


class ConfigError(Exception):
    pass


def load_config_json(file_name):
    if os.path.isfile(file_name):
        with codecs.open(file_name, "r", encoding='utf-8') as fp:
            global_config = json.load(fp)
    else:
        raise OSError('No "{}" file! Please check and retry.'.format(file_name))
    return global_config


class ConfigBase(object):
    """
        config class base
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        return self

    def get(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise AttributeError('No attribute <{attr}> in class <{name}>'.format(
                attr=attr, name=self.__class__.__name__
            ))


class ConfigFromJson(ConfigBase):
    def load(self):
        config = load_config_json(self.file_name)
        for item in config:
            if hasattr(self, item):
                raise ConfigError("Illegal attribute <{attr}> in class <{name}>".format(
                    attr=item, name=self.__class__.__name__
                ))
            setattr(self, item, config.get(item))
        return self

Config = ConfigFromJson