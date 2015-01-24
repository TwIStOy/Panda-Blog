__author__ = 'TwIStOy'

import os
import json
import shutil
import itertools
import collections
import codecs
import Error
import Util


class Processor(object):
    """Processor is the second part of the controller.
        plugin can be registered at such positions as key string:
            - before all(include init): "<"
            - before post verify(md5): "< post md5"
            - after post verify(md5): "> post md5"
            - before post verify(public): "< post public"
            - after post verify(public): "> post public"
            - before page verify(md5): "< page md5"
            - after page verify(md5): "> page md5"
            - before page verify(public): "< page public"
            - after page verify(public): "> post page"
            - before archive_modified select: "< archive"
            - after archive_modified select: "> archive"
            - after all: ">"
        Selector works in such order:
            init -> post_md5_verify -> post_public_verify -> page_md5_verify ->
            page_public_verify -> archive_modified
    """

    def _select(self):
        rv = dict()
        for p in ['post', 'page']:
            for a in ['md5', 'public']:
                for func in self.callback['< {p} {a}'.format(p=p, a=a)]:
                    func(self)
                getattr(self, '_{a}_verify'.format(a=a))(p)
                for func in self.callback['> {p} {a}'.format(p=p, a=a)]:
                    func(self)
        rv['post'] = filter(lambda po: po.need_compilation, self.resource['post'])
        rv['page'] = filter(lambda pa: pa.need_compilation, self.resource['page'])
        for func in self.callback['< archive']:
            func(self)
        rv['archive'] = self._archive()
        for func in self.callback['> archive']:
            func(self)
        return rv

    def run(self, resource):
        """Selector will run in order
        :return: all the resource must be compile
        """
        for func in self.callback['<']:
            func(self)
        self._init(resource)
        rv = self._select()
        for func in self.callback['>']:
            func(self)
        return rv

    # This will be later api
    def process(self, resource):
        pass

    def register(self, position, callback):
        """register callback at position.
        callback object must be callable and no return,
        the Selector(self) will pass into the callback function.
        """
        position_key = ['<', '< post md5', '> post md5', '< page md5', '> page md5',
                        '< post public', '> post public', '< page public', '> page public',
                        '< archive', '> archive', '>']
        if position not in position_key:
            raise Error.CoreError('Error position register in Selector.')
        self.callback[position].append(callback)

    def __init__(self, root, global_config):
        # root: /panda/
        self.root = root
        self.resource = None
        self.callback = dict()

    def _init(self, resource):
        self.resource = resource

    def _md5_verify(self, which):
        """verify posts' md5, if equal, "make" will be False
        :return:
        """
        info = Util.get_json(Util.get_path(self.root, "src", which, ".info"))
        new_post_info = dict()
        for p in self.resource[which]:
            if p.md5 == info.get(p.url):
                p.need_compilation = False
            new_post_info[p.url] = p.md5
        with codecs.open(Util.get_path(self.root, "src", which, ".info"), "w", encoding='utf-8') as fp:
            json.dump(new_post_info, fp)

    def _public_verify(self, which):
        """verify posts with public info, if not equal, "make" will be True
        :return:
        """
        public_post_list = filter(lambda name: os.path.isdir(name),
                                  os.listdir(Util.get_path(self.root, "public", "post")))
        public_info = Util.get_json(Util.get_path(self.root, "public", "post", ".info"))

        garbage = []
        posts = self.resource[which]
        url_to_root = {post.url: post for post in posts}
        for public in public_post_list:
            if public in url_to_root:
                if url_to_root[public].root != public_info.get(public):
                    url_to_root[public].need_compilation = True
            else:
                garbage.append(public)

        new_public_info = {}
        for post in posts:
            if post.url not in public_post_list:
                post.need_compilation = True
            new_public_info[post.url] = post.root

        with codecs.open(Util.get_path(self.root, "public", which, ".info"), "w", encoding='utf-8') as fp:
            json.dump(new_public_info, fp)

        for name in garbage:
            shutil.rmtree(Util.get_path(self.root, "public", which, name))

    def _archive(self):
        archive = dict()
        archive['month'] = itertools.groupby(self.resource['post'],
                                             lambda p: "{}-{}".format(p.year, p.month))
        archive['tag'] = collections.defaultdict(list)
        for p in self.resource['post']:
            for t in p.tag:
                archive['tag'][t].append(p)
        archive['author'] = itertools.groupby(self.resource['post'], lambda p: p.author)
        archive['category'] = itertools.groupby(self.resource['post'], lambda p: p.category)

        def _archive_select(which):
            archive_info = Util.get_json(Util.get_path(self.root, 'public', 'archive', which, ".info"))
            new_archive_info = dict()
            for t, p in archive[which]:
                new_archive_info[t] = [p.root for p in archive[which][t]]
            file_list = filter(lambda name: os.path.isdir(
                Util.get_path(self.root, 'public', 'archive', which, name)), os.listdir(
                Util.get_path(self.root, 'public', 'archive', which)))
            garbage = [name for name in file_list if name not in new_archive_info]
            for name in garbage:
                shutil.rmtree(Util.get_path(self.root, 'public', 'archive', which, name))
            with codecs.open(Util.get_path(self.root, 'public', 'archive', which, ".info"), "w", encoding='utf-8') as fp:
                json.dump(new_archive_info, fp)
            return [t for t, p in new_archive_info if archive_info.get(t) == p]

        return {ahv: _archive_select(ahv) for ahv in ['tag', 'month', 'author', 'category']}
