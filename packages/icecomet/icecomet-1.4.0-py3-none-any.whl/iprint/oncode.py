import inspect
import os
import sys


def oncode():
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    filename = info.filename.split('/')[:-1]
    filename = '/'.join(filename)
    print(filename)
    os.chdir(filename)

