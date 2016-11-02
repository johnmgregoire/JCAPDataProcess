import string
#import time
import os, os.path#, shutil
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib

import matplotlib.colors as colors
import matplotlib.cm as cm
#import matplotlib.mlab as mlab
#import pylab
#import pickle

projectpath=os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath,'QtForms'))
sys.path.append(os.path.join(projectpath,'AuxPrograms'))
sys.path.append(os.path.join(projectpath,'OtherApps'))

from xrd_io import *
from fcns_math import *
from fcns_io import *
from fcns_ui import *
from fcns_compplots import plotwidget
from ExternalImportForm import Ui_ExternalImportDialog

matplotlib.rcParams['backend.qt4'] = 'PyQt4'




class extimportDialog(QDialog, Ui_ExternalImportDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(extimportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent



        self.plotwsetup()
        button_fcn=[\
        (self.CreateFilesPushButton, self.createfiles_runprofilefcn), \
        (self.OpenFolderPushButton, self.importfolder), \
        (self.OpenPlatemapPushButton, self.openplatemap), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        ]
       



        for cb in [self.ExpSaveComboBox, self.AnaSaveComboBox]:
            for count, opt in enumerate(['Do not save', 'Save in TEMP as .run', 'Save as .run', 'Save as .done']):
                cb.insertItem(count, opt)
            cb.setCurrentIndex(3)

        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        QObject.connect(self.CalcXLineEdit,SIGNAL("editingFinished()"),self.lookupsamples)
        QObject.connect(self.CalcYLineEdit,SIGNAL("editingFinished()"),self.lookupsamples)

    
        #QObject.connect(self.RunSelectTreeWidget, SIGNAL('itemChanged(QTreeWidgetItem*, int)'), self.runselectionchanged)
        QObject.connect(self.RunSelectTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem)
        self.runtreeclass=treeclass_filedict(self.RunSelectTreeWidget)
        
        
        
        self.profiledefintionfcns=[self.xrds_profile]
                                      
        profiledesc=['Bruker XRDS data']
        for i, l in enumerate(profiledesc):
            self.ProfileComboBox.insertItem(i, l)
            

        
        self.RcpTreeWidgetFcns=treeclass_filedict(self.RcpTreeWidget)
        self.ExpTreeWidgetFcns=treeclass_filedict(self.ExpTreeWidget)
        self.AnaTreeWidgetFcns=treeclass_filedict(self.AnaTreeWidget)

        self.cleardata()

    
    def xrds_profile(self):
        self.importfolderfcn=get_rcpdlist_xrdolfder
        self.createfiledictsfcn=self.createfiledicts_xrds
        self.datatype='xrds'
        
    def raiseerror(self):
        raiseerror
    def xrds_copy_xy_to_ana(self, afd, anafolder):
        p=os.path.join(afd['folderpath'], afd['fn'])
        newp=os.path.join(anafolder, afd['anafn'])
        with open(p, mode='r') as f:
            lines=f.readlines()
        lines=[l.strip().replace(' ', ',') for l in lines]
        lines[0]=afd['fval'].partition(';')[2].partition(';')[0]
        s='\n'.join(lines)
        with open(newp, mode='w') as f:
            f.write(s)
            
    def createfiledicts_xrds(self):
        self.inds_rcpdlist=self.runtreeclass.getindsofchecktoplevelitems()
        self.ana_filedict_tocopy=[]
        self.all_rcp_dict={}
        self.expdict={}
        self.expdict['experiment_type']=self.datatype
        self.anadict={}
        nextana=1
        anabool=int(self.AnaSaveComboBox.currentIndex())>0
        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpd=self.maindatad['rcpdlist'][ind_rcp]
            
            rcpdict={}
            runk='run__%d' %(runcount+1)
            self.expdict[runk]={}
            exprund=self.expdict[runk]
            exprund['run_use']='data'
            
            exprund['rcp_file']=rcpd['name']+'.rcp'
            
            for k in ['name', 'parameters']:
                rcpdict[k]=rcpd[k]
                exprund[k]=rcpd[k]
            
            for fd in rcpd['file_dlist']:
                if not fd['tech'] in rcpdict.keys():
                    rcpdict[fd['tech']]={}
                    exprund[fd['tech']]={}
                if not fd['type'] in rcpdict[fd['tech']].keys():
                    rcpdict[fd['tech']][fd['type']]={}
                    exprund[fd['tech']][fd['type']]={}
                expfnval=str(fd['treeitem'].text(0)).partition(':')[2].strip()
                smp=expfnval.rpartition(';')[2].strip()
                rcpdict[fd['tech']][fd['type']][fd['fn']]=expfnval
                exprund[fd['tech']][fd['type']][fd['fn']]=expfnval
                if anabool:
                    item=fd['treeitem']
                    if int(item.childCount())==0:
                        continue
                    for i in range(item.childCount()):
                        an_name_item=item.child(i)
                        if not bool(an_name_item.checkState(0)):
                            continue
                        an_name=str(an_name_item.text(0))
                        anafiledlist=fd['aux_files'][an_name]
                        ana__d=None
                        for afd in anafiledlist:
                            if not bool(afd['treeitem'].checkState(0)):
                                continue
                            if ana__d is None:
                                anl=[k for k, v in self.anadict.iteritems() if k.startswith('ana__') and an_name==v['name']]
                                if len(anl)==0:
                                    anak='ana__%d' %nextana
                                    nextana+=1
                                    self.anadict[anak]={}
                                    self.anadict[anak]['name']=an_name
                                    self.anadict[anak]['technique']=self.datatype
                                    ana__d=self.anadict[anak]
                                else:
                                    anak=anl[0]
                                    ana__d=self.anadict[anak]
                                anrunk='files_%s' %runk
                                if not anrunk in ana__d.keys():
                                    ana__d[anrunk]={}
                                ana__d=ana__d[anrunk]
                            newfn='%s_%s' %(anak, afd['fn'])
                            afd['anafn']=newfn
                            afd['copy_fcn']=self.xrds_copy_xy_to_ana
                            ana__d[newfn]=afd['fval']+smp#ana file val expected to have all other info included already
                            self.ana_filedict_tocopy+=[afd]
            self.all_rcp_dict['rcp_file__%d' %(runcount+1)]=rcpdict
        self.RcpTreeWidgetFcns.filltree(self.all_rcp_dict, startkey='', laststartswith='rcp_file__')
        self.ExpTreeWidgetFcns.filltree(self.expdict, startkey='', laststartswith='run__')
        self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='', laststartswith='ana__')
        
    def edittreeitem(self, item, column):
        self.editparams(None, item=item, column=column)
        
    def editparams(self, widget, item=None, column=0):
        if item is None:
            item=widget.currentItem()
        s=str(item.text(column))
        st=s.partition(': ')
        k=''.join(st[:2])
        v=st[2].strip()
        if len(v)==0:
            print 'Error editing param,  no value detected: ', s
            return
        ans=userinputcaller(self, inputs=[(k, str, v)], title='Enter new param value',  cancelallowed=True)
        if ans is None or ans[0].strip()==v:
            return
        ans=ans[0].strip()
        
        warningbool = (True in [ws in k for ws in ['version']])
        parent=item.parent()
        if parent is None:
            parentstr=''
        else:
            parentstr=parent.text(0)
        warningbool = warningbool or True in [ws in parentstr or ws in k for ws in ['__', 'parameters', 'files_']]
        
        
        if warningbool:
            idialog=messageDialog(self, 'THIS IS CONSIDERED A READ-ONLY PARAMETER.\nYOU SHOULD PROBABLY "Cancel"')
            if not idialog.exec_():
                return
        item.setText(column,''.join([k, ans]))
        #below here is for modifying the dict from which the tree was made, but that is not needed in original operation owhere the tempana__ and ana files are editable but not .rcp, .exp, .ana trees
#        kl=[k.partition(':')[0].strip()]
#        while not item.parent() is None:
#            item=item.parent()
#            kl=[str(item.text(0)).partition(':')[0].strip()]+kl

#        d=self.anadict
#        while len(kl)>1:
#            d=d[kl.pop(0)]
#        d[kl[0]]=ans

    def importfolder(self, p=None):
        if p is None:
            p=mygetdir(parent=self, markstr='select folder containing all files for data import')
        if len(p)==0:
            return
        pid=self.get_plate_from_folder_path(p)
        if pid is None:
            ans=userinputcaller(self, inputs=[('plate_id', str, '')], title='Enter plate_id',  cancelallowed=True)
            if ans is None or len(ans[0].strip())==0 or not ans[0].isdigit():
                return
            pid=ans[0]
        self.plate_idstr=pid
        
        
        self.cleardata()
        self.profiledefintionfcns[self.ProfileComboBox.currentIndex()]()#defines the functions
        self.maindatad=self.importfolderfcn(p)
        if self.maindatad is None:
            return
        self.plateidLineEdit.setText(self.plate_idstr)
        
        
        for count, rcpd in enumerate(self.maindatad['rcpdlist']):
            mainitem=QTreeWidgetItem(['temprun__%d' %(count+1)], 0)

            self.runtreeclass.fillmainitem_with_dlistvalues(mainitem, rcpd['file_dlist'], k='fn', v='fval')
            for fd in rcpd['file_dlist']:
                if 'aux_files' in fd.keys():
                    for an_name, auxfiledlist in fd['aux_files'].items():
                        item=QTreeWidgetItem([an_name], 0)
                        item.setExpanded(False)
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                        item.setCheckState(0, Qt.Checked)
                        self.runtreeclass.fillmainitem_with_dlistvalues(item, auxfiledlist, k='fn', v='fval', checkbool=True)
                        fd['treeitem'].addChild(item)
            self.RunSelectTreeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(True)
            
        self.runtreeclass.maketoplevelchecked()
 

        self.foldernameLineEdit.setText(p)
        self.openplatemap(self.plate_idstr)



    def get_plate_from_folder_path(self, p):
        foldn=os.path.split(p)[1]
        serialstr=foldn.partition('_')[0]
        if len(serialstr)<3 or not serialstr.isdigit():
            return None
        return serialstr[:-1]
    def openplatemap(self, plate_idstr=None):
        if plate_idstr is None:
            pmpath=mygetopenfile(parent=self, xpath=PLATEMAPFOLDERS[0], markstr='select platemap')
            if len(pmpath)==0:
                return None
        else:
            pmpath, pmidstr=getplatemappath_plateid(plate_idstr, return_pmidstr=True)
            self.platemapdlist=readsingleplatemaptxt(pmpath, \
                        erroruifcn=\
                    lambda s:mygetopenfile(parent=self, xpath=PLATEMAPFOLDERS[0], markstr='Error: %s select platemap for plate_no %s' %(s, plate_idstr)))
        self.platemappathLineEdit.setText(pmpath)
        if not self.maindatad is None:
            self.lookupsamples()
        return



    def createfiles_runprofilefcn(self):
        if self.createfiledictsfcn is None:
            return
        self.createfiledictsfcn()
        

    def xrds_create_rcp_exp_ana(self):
        self.updateana()
        
        
    def updateana(self):
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.anadict[k]=s#this makes description just the last ana__ description
        
        
        #plateids=sorted(list(set(['%d' %rund['parameters']['plate_id'] for rund in [v for k, v in self.expfiledict.iteritems() if k.startswith('run__')]]))) #this old way of getting plate_ids will include plates for which analysis was not done
        
        ananames=sorted(list(set([anad['name'] for anad in [v for k, v in self.anadict.iteritems() if k.startswith('ana__')]])))
        plateidsstrlist_list=[anad['plate_ids'] for anad in [v for k, v in self.anadict.iteritems() if k.startswith('ana__')] if 'plate_ids' in anad.keys()]
        plateidsstrlist=sorted(list(set([idstr for liststr in plateidsstrlist_list for idstr in liststr.split(',')])))
        plateidsstr=','.join(plateidsstrlist)
        #self.anadict['plate_ids']=plateidsstr
        
        self.anadict['description']='%s on plate_id %s' %(', '.join(ananames), plateidsstr)
        self.AnaTreeWidgetFcns.filltree(self.anadict)
        
        self.fillanalysistypes(self.TechTypeButtonGroup.checkedButton())
        
    
        
    def cleardata(self, anadict=None):
        self.importfolderfcn=None
        self.createfiledictsfcn=None
        self.plotw_plate.axes.cla()
        self.plateidLineEdit.setText('')
        self.foldernameLineEdit.setText('')
        self.platemappathLineEdit.setText('')

#        self.analysisclass=None
#        self.activeana=None
#        self.anadict={}
#        
#        self.aux_exp_dlist=[]
#        self.aux_ana_dlist=[]
#        
#        self.paramsdict_le_dflt['description'][1]='null'
#        
#        if not anadict is None:
#            for k, v in anadict.iteritems():
#                self.anadict[k]=v
#            if 'description' in anadict.keys():
#                self.paramsdict_le_dflt['description'][1]=anadict['description']
#                
#        self.anadict['ana_version']='3'
#        
#        
#
#        self.AnaTreeWidget.clear()
#        
#        
#        if os.path.isdir(self.tempanafolder):
#            for fn in os.listdir(self.tempanafolder):
#                os.remove(os.path.join(self.tempanafolder, fn))
#        else:
#            self.tempanafolder=getanadefaultfolder(erroruifcn=lambda s:mygetdir(parent=self, markstr='select ANA default folder - to meet compliance this should be format %Y%m%d.%H%M%S.incomplete'))
#            #this is meant to result in rund['name']=%Y%m%d.%H%M%S but doesn't guarantee it
#            timestr=(os.path.split(self.tempanafolder)[1]).rstrip('.incomplete')
#            self.AnaNameLineEdit.setText(timestr)
#            self.paramsdict_le_dflt['name'][1]=timestr
 
    def saveana(self, dontclearyet=False, anatype=None, rundone=None):
        self.anafilestr=self.AnaTreeWidgetFcns.createtxt()
        for afd in self.ana_filedict_tocopy:
            afd['copy_fcn'](afd, anafolder)# could be shutil.copy if no changes required

#        if not 'ana_version' in self.anafilestr:
#            idialog=messageDialog(self, 'Aborting SAVE because no data in ANA')
#            idialog.exec_()
#            return
#        if anatype is None:
#            savefolder=None
#            dfltanatype=self.anadict['analysis_type']
#            idialog=SaveOptionsDialog(self, dfltanatype)
#            idialog.exec_()
#            if not idialog.choice or len(idialog.choice)==0:
#                return
#            anatype=idialog.choice
#            if anatype=='browse':
#                savefolder=mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Select folder for saving ANA')
#                if savefolder is None or len(savefolder)==0:
#                    return
#                rundone=''#rundone not used if user browses for folder
#            elif anatype==dfltanatype:#***saving in a place like eche or uvis then need to check if other things are there too
#                needcopy_dlist=find_paths_in_ana_need_copy_to_anatype(self.anadict, anatype)
#                if len(needcopy_dlist)>0:
#                    if None in needcopy_dlist:
#                        idialog=messageDialog(self, 'Aborting Save: Aux exp/ana in temp or not on K')
#                        idialog.exec_()
#                        return
#                    idialog=messageDialog(self, 'Need to copy EXP and/or ANA to %s to continue' %anatype)
#                    if not idialog.exec_():
#                        return
#                    for d_needcopy in needcopy_dlist: 
#                        errormsg=copyfolder_1level(d_needcopy['srcabs'], d_needcopy['destabs'])
#                        if errormsg:
#                            idialog=messageDialog(self, 'Aborting Save on exp/ana copy: ' %errormsg)
#                            idialog.exec_()
#                            return
#                        get_dict_item_keylist(self.anadict, d_needcopy['anadkeylist'][:-1])[d_needcopy['anadkeylist'][-1]]=d_needcopy['destrel']
#                    self.anafilestr=self.AnaTreeWidgetFcns.createtxt()
#        else:
#            savefolder=None
#            
#        if len(self.anafilestr)==0 or not 'ana_version' in self.anafilestr:
#            return
#
#        if rundone is None:
#            idialog=messageDialog(self, 'save as .done ?')
#            if idialog.exec_():
#                rundone='.done'
#            else:
#                rundone='.run'
#
#        anasavefolder=saveana_tempfolder(self.anafilestr, self.tempanafolder, analysis_type=anatype, anadict=self.anadict, savefolder=savefolder, rundone=rundone, erroruifcn=\
#            lambda s:mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select folder for saving ANA'))
#        
#        if not dontclearyet:
#            self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)#clear analysis happens here but exp_path wont' be lost
#        #self.cleardata()
#        return anasavefolder

    def lookupsamples(self, xyfcns=[]):
        if len(xyfcns)==0:
            try:
                fcnx=lambda X:eval(str(self.CalcXLineEdit.text()).strip())
                fcnx(1.)
                fcny=lambda Y:eval(str(self.CalcYLineEdit.text()).strip())
                fcny(1.)
            except:
                messageDialog(self, 'Error with platemap X,Y formula').exec_()
                return
        else:
            fcnx, fcny=xyfcns
        
        xall, yall=numpy.array([fd['xyarr'] for count, rcpd in enumerate(self.maindatad['rcpdlist']) for fd in rcpd['file_dlist'] if 'xyarr' in fd.keys()]).T
        
        xpmall=fcnx(xall)
        ypmall=fcny(yall)
        xypmall=list(numpy.array([xpmall, ypmall]).T)
        
        pmx=numpy.array([d['x'] for d in self.platemapdlist])
        pmy=numpy.array([d['y'] for d in self.platemapdlist])
        pms=[d['sample_no'] for d in self.platemapdlist]
        

        xyplotinfo=[]
        for count, rcpd in enumerate(self.maindatad['rcpdlist']):
            for fd in rcpd['file_dlist']:
                if 'xyarr' in fd.keys():
                    xv, yv=xypmall.pop(0)
                    pmi=numpy.argmin((pmx-xv)**2+(pmy-yv)**2)
                    smpstr='%d' %pms[pmi]
                    fd['fval']=';'.join([fd['fval'].partition(';')[0],smpstr])
                    fd['treeitem'].setText(0, ': '.join([fd['fn'], fd['fval']]))#the smpstr is kept track of in the tree widget so that it is user editable
                    xyplotinfo+=[(xv, yv, pmx[pmi], pmy[pmi], smpstr)]
        self.plot(xyplotinfo)

    def plot(self, xyplotinfo):
        
        self.plotw_plate.axes.cla()
        ax=self.plotw_plate.axes
        xl=[]
        yl=[]
        for xv, yv, xp, yp, s in xyplotinfo:
            ax.plot(xv, yv, 'ko')
            ax.plot([xv, xp], [yv, yp], 'r-')
            ax.text(xv, yv, s, ha='center', va='bottom')
            xl+=[xv]
            yl+=[yv]
        
        circ = pylab.Circle((50, 47.3), radius=50., edgecolor='k', facecolor='none')
        ax.add_patch(circ)
        
        x0, x1=0, 100
        y0, y1=0, 97.3
        x0=min(x0, min(xl))
        x1=max(x1, max(xl))
        y0=min(y0, min(yl))
        y1=max(y1, max(yl))
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        
        self.plotw_plate.fig.canvas.draw()
        
     

    def plotwsetup(self):

        self.plotw_plate=plotwidget(self)
        

        for b, w in [\
            (self.textBrowser_plate, self.plotw_plate), \
            ]:
            w.setGeometry(b.geometry())
            b.hide()
        
        self.plotw_plate.axes.set_aspect(1)

        axrect=[0.88, 0.1, 0.04, 0.8]

        self.plotw_plate.fig.subplots_adjust(left=0.12, bottom=.12)
    



class treeclass_filedict():
    def __init__(self, tree):
        self.treeWidget=tree
        self.treeWidget.clear()
    
    def getlistofchecktoplevelitems(self):
        return [str(self.treeWidget.topLevelItem(count).text(0)).strip().strip(':') for count in range(int(self.treeWidget.topLevelItemCount()))\
            if bool(self.treeWidget.topLevelItem(count).checkState(0))]
    def getindsofchecktoplevelitems(self):
        return [count for count in range(int(self.treeWidget.topLevelItemCount()))\
            if bool(self.treeWidget.topLevelItem(count).checkState(0))]
    def maketoplevelchecked(self):
        for count in range(int(self.treeWidget.topLevelItemCount())):
            item=self.treeWidget.topLevelItem(count)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
    def filltree(self, d, startkey='ana_version', laststartswith='ana__'):
        self.treeWidget.clear()
        #assume startkey is not for dict and laststatswith is dict
        
        if len(startkey)>0:
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
            
        anakl=sort_dict_keys_by_counter(d, keystartswith=laststartswith)
        for k in anakl:
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
            
        
    def fillmainitem_with_dlistvalues(self, mainitem, dlist, k='k', v='v', updatedwithitems=True, checkbool=None):
        for d in dlist:
            item=QTreeWidgetItem([': '.join([str(d[k]), str(d[v])])], 0)
            if not checkbool is None:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Checked if checkbool else Qt.Unchecked)
            mainitem.addChild(item)
            if updatedwithitems:
                d['treeitem']=item
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



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.extimportui=extimportDialog(self, title='Create RCP/EXP/ANA for non-HTE instruments', **kwargs)
            #self.calcui.importexp(exppath=r'K:\processes\experiment\eche\20161021.105822.copied-20161021221009715PDT\20161021.105822.exp')

            if execute:
                self.extimportui.exec_()
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()

