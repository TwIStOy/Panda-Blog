# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import Loader
import Processor
import Generator
import Config
import Util


class Core(object):
    def __init__(self, root):
        global_config = Config.Config(Util.get_path(root, 'config.json')).load()
        self.loader = Loader.Loader(Util.get_path(root, 'src'), global_config)
        self.processor = Processor.Processor(root, global_config)
        self.generator = Generator.Generator(root, global_config)

    def run(self):
        resources = self.loader.run()
        self.processor.run(resources)
        self.generator.run(resources)

