# -*- coding: UTF-8 -*-
from __future__ import print_function

import logging
import sys, os, os.path
import inspect

from .commands import command
from .common import commands, firstline

logger = logging.getLogger(__name__)

@command
def help(name=None):
    """display this help message"""
    script = os.path.basename(sys.argv[0])
    if name:
        help_one(name, complete=True)
        return
    print("%s: command line interface" % script)
    print("usage: %s COMMAND OPTIONS" % script)
    print("="*40)
    print("")
    index()

def help_one(name, func=None, complete=False):
    if not func: func = commands[name]
    args, varargs, varkw, defaults = inspect.getargspec(func)
    args_help = inspect.formatargspec(
        args, varargs, varkw, defaults,
        formatvalue=lambda s: "=["+str(s)+"]"
        )[1:-1].replace(', ', ' ')
    print("\t%s %s" % (name, args_help))
    if complete:
        print("\t\t%s" % func.__doc__.strip())
    else:
        print("\t\t%s" % firstline(func.__doc__))

def index():
    for name, func in commands.items():
        help_one(name, func)


def main():
    options = sys.argv[1:]
    try: name = options.pop(0)
    except IndexError: name = None
    func = commands.get(name, None)
    if not func: return help()
    ls = []
    kw = {}
    for option in options:
        if '=' not in option:
            ls.append(option)
        else:
            key, value = option.split('=', 1)
            kw[key] = value
    func(*ls, **kw)

if __name__ == '__main__':
    main()
