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
        (self.SaveFilesPushButton, self.savefiles), \
        (self.OpenPlatemapPushButton, self.openplatemap), \
        (self.AddMiscAnaPushButton, self.add_misc_to_ana), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        ]




        for cb in [self.ExpSaveComboBox, self.AnaSaveComboBox]:
            for count, opt in enumerate(['Do not save', 'Save in TEMP as .run', 'Save as .run', 'Save as .done']):
                cb.insertItem(count, opt)
            cb.setCurrentIndex(1)

        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)

        QObject.connect(self.CalcXLineEdit,SIGNAL("editingFinished()"),self.lookupsamples)
        QObject.connect(self.CalcYLineEdit,SIGNAL("editingFinished()"),self.lookupsamples)


        #QObject.connect(self.RunSelectTreeWidget, SIGNAL('itemChanged(QTreeWidgetItem*, int)'), self.runselectionchanged)
        QObject.connect(self.RcpTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem_readonly)
        QObject.connect(self.ExpTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem_exp)
        QObject.connect(self.AnaTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem_ana)
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

    def stdcopy_afd(self, afd, anafolder):
        p=os.path.join(afd['folderpath'], afd['fn'])
        newp=os.path.join(anafolder, afd['anafn'])
        shutil.copy(p, newp)

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
        self.expdict['exp_version']='3'
        self.expdict['description']='%d %s runs on plate_id %s' %(len(self.inds_rcpdlist), self.datatype, self.plate_idstr)
        self.anadict={}
        nextana=1
        anabool=int(self.AnaSaveComboBox.currentIndex())>0
        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpd=self.maindatad['rcpdlist'][ind_rcp]

            rcpdict={}
            rcpdict['experiment_type']=self.datatype
            runk='run__%d' %(runcount+1)
            self.expdict[runk]={}
            exprund=self.expdict[runk]
            exprund['run_use']='data'
            exprund['plate_id']=self.plate_idstr
            rcpd['parameters']['plate_id']=self.plate_idstr
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
                        anafiledlist=fd['ana_files'][an_name]
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
                                    self.anadict[anak]['plate_ids']=self.plate_idstr
                                    ana__d=self.anadict[anak]
                                else:
                                    anak=anl[0]
                                    ana__d=self.anadict[anak]
                                anrunk='files_%s' %runk
                                if not anrunk in ana__d.keys():
                                    ana__d[anrunk]={}
                                ana__d=ana__d[anrunk]

<<<<<<< HEAD
=======

>>>>>>> origin/master
                            newfn='%s_%s' %(anak, afd['fn'].replace('.xy', '.csv'))
                            afd['anafn']=newfn
                            afd['copy_fcn']=self.xrds_copy_xy_to_ana
                            antypek=afd['type']
                            if not antypek in ana__d.keys():
                                ana__d[antypek]={}
                            ana__d[antypek][newfn]=afd['fval']+smp#ana file val expected to have all other info included already
                            self.ana_filedict_tocopy+=[afd]
            self.all_rcp_dict['rcp_file__%d' %(runcount+1)]=rcpdict
        if anabool:
<<<<<<< HEAD
            if 'multirun_ana_files' in self.maindatad.keys() and len(self.maindatad['multirun_ana_files'])>0:
                for an_name, anafiledlist in self.maindatad['multirun_ana_files'].iteritems():
                    ana__d=None
                    for afd in anafiledlist:
                        if ana__d is None:
                            anl=[k for k, v in self.anadict.iteritems() if k.startswith('ana__') and an_name==v['name']]
                            if len(anl)==0:
                                anak='ana__%d' %nextana
                                nextana+=1
                                self.anadict[anak]={}
                                self.anadict[anak]['name']=an_name
                                self.anadict[anak]['technique']=self.datatype
                                self.anadict[anak]['plate_ids']=self.plate_idstr
                                ana__d=self.anadict[anak]
                            else:
                                anak=anl[0]
                                ana__d=self.anadict[anak]
                            anrunk='files_multi_run'
                            if not anrunk in ana__d.keys():
                                ana__d[anrunk]={}
                            ana__d=ana__d[anrunk]

                        newfn='%s_%s' %(anak, afd['fn'])
                        afd['anafn']=newfn
                        afd['copy_fcn']=self.stdcopy_afd
                        antypek=afd['type']
                        if not antypek in ana__d.keys():
                            ana__d[antypek]={}
                        ana__d[antypek][newfn]=afd['fval']
                        self.ana_filedict_tocopy+=[afd]
                            
            ananames=[anad['name'] for anak, anad in self.anadict.iteritems() if anak.startswith('ana__')]
            if len(ananames)==0:
                self.anadict={}
            else:
                self.anadict['plate_ids']=self.plate_idstr
                self.anadict['description']='%s on plate_id %s' %(','.join(set(ananames)), self.plate_idstr)
                self.anadict['ana_version']='3'

        self.RcpTreeWidgetFcns.filltree(self.all_rcp_dict, startkey='', laststartswith='rcp_file__', updatedwithtoplevelitems=True)
        self.ExpTreeWidgetFcns.filltree(self.expdict, startkey='exp_version', laststartswith='run__')
        self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')
    
    def add_misc_to_ana(self, p=None, anak=None, anarunk=None, filltreebool=True):
        if anak is None or anarunk is None:
            if not 'ana__1' in self.anadict.keys():
                return
            
            anakl=sort_dict_keys_by_counter(self.anadict, keystartswith='ana__')[::-1]
            anak=anakl[-1]
            anarunk='files_multi_run'

            for anak in anakl:
                if anarunk in self.anadict[anak].keys():
                    break
                l_anarunk=sort_dict_keys_by_counter(self.anadict[anak], keystartswith='files_run__')
                if len(l_anarunk)>0:
                    anarunk=l_anarunk[0]
                    break
            
            ans=userinputcaller(self, inputs=[('ana__X  key', str, anak), ('files_run__X  key', str, anarunk)], title='Enter location in .ana',  cancelallowed=True)
            if ans is None:
=======
            self.anadict['plate_ids']=self.plate_idstr
            self.anadict['description']='%s on plate_id %s' %(','.join(set([anad['name'] for anak, anad in self.anadict.iteritems() if anak.startswith('ana__')])), self.plate_idstr)
            self.anadict['ana_version']='3'
        self.RcpTreeWidgetFcns.filltree(self.all_rcp_dict, startkey='', laststartswith='rcp_file__', updatedwithtoplevelitems=True)
        self.ExpTreeWidgetFcns.filltree(self.expdict, startkey='exp_version', laststartswith='run__')
        self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')

    def add_misc_to_ana(self, p=None, anak=None, anarunk=None):
        if anak is None or anarunk is None:
            if not 'ana__1' in self.anadict.keys():
                return
            l_anarunk=sort_dict_keys_by_counter(self.anadict['ana__1'], keystartswith='files_run__')
            if len(l_anarunk)==0:
                return

            ans=userinputcaller(self, inputs=[('ana__ key', str, 'ana__1'), ('files_run__ key key', str, l_anarunk[0])], title='Enter location in .ana',  cancelallowed=True)
            if readonly or ans is None or ans[0].strip()==v:
>>>>>>> origin/master
                return
            anak=ans[0].strip()
            anarunk=ans[1].strip()

        if not anak in self.anadict.keys():
            return
        if not anarunk in self.anadict[anak].keys():
            return

        if p is None:
            p=mygetopenfile(parent=self, xpath=self.import_folder, markstr='select file for import into ana')
        if len(p)==0:
            return
        fold, fn=os.path.split(p)#would be prudent to check if this filename is already in the anak but hopefully user doesn't do this
        newfn='%s_%s' %(anak, fn)
        d=self.anadict[anak][anarunk]
        if not 'misc_files' in d.keys():
            d['misc_files']={}
        d['misc_files'][newfn]='user_import_file;'
        afd={}
        afd['folderpath']=fold
        afd['fn']=fn
        afd['anafn']=newfn
        afd['copy_fcn']=self.stdcopy_afd
        self.ana_filedict_tocopy+=[afd]
        if filltreebool:
            self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')
    def edittreeitem(self, item, column):
        self.editparams(None, item=item, column=column)
    def edittreeitem_readonly(self, item, column):
        self.editparams(None, item=item, column=column, readonly=True)
    def edittreeitem_exp(self, item, column):
        self.editparams(None, item=item, column=column, d=self.expdict)
    def edittreeitem_ana(self, item, column):
        self.editparams(None, item=item, column=column, d=self.anadict)
    def editparams(self, widget, item=None, column=0, readonly=False, d=None):
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
        if readonly or ans is None or ans[0].strip()==v:
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

        if d is None:
            return

        kl=[k.partition(':')[0].strip()]
        while not item.parent() is None:
            item=item.parent()
            kl=[str(item.text(0)).partition(':')[0].strip()]+kl

        while len(kl)>1:
            d=d[kl.pop(0)]
        d[kl[0]]=ans

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
        self.import_folder=p
        if self.maindatad is None:
            return
        self.plateidLineEdit.setText(self.plate_idstr)


        for count, rcpd in enumerate(self.maindatad['rcpdlist']):
            mainitem=QTreeWidgetItem(['temprun__%d' %(count+1)], 0)

            self.runtreeclass.fillmainitem_with_dlistvalues(mainitem, rcpd['file_dlist'], k='fn', v='fval')
            for fd in rcpd['file_dlist']:
                if 'ana_files' in fd.keys():
                    for an_name, auxfiledlist in fd['ana_files'].items():
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

    def cleardata(self, anadict=None):
        self.inds_rcpdlist=[]
        self.ana_filedict_tocopy=[]
        self.all_rcp_dict={}
        self.maindatad={}
        self.expdict={}
        self.anadict={}

        self.importfolderfcn=None
        self.createfiledictsfcn=None
        self.plotw_plate.axes.cla()
        self.plateidLineEdit.setText('')
        self.foldernameLineEdit.setText('')
        self.platemappathLineEdit.setText('')

        self.RunSelectTreeWidget.clear()
        self.RcpTreeWidget.clear()
        self.ExpTreeWidget.clear()
        self.AnaTreeWidget.clear()



    def savefiles(self):

        dropfolder=tryprependpath(EXPERIMENT_DROP_FOLDERS, os.path.join(self.datatype, 'drop'))
        if dropfolder is None:
            messageDialog(self, 'Aborting SAVE because cannot find drop folder').exec_()
            return

        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpfiled=self.all_rcp_dict['rcp_file__%d' %(runcount+1)]
            rcpname=rcpfiled['name']
            rcpfolder=os.path.join(dropfolder, rcpname)
            if os.path.isdir(rcpfolder):
                messageDialog(self, 'Aborting SAVE because at least 1 rcp drop folder exists').exec_()
                return

        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpfiled=self.all_rcp_dict['rcp_file__%d' %(runcount+1)]
            rcpname=rcpfiled['name']
            rcpfolder=os.path.join(dropfolder, rcpname)
            os.mkdir(rcpfolder)

            rcpd=self.maindatad['rcpdlist'][ind_rcp]
            for fd in rcpd['file_dlist']:
                shutil.copy(os.path.join(fd['folderpath'], fd['fn']), os.path.join(rcpfolder, fd['fn']))

            rcppath=os.path.join(rcpfolder, rcpname+'.rcp')
            filestr=self.RcpTreeWidgetFcns.createtxt(parentitem=rcpfiled['treeitem'])
            with open(rcppath, mode='w') as f:
                f.write(filestr)

        saveopt=int(self.ExpSaveComboBox.currentIndex())
        if self.expdict is None or len(self.expdict)==0:
            saveopt=0

        if saveopt>0:
            saveexpfiledict, dsavep=saveexp_txt_dat(self.expdict, saverawdat=False, experiment_type='temp' if saveopt==1 else self.datatype, rundone='.done' if saveopt==3 else '.run', file_attr_and_existence_check=False)
            expfolderpath, expfn=os.path.split(dsavep)
            expname=expfn.rpartition('.')[0]
        else:
            return #cannot save ana if not saving exp

        saveopt=int(self.AnaSaveComboBox.currentIndex())
        if self.anadict is None or len(self.anadict)==0:
            saveopt=0
        if saveopt>0:
            rp=compareprependpath(EXPFOLDERS_J+EXPFOLDERS_L, expfolderpath)
            self.anadict['experiment_path']=rp.replace(chr(92),chr(47))
            self.anadict['experiment_name']=expname
            self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')

            anatempfolder=getanadefaultfolder()
            anafilestr=self.AnaTreeWidgetFcns.createtxt()
            for afd in self.ana_filedict_tocopy:
                afd['copy_fcn'](afd, anatempfolder)# could be shutil.copy if no changes required
            anafolder=saveana_tempfolder(anafilestr, anatempfolder, anadict=None, analysis_type='temp' if saveopt==1 else self.datatype, rundone='.done' if saveopt==3 else '.run')

#        if saveopt>1:#everything now in the folder so copy to non-temp if necessary
#            saveana_tempfolder(None, anafolder, anadict=None, skipana=False, analysis_type=self.datatype, rundone='.done' if saveopt==3 else '.run')


    def lookupsamples(self, xyfcns=[]):
        if len(xyfcns)==0:
            try:
                fcnx=lambda X, Y:eval(str(self.CalcXLineEdit.text()).strip())
                fcnx(1., 1.)
                fcny=lambda X, Y:eval(str(self.CalcYLineEdit.text()).strip())
                fcny(1., 1.)
            except:
                messageDialog(self, 'Error with platemap X,Y formula').exec_()
                return
        else:
            fcnx, fcny=xyfcns

        xall, yall=numpy.array([fd['xyarr'] for count, rcpd in enumerate(self.maindatad['rcpdlist']) for fd in rcpd['file_dlist'] if 'xyarr' in fd.keys()]).T

        xpmall=fcnx(xall, yall)
        ypmall=fcny(xall, yall)
        xypmall=list(numpy.array([xpmall, ypmall]).T)

        pmx=numpy.array([d['x'] for d in self.platemapdlist])
        pmy=numpy.array([d['y'] for d in self.platemapdlist])
        pms=[d['sample_no'] for d in self.platemapdlist]


        xyplotinfo=[]
        for count, rcpd in enumerate(self.maindatad['rcpdlist']):
            for fd in rcpd['file_dlist']:
                if 'xyarr' in fd.keys():
                    xv, yv=xypmall.pop(0)
                    if numpy.isnan(xv) or numpy.isnan(yv):
                        continue
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
        if len(xl)==0:
            self.plotw_plate.fig.canvas.draw()
            return
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
    def filltree(self, d, startkey='ana_version', laststartswith='ana__', updatedwithtoplevelitems=False):
        self.treeWidget.clear()
        #assume startkey is not for dict and laststatswith is dict
<<<<<<< HEAD
        if len(d)==0:
            return
=======

>>>>>>> origin/master
        if len(startkey)>0:
            mainitem=QTreeWidgetItem([': '.join([startkey, d[startkey]])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            self.treeWidget.setCurrentItem(mainitem)

        for k in sorted([k for k, v in d.iteritems() if k!=startkey and not isinstance(v, dict) and not k=='treeitem']):
            mainitem=QTreeWidgetItem([': '.join([k, str(d[k])])], 0)
            self.treeWidget.addTopLevelItem(mainitem)

        for k in sorted([k for k, v in d.iteritems() if not k.startswith(laststartswith) and isinstance(v, dict)]):
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
            if updatedwithtoplevelitems:
                d[k]['treeitem']=mainitem

        anakl=sort_dict_keys_by_counter(d, keystartswith=laststartswith)
        for k in anakl:
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
            if updatedwithtoplevelitems and isinstance(d[k], dict):
                d[k]['treeitem']=mainitem


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
    def createtxt(self, parentitem=None, indent='    '):
        self.indent=indent
        if parentitem is None:
            itemlist=[self.treeWidget.topLevelItem(count) for count in range(int(self.treeWidget.topLevelItemCount()))]
        else:
            itemlist=[parentitem.child(count) for count in range(int(parentitem.childCount()))]
        return '\n'.join([self.createtxt_item(item) for item in itemlist])

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
