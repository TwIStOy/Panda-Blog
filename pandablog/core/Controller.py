# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import Loader
import Selector
import Renderer
import Config
import Util as util


class Controller(object):
    def __init__(self, root):
        global_config = Config.Config(util.get_path(root, 'config.json'))
        self.loader = Loader.Loader(util.get_path(root, 'src'), global_config)
        self.selector = Selector.Selector(root)
        self.renderer = Renderer.Renderer(root, global_config)

    def run(self):
        resource = self.loader.run()
        for_render = self.selector.run(resource)
        self.renderer.run(resource, for_render)

