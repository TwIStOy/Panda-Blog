# -*- coding:utf-8 -*-
"""Load configuration from root path"""

import Util
import json
import codecs
import os


def load_config(root):
    if os.path.isfile(Util.get_path(root, 'config.json')):
        with codecs.open(Util.get_path(root, 'config.json'), "r", encoding='utf-8') as fp:
            global_config = json.load(fp)
    else:
        raise OSError('No "config.json" file! Please check and retry.')
    return global_config