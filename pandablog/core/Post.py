# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import urllib
import re
import Log as log
import Util as util
from datetime import datetime
import codecs


class PostError(Exception):
    pass


# TODO: write error handling to make this class more robust
class MetaInfo(object):
    def __init__(self):
        self.author = None
        self.category = None
        self.datetime = None
        self.tags = []
        self.title = None
        self.url = None

    def add_tags(self, string):
        self.tags += [tag.strip() for tag in string.split(',')]

    def set_tags(self, string):
        self.add_tags(string)

    def set_datetime(self, string):
        self.datetime = datetime.strptime(string, '%Y-%m-%d')

    def set_category(self, string):
        self.category = string

    def set_author(self, string):
        self.author = string

    def set_url(self, string):
        self.url = string

    def set_title(self, string):
        self.title = string

    def set_attr_value(self, attr, value):
        """set attribute value pair"""
        if attr in ['author', 'category', 'datetime', 'tags', 'title', 'url']:
            getattr(self, "set_{}".format(attr))(value)
        else:
            log.debug('Error attr in <set_attr_value> (attr="{attr}", value="{value}")'.format(
                attr=attr, value=value
            ))

    def init(self, config):
        """initialize self into a legal meta data suitable for blog content generation.
        legalize self by applying some default value from config
        """
        if not self.author:
            self.author = config.default_author
        if not self.category:
            self.category = config.default_category
        if not self.title:
            self.title = config.default_title
        if not self.datetime:
            self.datetime = config.default_datetime
        if not self.url:
            self.url = urllib.urlencode(self.title)

    def load_from_file(self, filename, config):
        """load meta data from a file. return self upon finishing"""
        try:
            fp = codecs.open(filename, 'r', 'utf-8')
            for line in fp.readline():
                if line == '':
                    break
                result = re.search('^(.+?):(.+)$', line, re.IGNORECASE)
                if result:
                    attr = result.group(1).strip().lower()
                    value = result.group(2).strip()
                    self.set_attr_value(attr, value)
        except Exception, e:
            log.warning('Cannot retrieve meta info from' + filename + '!\n' + str(e))
        return self.init(config)

    def __le__(self, other):
        return self.datetime < other.datetime

class Post(object):
    def __init__(self, filename, config):
        self.meta_info = MetaInfo()
        self.meta_info.load_from_file(filename, config)
        self.need_compilation = False
        self.filename = filename

    def init_meta(self):
        self.meta_info.load_from_file(self.filename)

    def generate_html_content(self):
        """Return generated html content"""
        with codecs.open(self.filename, 'r', 'utf-8') as fp:
            content = util.mk_transfer(fp.read())
        return content

    def get_url(self, urls):
        """Get the real url of the post. Resolve conflicts by appending -n to the base url"""
        now = self.meta_info.url
        if now in urls:
            now = now + '-'
            addition = 1
            while now + str(addition) in urls:
                addition += 1
            now = now + str(addition)
        self.url = now
        return self

    def __le__(self, other):
        return self.meta_info < other.meta_info
