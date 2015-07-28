import time
import os, os.path, shutil
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import pylab
from fcns_math import *
from fcns_io import *
from fcns_ui import *


def createontheflyrundict(expfiledict, expfolder, lastmodtime=0, append=True):
    if (not append) or not 'files_technique__onthefly' in expfiledict['run__1'].keys():
        expfiledict['run__1']['files_technique__onthefly']={}
        expfiledict['run__1']['files_technique__onthefly']['all_files']={}
    d=expfiledict['run__1']['files_technique__onthefly']['all_files']
    
    fnl=os.listdir(expfolder)

    modtimes=[os.path.getmtime(os.path.join(expfolder, fn)) for fn in fnl]
    modtime=max(modtimes)
    fnl2=[fn for fn, mt in zip(fnl, modtimes) if mt>lastmodtime]
    
    for fn in fnl2:
        p=os.path.join(expfolder, fn)
        smp, attrd=smp_dict_generaltxt(p, delim='', returnsmp=True, addparams=False, lines=None, returnonlyattrdict=True)
        if len(attrd)==0:
            print 'error reading ', fn
            if fn in d.keys():
                del d[fn]#there was a previous versino of this file that has been overwritten
            continue
        d[fn]=copy.copy(attrd)
    return modtime
