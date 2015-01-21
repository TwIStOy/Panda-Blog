# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import os
import urllib
import re
import log
import util


def get_post_meta_from_file(fp):
    """Takes a file and return a dict containing meta-data from the text file. It will try to extract
    meta-info from every line before it reach the first empty line, which separates the meta-date and the content.
    Each meta-info should be in the form of "attr:value". Attributes are case-insensitive during analyzing
    and output attribute will be in lower-case. Any text unrecognized as meta info will be treated as content.
    :return: a dict containing meta-info
    """
    meta = dict()
    try:
        fp.seek(0)
    except:
        pass
    for line in fp.readline():
        if line == '':
            return meta
        result = re.search('^(.+?):(.+)$', line, re.IGNORECASE)
        if result:
            attr, value = result.group(1).strip().lower(), result.group(2).strip()
            meta[attr] = value
    return meta


class PostError(Exception):
    pass


class Post(object):
    def __init__(self, root, global_config):

        # Check for necessary files.
        self.fp = open(root, "r", "utf-8")
        config = analyze_post(self.fp)
        self.root = root

        # *post content*. It shouldn't be read before we can determine whether the post should be compile.
        self.content = None

        # *post title*. Necessary.
        self.title = config.get('title')
        if not self.title:
            raise PostError('No keyword "title" in "info.json". Please Check and retry.')

        # *post base url*. The final url will be determined after calling get_url()
        # Try to set it from "info.json". If can't will be set as its title.
        self._base_url = config.get('url')
        if not self._base_url:
            self._base_url = urllib.urlencode(self.title)
        self.url = None

        # Try to get *post tag* from "info.json". Read them and splits them into tags by ','.
        self.tag = config.get('tag')
        if self.tag:
            self.tag = re.split(',\s*', self.tag)
        else:
            self.tag = []

        # Get *post author* from info.json.
        # Will set it to "default_author" from global_config on failure.
        self.author = config.get('author')
        if not self.author:
            self.author = global_config.get('default_author')

        # *post create time*. Can't be ommited.
        # Then split it into year, month, date.
        self.create_time = config.get('create_time')
        if not self.create_time:
            raise PostError('No keyword "create_time" in "info.json". Please Check and retry.')
        self.year, self.month, self.date = [int(item) for item in self.create_time.split('-')]

        # Try to get *post category* from "info.json".
        # Will set to Uncategorized" on failure.
        self.category = config.get('category')
        if not self.category:
            self.category = "Uncategorized"

        # Hash post with md5 algorithm
        with open(os.path.join(root, 'content.md'), "r", "utf-8") as fp:
            self.md5 = util.get_file_md5(fp)

        # This will be set to True if this post needs compilation, False if not.
        self.make = True

        log.debug("Load post success! {dir}".format(dir=root))

    def get_content(self):
        """self.content will be set after this method.
            It convert markdown file to HTML file.
        :return:
        """
        self.content = util.mk_transfer(self.fp.read())
        return self

    def get_url(self, urls):
        """self.url will be set after calling this method.
        urls is the list contains urls of all posts. This method will check
        if there's any url conflict.
        If a conflict occur, it will try to change the url to avoid conflict.
        """
        now = self._base_url
        addition = 1
        while now in urls:
            addition += 1
            now = now + "," + str(addition)
        self.url = now
        return self

    def __le__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.date != other.date:
            return self.date < other.date

    def __ge__(self, other):
        return not self.__le__(other)

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and self.date == other.date

