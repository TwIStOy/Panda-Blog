# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='blog.log',
                    filemode='w')


console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def debug(message):
    return logging.debug(message)


def info(message):
    return logging.info(message)


def warning(message):
    return logging.warning(message)


def critical(message):
    return logging.critical(message)


def error(message):
    return logging.error(message)


