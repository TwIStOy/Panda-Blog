# -*- coding:utf-8 -*-
__author__ = 'TwIStOy Phunching'

import urllib
import re
import Log
import Util
from datetime import datetime
import codecs


# def get_post_meta_from_file(fp):
#     """Takes a file and return a dict containing meta-data from the text file. It will try to extract
#     meta-info from every line before it reach the first empty line, which separates the meta-date and the content.
#     Each meta-info should be in the form of "attr:value". Attributes are case-insensitive during analyzing
#     and output attribute will be in lower-case. Any text unrecognized as meta info will be treated as content.
#     :return: a dict containing meta-info
#     """
#     meta = dict()
#     try:
#         fp.seek(0)
#     except:
#         pass
#     for line in fp.readline():
#         if line == '':
#             return meta
#         result = re.search('^(.+?):(.+)$', line, re.IGNORECASE)
#         if result:
#             attr, value = result.group(1).strip().lower(), result.group(2).strip()
#             meta[attr] = value
#     return meta


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

    def _add_tags(self, string):
        self.tags += [tag.strip() for tag in string.split(',')]

    def _set_tags(self, string):
        self._add_tags(string)

    def _set_datetime(self, string):
        self.datetime = datetime.strptime(string, '%Y-%m-%d')

    def _set_category(self, string):
        self.category = string

    def _set_author(self, string):
        self.author = string

    def _set_url(self, string):
        self.url = string

    def _set_title(self, string):
        self.title = string

    def _set_attr_value(self, attr, value):
        """set attribute value pair"""
        if attr in ['author', 'category', 'datetime', 'tags', 'title', 'url']:
            getattr(self, "_set_{}".format(attr))(value)
        else:
            Log.debug('Error attr in <set_attr_value> (attr="{attr}", value="{value}")'.format(
                attr=attr, value=value
            ))

    def _default_setting(self, config):
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
        return self

    def load_from_file(self, fp, config):
        """load meta data from a file. return self upon finishing"""
        try:
            for line in fp.readline():
                if line == '':
                    break
                result = re.search('^(.+?):(.+)$', line, re.IGNORECASE)
                if result:
                    attr = result.group(1).strip().lower()
                    value = result.group(2).strip()
                    self._set_attr_value(attr, value)
        except Exception, e:
            Log.warning('Cannot retrieve meta info from' + fp.name + '!\n' + str(e))
        return self._default_setting(config)

    def __le__(self, other):
        return self.datetime < other.datetime


class Post(object):
    def __init__(self, filename, config):
        self.fp = codecs.open(filename, 'r', 'utf-8')
        self.meta_info = MetaInfo().load_from_file(self.fp, config)
        # self.need_compilation = True
        self.filename = filename
        self.url = None
        self.content = None

    def generate_html_content(self):
        """Generate html content"""
        self.content = Util.mk_transfer(self.fp.read())
        return self

    def get_url(self, urls):
        """Get the real url of the post. Resolve conflicts by appending -n to the base url"""
        now = self.meta_info.url
        if now in urls:
            now += '-'
            addition = 1
            while now + str(addition) in urls:
                addition += 1
            now += str(addition)
        self.url = now
        return self

    def __le__(self, other):
        return self.meta_info < other.meta_info

    def __ge__(self, other):
        return not self.__le__(other)
