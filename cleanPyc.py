#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

#清理 dir 目录下的.pyc文件
def cleanPyc(dir):
    if os.path.isdir(dir):
        for dirs,subdirs,files in os.walk(dir):
            for file in files:
                if '.pyc' in file:
                    os.system('rm -f {}'.format(os.path.join(dir,file)))
                    print("delete {} file".format(os.path.join(dir,file)))
    else:

        print ("must input directory file")



if __name__ == '__main__':

    try:
       dir = sys.argv[1]
       cleanPyc(dir)
    except IndexError as e:
        print(e.message)
