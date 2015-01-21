__author__ = 'TwIstOy'


import collections
import sys


class ArgParserError(Exception):
    pass


class ArgParser(object):

    def __init__(self):
        self.catch_list_short = dict()
        self.catch_list_long = dict()
        self.info = collections.namedtuple('info', 'metavar type_return default des help_doc need')

    def exit(self):
        sys.stderr.write("Error command arguments.")
        sys.exit(1)

    def parse_argument(self, args):
        state = 'CATCH'
        where = None
        rv = dict()
        for arg in args:
            if state == 'CATCH':  # catch state
                if arg.startwith('--'):  # long argument
                    if arg in self.catch_list_long:
                        if self.catch_list_long[arg].need:
                            state = 'GET'
                            where = self.catch_list_long[arg]
                    else:
                        self.exit()
                else:  # short argument
                    if self.catch_list_short[arg].need:
                        state = 'GET'
                        where = self.catch_list_short[arg]
                    else:
                        self.exit()
            else:  # GET state
                if arg.startwith('-'):
                    self.exit()
                rv[where.des] = where.type_return(arg)
        return rv

    def add_argument(self, *args, **kwargs):
        info_now = self.info(**kwargs)
        for arg in args:
            if not isinstance(arg, str):
                raise ArgParserError("Input object is not str. Please check and retry.")
            arg = arg.strip()
            if len(arg) <= 3:
                catch = '-' + arg
                if catch in self.catch_list_short:
                    raise ArgParserError('{arg} already exists.'.format(catch))
                self.catch_list_short[catch] = info_now
            else:
                catch = '--' + arg
                if catch in self.catch_list_long:
                    raise ArgParserError('{arg} already exists.'.format(catch))
                self.catch_list_long[catch] = info_now

