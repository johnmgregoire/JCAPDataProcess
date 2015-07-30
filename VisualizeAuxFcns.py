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


def createontheflyrundict(expfiledict, expfolder, lastmodtime=0):

    d=expfiledict['run__1']['files_technique__onthefly']['all_files']
    d_appended={}
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
        d_appended[fn]=d[fn]
    return modtime, d_appended

def d_nestedkeys(d, keylist):
    return reduce(lambda dd, k: dd[k], keylist, d)


#plateid,code,sample,fom,xy,comp
def extractplotdinfo(fomd, fomname):
    d=fomd
    returnlist=[d[k] for k in ['plateid','code','sample_no', fomname]]
    if d['sample_no']==0:
        returnlist+=[[numpy.nan]*2, [numpy.nan]*4]
    else:
        pmd=self.expfiledict['run__%d' %d['runint']]['platemapdlist'][rund['platemapsamples'].index(d['sample_no'])]
        returnlist+=[[pmd[k] for k in ['x', 'y']]]
        returnlist+=[[pmd[k] for k in ['A', 'B', 'C', 'D']]]
    return returnlist
    
    


class treeclass_anaexpfom():
    def __init__(self, tree):
        self.treeWidget=tree
        
    def initfilltree(self, expfiledict, anafiledict):
        self.treeWidget.clear()
        self.fomwidgetItem=
    
        self.expfileitem_forappend
    def appendexpfiles(self, d_appended)
        self.nestedfill(d_appended, self.expfileitem_forappend, laststartswith='xxxx')
    def getusefombools(self):
        mainitem=self.fomwidgetItem
        l_usefombool=[bool(mainitem.child(i).checkState(0)) for i in range(mainitem.childCount())]
        return l_usefombool
        
        
        
    def filltree(self, d, startkey='ana_version', laststartswith='ana__'):
        self.treeWidget.clear()
        #assume startkey is not for dict and laststatswith is dict
        
        mainitem=QTreeWidgetItem([': '.join([startkey, d[startkey]])], 0)
        self.treeWidget.addTopLevelItem(mainitem)
        self.treeWidget.setCurrentItem(mainitem)
        
        for k in sorted([k for k, v in d.iteritems() if k!=startkey and not isinstance(v, dict)]):
            mainitem=QTreeWidgetItem([': '.join([k, str(d[k])])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            
        for k in sorted([k for k, v in d.iteritems() if not k.startswith(laststartswith) and isinstance(v, dict)]):
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
            
        anakl=sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in anakl:
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
    def nestedfill(self, d, parentitem, laststartswith='files_'):
        nondictkeys=sorted([k for k, v in d.iteritems() if not isinstance(v, dict)])
        for k in nondictkeys:
            item=QTreeWidgetItem([': '.join([k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys1=sorted([k for k, v in d.iteritems() if not k.startswith(laststartswith) and isinstance(v, dict)])
        for k in dictkeys1:
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], item)
            parentitem.addChild(item)
        dictkeys2=sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in dictkeys2:
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], item)
            parentitem.addChild(item)
    def createtxt(self, indent='    '):
        self.indent=indent
        return '\n'.join([self.createtxt_item(self.treeWidget.topLevelItem(count)) for count in range(int(self.treeWidget.topLevelItemCount()))])
        
    def createtxt_item(self, item, indentlevel=0):
        str(item.text(0))
        itemstr=self.indent*indentlevel+str(item.text(0)).strip()
        if item.childCount()==0:
            return itemstr
        childstr='\n'.join([self.createtxt_item(item.child(i), indentlevel=indentlevel+1) for i in range(item.childCount())])
        return '\n'.join([itemstr, childstr])
    
    def partitionlineitem(self, item):
        s=str(item.text(0)).strip()
        a, b, c=s.partition(':')
        return (a.strip(), c.strip())
    def createdict(self):
        return dict(\
        [self.createdict_item(self.treeWidget.topLevelItem(count))\
            for count in range(int(self.treeWidget.topLevelItemCount()))])
        
    def createdict_item(self, item):
        tup=self.partitionlineitem(item)
        if item.childCount()==0:
            return tup
        d=dict([self.createdict_item(item.child(i)) for i in range(item.childCount())])
        return (tup[0], d)

