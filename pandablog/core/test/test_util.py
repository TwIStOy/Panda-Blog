__author__ = 'TwIstOy'

"""
    For test module <Util> in <core>.
"""


import unittest
from pandablog.core import Util
import os
import shutil
import json
import codecs


class UtilTest(unittest.TestCase):

    def setUp(self):
        with codecs.open("c:\\panda.test", "w", encoding='utf-8') as fp:
            fp.write("### h1\n```python\ncode_part```\n*a* **b**\nsafe_latex!\(a_i_1\)\[a_i_1\]")
        if os.path.isdir("c:\\panda_test"):
            shutil.rmtree("c:\\panda_test")

    def tearDown(self):
        if os.path.isdir("c:\\panda_test"):
            shutil.rmtree("c:\\panda_test")
        files = ['"c:\\panda.test"', 'c:\\panda.json.test', 'c:\\panda.json.test2']
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

    def test_get_path(self):
        self.assertEqual(Util.get_path('c:/', 'twistoy', ['la', 'la'], "info.json"),
                         'c:/twistoy\\la\\la\\info.json')
        self.assertEqual(Util.get_path(['c:\\', 'twistoy', ['la', 'la']], 'info.json'),
                         'c:\\twistoy\\la\\la\\info.json')

    def test_create_dir(self):
        path = 'c:\\panda_test\\lalala'
        Util.create_dir(path)
        self.assertTrue(os.path.isdir(path))
        self.assertEqual(Util.create_dir(path), None)
        os.rmdir(path)
        with codecs.open(path, "w") as fp:
            fp.write("lalala")
        with self.assertRaises(OSError):
            Util.create_dir(path)

    def test_mk_transfer(self):
        with codecs.open("c:\\panda.test", "r", encoding='utf-8') as fp:
            rv = Util.mk_transfer(fp)
        ans = ['<h3>h1</h3>',
               '<code class="python syntax-highlight">',
               'code_part',
               '</code>',
               '<em>a</em>',
               '<strong>b</strong>',
               'safe_latex!\(a_i_1\)\[a_i_1\]']
        for line in ans:
            self.assertIn(line, rv)

    def test_get_json(self):
        # test for load a file which exists
        with codecs.open('c:\\panda.json.test', "w", encoding='utf-8') as fp:
            test = {"a": "b"}
            json.dump(test, fp)
        read_ans = Util.get_json("c:\\panda.json.test")
        self.assertDictEqual(test, read_ans)

        # test for load a file which does not exist
        test_empty = {}
        read_ans = Util.get_json("c:\\panda.json.test2")
        self.assertDictEqual(test_empty, read_ans)


if __name__ == '__main__':
    unittest.main()