# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

from .. import post
import os
import collections
from jinja2 import Environment, FileSystemLoader
import controller_error


class Loader(object):
    """Loader is the first part of the controller.
        plugin can be registered at such positions as key strings:
            - before all(include init): "<"
            - before load post: "< post"
            - after load post: "> post"
            - before load page: "< page"
            - after load page: "> page"
            - before load template: "< template"
            - after load template: "> template"
            - after all(now it is same as "> template", it may change later): ">"
        Loader works in such order:
            init -> load post -> load page -> load template
    """

    def __init__(self, root, global_config):
        # the path of '/panda/src'
        self.root = root
        self.global_config = global_config
        self.callback = collections.defaultdict(list)

    def _init(self):

        # Init paths include 'post', 'template', 'page'
        self.paths = dict()
        self.paths['post'] = os.path.join(self.root, 'post')
        self.paths['template'] = os.path.join(os.path.join(self.root, 'theme'),
                                              self.global_config.get('theme'))
        self.paths['page'] = os.path.join(self.root, 'page')

    def register(self, position, callback):
        """register callback at position.
        callback object must be callable and no return,
        the Loader(self) will pass into the callback function.
        """
        position_key = ['<', '< post', '> post', '< page', '> page',
                        '< template', '> template', '>']
        if position not in position_key:
            raise controller_error.ControllerError('Error position register in Loader.')
        self.callback[position].append(callback)

    def _load_post(self):
        file_list = os.listdir(self.paths['post'])
        file_list = filter(lambda name: name.endwith(".md"), file_list)
        posts = map(lambda name: post.Post(name, self.global_config), file_list)
        urls = []
        for p in posts:
            p.get_url(urls)
        return posts

    def _load_page(self):
        file_list = os.listdir(self.paths['page'])
        file_list = filter(lambda name: name.endwith(".md"), file_list)
        return map(lambda name: post.Post(name, self.global_config), file_list)

    def _load_template(self):
        env = Environment(loader=FileSystemLoader(self.paths['template']))
        template_names = ['post', 'tag', 'month', 'author', 'index', 'page', 'category']
        template = {name: env.get_template("{}.html".format(name)) for name in template_names}
        return template

    def _load(self):
        self._init()
        parts = ['post', 'page', 'template']
        resource = dict()
        for part in parts:
            for func in self.callback['< {}'.format(part)]:
                func(self)
            resource[part] = getattr(self, "_load_{}".foramt(part))()
            for func in self.callback['> {}'.format(part)]:
                func(self)
        return resource

    def run(self):
        """Loader will run the plugins in order
        :return: all the resource
        """
        for func in self.callback['<']:
            func(self)
        rv = self._load()
        for func in self.callback['>']:
            func(self)
        return rv