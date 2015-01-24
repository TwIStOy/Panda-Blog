__author__ = 'TwIstOy'

import codecs
import os
import Util
import argparse
import time

name_to_command = dict()
parser = argparse.ArgumentParser('panda: a simple static blog generator. \n'
                                 '\tThere are modes: create, delete, init, generate.\n'
                                 '\tcreate mode: ["create", "new", "add", "n"]\n'
                                 '\tdelete mode: ["delete", "omit", remove", "d"]\n'
                                 '\tinit mode: ["init", "i"]\n'
                                 '\tgenerate mode: ["generate", "g"]\n'
                                 "Here's the options:")
parser.add_argument('-t', '--title', metavar='TITLE', default='hello world', type=str, dest='title',
                    help="The title of post or page. Only used in <create mode>.")
parser.add_argument('-d', '--date', metavar='DATE',
                    default=time.strftime('%Y-%m-%d',time.localtime(time.time())), type=str, dest='date',
                    help="The data of post or page. Format YY-MM-DD. Only used in <create mode>.")
parser.add_argument('-a', '--author', metavar='AUTHOR', default=None, dest='author',
                    help='The author of post or page. Only used in <create mode>.')
parser.add_argument('-u', '--url', metavar='URL', default=None, type=str, dest='url',
                    help='The url of post or page. Only used in <create mode>. If not'
                         'specified, it will be the quote of title.')
parser.add_argument('-T', '--tags', metavar='TAGS', dest='tags', default=None,
                    help='The tags of new post. If not specified, it will be empty. You'
                         'can split them will ",".')

parser.add_argument('-c', '--category', metavar='CATEGORY', dest='category', default=None,
                    help='The category of new post. If not specified, it will be "Uncategorized".')
parser.add_argument('-f', '--filename', metavar='FILENAME', dest='filename', default=None,
                    help='The filename which you want to operate.')
parser.add_argument('-F', '--form', metavar='FORM', dest='form', default=None,
                    help='Which form you want to operate. "post" of "page".')


class ArgumentError(Exception):
    pass


def create_action(info):
    infos = ['title', 'date', 'tags', 'category', 'author', 'url']
    if info.form and info.filename:
        context = []
        for name in infos:
            if getattr(info, name):
                context.append('{name}: {value}'.format(name=name, value=getattr(info, name)))
        with codecs.open(Util.get_path(os.getcwd(), "src", info.form, info.filename)) as fp:
            context.extend(["", "# hello world"])
            fp.write("\n".join(context))
    else:
        raise ArgumentError('Necessary option is missing.')


name_to_command['create'] = 'create'
name_to_command['add'] = 'create'
name_to_command['new'] = 'create'
name_to_command['n'] = 'create'


def delete_action(info):
    if info.form and info.filename:
        file_path = Util.get_path(os.getcwd(), "src", info.form, info.filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    else:
        raise ArgumentError('Necessary option is missing.')


name_to_command['delete'] = 'delete'
name_to_command['remove'] = 'delete'
name_to_command['omit'] = 'delete'
name_to_command['d'] = 'delete'


def init_action(info):
    if info.root:
        root = info.root
    else:
        root = os.getcwd()
    Util.create_dir(Util.get_path(root, 'src', 'post'))
    Util.create_dir(Util.get_path(root, 'src', 'page'))
    Util.create_dir(Util.get_path(root, 'public', 'post'))
    Util.create_dir(Util.get_path(root, 'public', 'page'))
    Util.create_dir(Util.get_path(root, 'theme', 'default'))
    # todo: default theme should be written to file here


name_to_command['init'] = 'init'
name_to_command['i'] = 'init'


def generate_action(info):
    import Core

    if info.root:
        Core.Core(info.root).run()
    else:
        Core.Core(os.getcwd()).run()


name_to_command['generate'] = 'generate'
name_to_command['g'] = 'generate'


def help_action(info):
    parser.print_help()

name_to_command['help'] = 'help'
name_to_command['h'] = 'help'


def arg_parse(arg_list):
    if arg_list[0] not in name_to_command:
        raise ArgumentError('{} is illegal.'.format(arg_list[0]))
    return parser.parse_args(arg_list[1])