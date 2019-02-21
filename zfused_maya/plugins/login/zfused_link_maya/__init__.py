import sys
import os

DIRNAME = os.path.dirname(__file__)
sys.path.insert(0, DIRNAME)
sys.path.insert(0, "{}/packages".format(DIRNAME))
sys.path.insert(0, "{}/zfused_login".format(DIRNAME))

from zfused_login import *