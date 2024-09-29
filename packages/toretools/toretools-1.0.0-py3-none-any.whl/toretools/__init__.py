# -*- coding: utf-8 -*-

#
# ToreTools - The useful tools for creating mathematical programs and more.
#
# Torrez Tsoi
# that1.stinkyarmpits@gmail.com
#
# License: MIT
#


from os.path import dirname, join as pjoin

from .toretools import *

from . import __version__

globals().update(dict((k, v) for k, v in __version__.__dict__.items()))
