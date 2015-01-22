__author__ = 'TwIStOy'
"""
    For test the module <Post> in <core>
"""

import unittest
from pandablog.core import Post
import codecs


class TestPost(unittest.TestCase):

    def setUp(self):
        context = {
            'tags: a, b, c',
            'category: test',
            'author: test',
            'title: title_test',
            'datetime: 1000-1-1',
            "",
            "# a",
            "## aa"
        }
        with codecs.open("c:\\panda.test", 'r', 'utf-8') as fp:
            fp.write("\n".join(context))

    def tearDown(self):
        pass


    pass


if __name__ == '__main__':
    unittest.main()
