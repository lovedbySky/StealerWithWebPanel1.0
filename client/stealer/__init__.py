import os, sys
from tempfile import gettempdir

from .browsers import Chromium, Firefox
from .get_info import GetInfo


__version__ = '1.0.0'
info = GetInfo()
chromium = Chromium()
firefox = Firefox()

__path = os.getcwd()
sys.path.append(os.path.join(__path, '..'))

import config

tempdir = gettempdir()
os.chdir(tempdir)
