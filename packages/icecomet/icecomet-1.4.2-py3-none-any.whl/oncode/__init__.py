import inspect
import os
import sys
def get_filename():
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    return info.filename

def oncode():
    filename = get_filename().split('/')[:-1]
    filename = '/'.join(filename)
    os.chdir(filename)


