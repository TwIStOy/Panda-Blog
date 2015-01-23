__author__ = 'TwIStOy'
"""
    For test the module <Post> in <core>
"""

import unittest
from pandablog.core import Post
import codecs
import json
import os
from pandablog.core import Config
import datetime


class TestPost(unittest.TestCase):
    def test_all(self):
        global_config = Config.Config('c:\\config.json').load()
        post = Post.Post("c:\\panda.test", global_config)
        self.assertEqual(post.meta_info.tags, ['a', 'b', 'c'])
        self.assertEqual(post.meta_info.author, 'test')
        self.assertEqual(post.meta_info.category, 'test')
        self.assertEqual(post.meta_info.title, 'title_test')
        self.assertEqual(post.meta_info.datetime,
                         datetime.datetime.strptime('1000-1-1', "%Y-%m-%d"))
        self.assertEqual(post.url, None)
        urls = []
        post.get_url(urls)
        self.assertEqual(post.url, 'title_test')
        self.assertEqual(post.content, None)
        post.generate_html_content()
        self.assertTrue("<h1>a</h1>" in post.content)
        self.assertTrue("<h2>aa</h2>" in post.content)

    def setUp(self):
        context = [
            'tags: a, b, c',
            'category: test',
            'author: test',
            'title: title_test',
            'datetime: 1000-1-1',
            "",
            "# a",
            "## aa"
        ]
        config_info = {
            "default_author": "TwIStOy",
            "default_category": "test",
            "default_title": "hello world",
            "default_datetime": "2012-12-12"
        }
        with codecs.open("c:\\panda.test", 'w', 'utf-8') as fp:
            tmp = "\n".join(context)
            fp.write(tmp)
        with codecs.open("c:\\config.json", "w", "utf-8") as fp:
            json.dump(config_info, fp)

    def tearDown(self):
        if os.path.isfile("c:\\config.json"):
            os.remove("c:\\config.json")


if __name__ == '__main__':
    unittest.main()
