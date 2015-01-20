__author__ = 'TwIStOy'

from .. import util
import os
import json


class Selector(object):

    def __init__(self, root, resource):
        # root: /panda/
        self.root = root
        self.resource = resource

    def only_md5_verify_post(self):
        """verify posts' md5, if equal, "make" will be False
        :return:
        """
        info = util.get_json(util.get_path(self.root, "src", "post", ".post_info"))
        new_post_info = dict()
        for p in self.resource['post']:
            if p.md5 == info.get(p.url):
                p.make = False
            new_post_info[p.url] = p.md5
        with open(util.get_path(self.root, "src", "post", ".post_info"), "w", "utf-8") as fp:
            json.dump(new_post_info, fp)







