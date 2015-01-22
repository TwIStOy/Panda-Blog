# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import Loader
import Selector
import Renderer
import Util as util
import os
import json
import codecs


class Controller(object):
    def __init__(self, root):
        if os.path.isfile(util.get_path(root, 'config.json')):
            with codecs.open(util.get_path(root, 'config.json'), "r", encoding='utf-8') as fp:
                global_config = json.load(fp)
        else:
            raise OSError('No "config.json" file! Please check and retry.')
        self.global_config = global_config
        self.loader = Loader.Loader(util.get_path(root, 'src'), global_config)
        self.selector = Selector.Selector(root)
        self.renderer = Renderer.Renderer(root, global_config)

    def run(self):
        resource = self.loader.run()
        for_render = self.selector.run(resource)
        self.renderer.run(resource, for_render)

