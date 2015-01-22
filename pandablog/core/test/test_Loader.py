__author__ = 'TwIStOy'

import unittest
from pandablog.core import Loader
from pandablog.core import Util
import codecs


# TODO: complete it!
class LoaderTest(unittest.TestCase):

    def setUp(self):
        load_root_path = "c:\\panda\\src"
        Util.create_dir(load_root_path)
        Util.create_dir(Util.get_path(load_root_path, 'post'))
        Util.create_dir(Util.get_path(load_root_path, 'page'))
        Util.create_dir(Util.get_path(load_root_path, 'theme', 'default'))

        with codecs.open() as fp:
            pass
        pass

    def tearDown(self):
        pass

    pass
