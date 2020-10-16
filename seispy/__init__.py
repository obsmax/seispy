import sys, glob, os
import numpy as np
import matplotlib.pyplot as plt

# fuck distutils2
version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
with open(version_file, "r") as fh:
    __version__ = fh.read().rstrip('\n')

from seispy.trace import Trace
from seispy.stream import Stream, readseispystream
