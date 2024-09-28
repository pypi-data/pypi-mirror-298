import os
import sys


def cd_me():
    os.chdir(os.getcwd())

if __name__=='__main__':
    pass
else:
    cd_me()
    print('a')



