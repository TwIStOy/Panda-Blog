# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import Util
import codecs


class Generator(object):
    """Renderer is the last part of the controller.
        It will render the all the pages(include post, page and archive), and write them into file.
        plugin can be registered at such positions as key strings:
            - before all(include init): "<"
            - before render post: "< post"
            - after render post: "> post"
            - before render page: "< page"
            - after render page: "> page"
            - before render template: "< archive"
            - after render template: "> archive"
            - after all(now it is same as "> archive", it may change later): ">"
        renderer works in such order:
            init -> render post -> render page -> render archive
    """
    def __init__(self, root, global_config):
        # root: /panda/
        self.callback = {}
        self.root = root
        self.resource = None
        self.for_render = None
        self.context = None
        self.global_config = global_config

    def _init(self, resource, for_render):
        self.resource = resource
        self.for_render = for_render
        self.context = {
            "page_title": "default",
            "site_title": self.global_config.get('title'),
            "site_description": self.global_config.get('description'),
            "site_url": self.global_config.get('url'),
            "nav_links": [{"url": "{}/page/{}/".format(self.global_config.get('url'), page.name),
                           'value': page.title} for page in resource['page']]
        }

    def _render_post(self, which):
        for post in self.for_render[which]:
            self.context['page_title'] = post.title
            self.context['post'] = post
            text = self.resource['template'][which].render(**self.context)
            Util.create_dir(Util.get_path(self.root, 'public', which, post.url))
            with codecs.open(Util.get_path(self.root, 'public', which, post.url, 'index.html'), 'w', encoding='utf-8') as fp:
                fp.write(text)

    def _render_archive(self, which):

        for ar, po in self.for_render['archive'][which]:
            self.context['page_title'] = "Archive {} - {}".format(which, ar)
            self.context['archive'] = po
            text = self.resource['template'][which].render(**self.context)
            Util.create_dir(Util.get_path(self.root, 'public', 'archive', which, ar))
            with codecs.open(Util.get_path(self.root, 'public', 'archive', which, ar, "index.html"), "w", encoding='utf-8') as fp:
                fp.write(text)

    def _render(self):
        for which in ['post', 'page']:
            for func in self.callback['< {}'.format(which)]:
                func(self)
            self._render_post(which)
            for func in self.callback['> {}'.format(which)]:
                func(self)
        for func in self.callback['< archive']:
            func(self)
        for which2 in ['tag', 'author', 'month', 'category']:
            self._render_archive(which2)
        for func in self.callback['> archive']:
            func(self)

    def run(self, resource, for_render):
        for func in self.callback['<']:
            func(self)
        self._init(resource, for_render)
        self._render()
        for func in self.callback['>']:
            func(self)

    # This is later api
    def generate(self, resource):
        pass
