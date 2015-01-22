# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import os
import Log as log
import hashlib
import MkTransfer as mkt
import json
import codecs


def create_dir(new_dir):
    """works for a good mkdir attribute
    - already exists, silence
    - it's a file, raise an exception
    - parent dictionary don't exists, create them as well
    """
    if os.path.isdir(new_dir):
        return
    if os.path.isfile(new_dir):
        raise OSError("A file <{0}> exists. Please check it and retry.".format(new_dir))

    parent, son = os.path.split(new_dir)
    if parent and not os.path.isdir(parent):
        log.debug("For create {son}, create {parent}".format(son=son, parent=parent))
        create_dir(parent)
    if son:
        os.mkdir(new_dir)


def get_file_md5(fp):
    md5 = hashlib.md5()
    buff_size = 8096
    while True:
        read_part = fp.read(buff_size)
        if not read_part:
            break
        md5.update(read_part)
    return md5.hexdigest()


def mk_transfer(fp):
    return mkt.convert(fp.read())


def _get_path(*parts):
    new_parts = []
    for p in parts:
        if not isinstance(p, str) and hasattr(p, "__iter__"):
            new_parts.extend(_get_path(*p))
        else:
            new_parts.append(p)
    return new_parts


def get_path(*parts):
    new_parts = _get_path(*parts)
    rv = ""
    for index, part in enumerate(new_parts):
        if index == 0:
            rv = part
        else:
            rv = os.path.join(rv, part)
    return rv


def get_json(file_path):
    """works for a good json.load attribute
    - already exists, read it and return json object
    - not exists, create an empty json file and return its json object
    - it's a folder, raise an exception
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        with codecs.open(file_path, "w", encoding='utf-8') as fp:
            fp.write("{}")
    if os.path.isdir(file_path):
        raise OSError('{} is wanted to be a json file.'.format(file_path))
    with codecs.open(file_path, "r", encoding='utf-8') as fp:
        info = json.load(fp)
    return info