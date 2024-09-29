#!/usr/bin/env python
#
# EchoWave - Never use print() to debug again
#
# License: MIT
#

from os.path import dirname, join as pjoin

from .echowave import *  # noqa
from .builtins import install, uninstall

from . import __version__

globals().update(dict((k, v) for k, v in __version__.__dict__.items()))
