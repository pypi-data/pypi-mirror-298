# -*- coding: utf-8 -*-

#
# IceCream - Never use print() to debug again
#
# License: MIT
#

import echowave


try:
    builtins = __import__("__builtin__")
except ImportError:
    builtins = __import__("builtins")


def install(ew="ew"):
    setattr(builtins, ew, echowave.ew)


def uninstall(ew="ew"):
    delattr(builtins, ew)
