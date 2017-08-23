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
        (self.AddToAnaPushButton, self.add_to_ana), \
        (self.RaiseErrorPushButton, self.raiseerror), \
        ]




        for cb in [self.ExpSaveComboBox, self.AnaSaveComboBox]:
            for count, opt in enumerate(['Do not save', 'Save in TEMP as .run', 'Save as .run', 'Save as .done']):
                cb.insertItem(count, opt)
            cb.setCurrentIndex(3)
        
        QObject.connect(self.ExpSaveComboBox,SIGNAL("activated(QString)"), self.restrictanasave)
        
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



        self.profiledefintionfcns=[self.xrds_profile_withq, self.xrds_profile, self.ssrl_profile_v1]

        profiledesc=['Bruker XRDS with Q','Bruker XRDS data', 'SSRL v1']
        for i, l in enumerate(profiledesc):
            self.ProfileComboBox.insertItem(i, l)

        

        self.RcpTreeWidgetFcns=treeclass_filedict(self.RcpTreeWidget)
        self.ExpTreeWidgetFcns=treeclass_filedict(self.ExpTreeWidget)
        self.AnaTreeWidgetFcns=treeclass_filedict(self.AnaTreeWidget)

        self.cleardata()
        
        self.ProfileComboBox.setCurrentIndex(0)
        
    def restrictanasave(self):
        if self.AnaSaveComboBox.currentIndex()<=self.ExpSaveComboBox.currentIndex():
            return
        self.AnaSaveComboBox.setCurrentIndex(self.ExpSaveComboBox.currentIndex())
        
    def ssrl_profile_v1(self):
        from ssrl_io import *
        self.importfolderfcn=get_externalimportdatad_ssrl_batchresults
        self.createfiledictsfcn=self.createfiledicts
        self.mod_smp_afd_fcn=self.mod_afd_fcn__std
        self.mod_multi_afd_fcn=self.mod_afd_fcn__std
        self.datatype='ssrl'
        self.computernamedefault='HTE-SSRL-01'
        self.AddToAnaPushButton.setText('Create UDI')
        self.AddToAnaPushButton.setVisible(True)
        self.add_to_ana_fcn=self.create_udi
        self.CalcXLineEdit.setText('X')
        self.CalcYLineEdit.setText('Y')
        self.copy_all_to_ana_fcn=self.copy_all_to_ana__ssrl
        self.openmessage='select folder containing spec file and a subfolder "images"'
        
                
    def xrds_profile(self):
        self.importfolderfcn=get_externalimportdatad_xrds_folder
        self.createfiledictsfcn=self.createfiledicts
        self.mod_smp_afd_fcn=self.mod_smp_afd__xrds
        self.mod_multi_afd_fcn=self.mod_afd_fcn__std
        self.datatype='xrds'
        self.computernamedefault='HTE-XRDS-01'
        self.copy_all_to_ana_fcn=self.copy_all_to_ana__std
        self.AddToAnaPushButton.setVisible(False)
        self.openmessage='select folder containing all files for data import'
    
    def xrds_profile_withq(self):
        self.xrds_profile()
        self.mod_smp_afd_fcn=self.mod_smp_afd__xrds_withq
    
    def raiseerror(self):
        raiseerror

    def add_to_ana(self):
        self.add_to_ana_fcn()
        
    def create_udi(self, opttionsearchstr_comps=None, opttionsearchstr_xrd=None):
        if len(self.anadict)==0:
            return
        anak='ana__%d' %self.nextana
        anarunk='files_multi_run'
        self.nextana+=1
        self.anadict[anak]={}
        self.anadict[anak]['name']='Analysis__Create_UDI'
        self.anadict[anak]['technique']=self.datatype
        self.anadict[anak]['plate_ids']=self.plate_idstr
        self.anadict[anak][anarunk]={}
        ana__d=self.anadict[anak]
                                
        newfn='%s_%s.udi' %(anak, self.plate_idstr)
        ana__d=ana__d[anarunk]
        afd_udi={}
        #afd_udi['folderpath']=fold
        afd_udi['anak']=anak
        afd_udi['type']='misc_files'
        #afd_udi['fn']=fn
        afd_udi['fval']='ssrl_udi_file'
        afd_udi['anafn']=newfn
        afd_udi['copy_fcn']=self.copy_createudi
        if not afd_udi['type'] in ana__d.keys():
            ana__d[afd_udi['type']]={}
        ana__d[afd_udi['type']][afd_udi['anafn']]=afd_udi['fval']
        
        xrdanak_anname_options=[(k, self.anadict[k]['name']) for k in sort_dict_keys_by_counter(self.anadict, keystartswith='ana__') if True in ['pattern_files' in d.keys() for k2, d in self.anadict[k].iteritems() if isinstance(d, dict)]]
        xrdanaoptions=['-'.join(tup) for tup in xrdanak_anname_options]
        if not opttionsearchstr_xrd is None:
            xrdselectind=0
            for s in xrdanaoptions:
                if opttionsearchstr_xrd in s:
                    break
                xrdselectind+=1
            if xrdselectind==len(xrdanaoptions):
                print 'udi xrd search option not found'
                return
        elif len(xrdanaoptions)==1:
            xrdselectind=0
        else:
            xrdselectind=userselectcaller(self, options=xrdanaoptions, title='Select xrd data source for udi',  cancelallowed=True)
            if xrdselectind is None:
                return
        
        anak_xrd, analysis_name__patterns=xrdanak_anname_options[xrdselectind]
        
        fval=[d['pattern_files'].values()[0] for k2, d in self.anadict[anak_xrd].iteritems() if isinstance(d, dict) and 'pattern_files' in d.keys()][0]
        
        qkey, intkey=fval.split(';')[1].split(',')[:2]
        
        udi_dict={'ana_file_type':'pattern_files', 'anak':anak_xrd, 'q_key':qkey, 'intensity_key':intkey, 'pattern_source_analysis_name':analysis_name__patterns}
        
        kl=[k for k in sort_dict_keys_by_counter(self.anadict, keystartswith='ana__')  if 'files_multi_run' in self.anadict[k].keys() and 'fom_files' in self.anadict[k]['files_multi_run'].keys()]
        anak_anname_options=[(k, csvfn) for k in kl for csvfn, csvfval in self.anadict[k]['files_multi_run']['fom_files'].items() if csvfval.count('.AtFrac')>1]
        anaoptions=['-'.join(tup) for tup in anak_anname_options]
        if len(anaoptions)==0:
            print 'no comp data found'
            return
        if not opttionsearchstr_comps is None:
            selectind=0
            for s in anaoptions:
                if opttionsearchstr_comps in s:
                    break
                selectind+=1
            if selectind==len(anaoptions):
                print 'udi comp search option not found'
                return
        else:
            #anaoptions+=['platemap']
            selectind=userselectcaller(self, options=anaoptions, title='Select composition source for udi',  cancelallowed=True)
            if selectind is None:
                return
#            if selectind==len(anaoptions)-1:
#                #platemp
#                selectind=None
            #start programming ability to import comps from aux ana but thsi should be doen elsewhere
#            elif selectind==len(anaoptions)-2:
#                p=selectexpanafile(self, exp=False, markstr='Select .ana/.pck to import, or .zip file')
#                if len(p)==0:
#                    return
#                auxanadict=readana(p, stringvalues=True, erroruifcn=None)
#                auxanadict=[for k in sort_dict_keys_by_counter(auxanadict, keystartswith='ana__') if 'files_multi_run' in auxanadict[k].keys() and 'fom_files' in auxanadict[k]['files_multi_run'].keys()]
#                fomd, csvheaderdict=readcsvdict(p, filed, returnheaderdict=True, zipclass=anazipclass)
                
        anak_comps, csvfn_comps=anak_anname_options[selectind]
        udi_dict['anak_comps']=anak_comps
        udi_dict['fom_file_comps']=csvfn_comps
        udi_dict['fomname_split_comps']='.AtFrac'
        afd_udi['udi_dict']=udi_dict
        
        self.anadict[anak]['parameters']={}
        for k, v in udi_dict.iteritems():
            self.anadict[anak]['parameters'][k]=v
        afd_udi['sample_no__ana_filedict_inds']=sorted([(afd['sample_no'], count, ) for count, afd in enumerate(self.ana_filedict_tocopy) if 'sample_no' in afd.keys() and afd['type']=='pattern_files'])
        #need to get compositions and xy data and only keep sample_no with this info
        self.ana_filedict_tocopy+=[afd_udi]
        self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')
    
    def copy_createudi(self, afd, anafolder):
        ananame=os.path.split(anafolder)[1].rpartition('.')[0]
        udi_dict=afd['udi_dict']
        udi_dict['ana_name']=ananame
        udi_dict['ana_name_comps']=ananame
        udi_dict['plate_id']=self.plate_idstr
        for k, v in udi_dict.iteritems():
            self.anadict[afd['anak']]['parameters'][k]=v
        anadict_with_filed=copy.deepcopy(self.anadict)
        convertfilekeystofiled(anadict_with_filed)
        create_udi_anas(os.path.join(anafolder, afd['anafn']), udi_dict, anadict=anadict_with_filed,anadict_comps=anadict_with_filed, anafolder=anafolder, anafolder_comps=anafolder)
    
    
    def copy_all_to_ana__ssrl(self, anatempfolder):

        finished_inds_ana_filedict_tocopy=[]
        h5f=self.maindatad['h5f']
        g=h5f[h5f.attrs['default_group']]
        gs=g['spec']
        gd=g['deposition']
        if 'selectROI' in gd.keys():
            gr=gd['selectROI']
        

        mainh5inds=[]
        for k, headline in zip(['qcounts_subbcknd', 'qcounts'], ['q.nm,intensity.counts', 'q.nm_processed,intensity.counts_processed']):#do qcounts last so this is the default for mainh5inds below
            q=g['xrd'][k].attrs['q']
        
            temptups=sorted([(afd['h5arrind'], afd['anafn'], afd['sample_no'], count) for count, afd in enumerate(self.ana_filedict_tocopy) if 'sample_no' in afd.keys() and 'h5dataset' in afd.keys() and afd['h5dataset']==k])
            if len(temptups)==0:
                continue
            mainh5inds=map(operator.itemgetter(0), temptups)
            fns=map(operator.itemgetter(1), temptups)
            mainsmps=map(operator.itemgetter(2), temptups)
            finished_inds_ana_filedict_tocopy+=map(operator.itemgetter(3), temptups)
            
            temptups=sorted([(afd['h5arrind'], afd['anafn'], count) for count, afd in enumerate(self.ana_filedict_tocopy) if (not 'sample_no' in afd.keys()) and 'h5dataset' in afd.keys() and afd['h5dataset']==k])
            nosmp_mainh5inds=map(operator.itemgetter(0), temptups)
            nosmp_fns=map(operator.itemgetter(1), temptups)
            finished_inds_ana_filedict_tocopy+=map(operator.itemgetter(2), temptups)
            
            qcountsarr=g['xrd'][k][:, :][mainh5inds+nosmp_mainh5inds]
            for fn, qc in zip(fns+nosmp_fns, qcountsarr):
                lines=[headline]
                lines+=['%.5e,%.5e' %t for t in zip(q, qc)]
                s='\n'.join(lines)
                with open(os.path.join(anatempfolder, fn), mode='w') as f:
                    f.write(s)
            
        
        templ=[(afd, count) for count, afd in enumerate(self.ana_filedict_tocopy) if 'roi_keys_to_copy' in afd.keys()]
        
        if len(mainh5inds)==0 or len(templ)!=1:
            h5f.close()
            return
        afd, ind=templ[0]
        finished_inds_ana_filedict_tocopy+=[ind]
        fom_columns=[mainsmps]
        fom_columns+=[[1]*len(mainsmps)]#runint
        fom_columns+=[[self.plate_idstr]*len(mainsmps)]
        fmtlist=['%d', '%d', '%s']
        fmtlist+=['%.4e']*len(afd['roi_keys_to_copy'])
        for sk in afd['roi_keys_to_copy']:
            fom_columns+=[gs[sk][:][mainh5inds]]
        comps=gr['compositions'][:, :][mainh5inds]
        fmtlist+=['%.3f']*comps.shape[1]
        for arr in comps.T:
            fom_columns+=[arr]
        
        self.anadict[afd['anak']]['files_multi_run'][afd['type']][afd['anafn']]=';'.join([afd['fval'].rpartition(';')[0], '%d' %len(mainsmps)])
        lines=[afd['headline']]
        fmstr=','.join(fmtlist)
        lines+=[fmstr %tup for tup in zip(*fom_columns)]
        s='\n'.join(lines)
        with open(os.path.join(anatempfolder, afd['anafn']), mode='w') as f:
            f.write(s)
        
        for anak in sort_dict_keys_by_counter(self.anadict, keystartswith='ana__'):
            if self.anadict[anak]['name']=='Analysis__SSRL_Integrate':
                self.anadict[anak]['parameters']={}
                for k, v in g['xrd'].attrs.items():
                    self.anadict[anak]['parameters'][k]=str(v)
            elif self.anadict[anak]['name']=='Analysis__SSRL_Process':
                self.anadict[anak]['parameters']={'method':'legacy spline-based baseline detection'}
        
        h5f.close()
        
        for count, afd in enumerate(self.ana_filedict_tocopy):
            if count in finished_inds_ana_filedict_tocopy:
                continue
            afd['copy_fcn'](afd, anatempfolder)

    def copy_all_to_ana__std(self, anatempfolder):
        for count, afd in enumerate(self.ana_filedict_tocopy):
            afd['copy_fcn'](afd, anatempfolder)
       
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
    
    def xrds_copy_xy_to_ana_convert_to_q(self, afd, anafolder):
        p=os.path.join(afd['folderpath'], afd['fn'])
        newp=os.path.join(anafolder, afd['anafn'])
        with open(p, mode='r') as f:
            lines=f.readlines()
        lines=[l.strip() for l in lines]
        lines[0]=afd['fval'].partition(';')[2].partition(';')[0]
        strtuplist=[l.split(' ') for l in lines[1:]]
        ttvals=numpy.array([myeval(tt) for tt, z in strtuplist])
        qvals=q_twotheta(ttvals)
        lines=[lines[0]]
        lines+=['%.3f,%s,%s' %(q, tt, z) for q, (tt, z) in zip(qvals, strtuplist)]
        s='\n'.join(lines)
        with open(newp, mode='w') as f:
            f.write(s)
    
    def evalsmpstr_afd(self, afd, smpstr):
        if not (smpstr is None or len(smpstr)==0 or smpstr=='0'):
            afd['sample_no']=myeval(smpstr)
            
    def mod_smp_afd__xrds(self, afd, anak, smpstr=None):                                
        newfn='%s_%s' %(anak, afd['fn'].replace('.xy', '.csv'))
        afd['anafn']=newfn
        afd['anak']=anak
        afd['copy_fcn']=self.xrds_copy_xy_to_ana
        self.evalsmpstr_afd(afd, smpstr)
        return [afd]
    
    def mod_smp_afd__xrds_withq(self, afd, anak, smpstr=None):
        newfn='%s_%s' %(anak, afd['fn'].replace('.xy', '.csv'))
        afd['anafn']=newfn
        afd['fval']=afd['fval'].replace('two_theta.deg,','q.nm,two_theta.deg,')
        afd['anak']=anak
        afd['copy_fcn']=self.xrds_copy_xy_to_ana_convert_to_q
        self.evalsmpstr_afd(afd, smpstr)
        return [afd]
        
    def mod_afd_fcn__std(self, afd, anak, smpstr=None):
        newfn='%s_%s' %(anak, afd['fn'])
        afd['anafn']=newfn
        afd['copy_fcn']=self.stdcopy_afd
        afd['anak']=anak
        self.evalsmpstr_afd(afd, smpstr)
        return [afd]
        
    def createfiledicts(self):
        self.inds_rcpdlist=self.runtreeclass.getindsofchecktoplevelitems()
        self.ana_filedict_tocopy=[]
        self.all_rcp_dict={}
        self.expdict={}
        self.expdict['experiment_type']=self.datatype
        self.expdict['exp_version']='3'
        self.expdict['description']='%d %s runs on plate_id %s' %(len(self.inds_rcpdlist), self.datatype, self.plate_idstr)
        self.expdict['created_by']=self.datatype
        self.expdict['access']='hte'

        self.anadict={}
        self.anadict['created_by']=self.datatype
        self.anadict['access']='hte'
        self.anadict['analysis_type']=self.datatype
        
        rcplab=str(self.rcplabelLineEdit.text())
        rcplab=filterchars(rcplab, valid_chars = "-%s" % (string.ascii_letters))
        if len(rcplab)==0:
            rcplab='extimport'
        self.rcpmainfoldname='_'.join([timestampname()[:8], rcplab, get_serial_plate_id(self.plate_idstr)])
        
        self.nextana=1
        anabool=int(self.AnaSaveComboBox.currentIndex())>0
        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpd=self.maindatad['rcpdlist'][ind_rcp]

            rcpdict={}
            rcpdict['experiment_type']=self.datatype
            rcpdict['technique_name']=self.datatype
            
            rcpdict['rcp_version']='2'
            if not self.pmidstr is None:
                rcpdict['screening_map_id']=self.pmidstr
            
            runk='run__%d' %(runcount+1)
            self.expdict[runk]={}
            exprund=self.expdict[runk]
            exprund['run_use']='data'
            exprund['plate_id']=self.plate_idstr
#            if not 'parameters' in rcpdict.keys():
#                rcpdict['parameters']={}
           
            rcpdict['plate_id']=self.plate_idstr
            exprund['rcp_file']=rcpd['name']+'.rcp'
            if 'machine_name' in rcpd['parameters']:
                rcpdict['computer_name']=rcpd['parameters']['machine_name']
            else:
                rcpdict['computer_name']=self.computernamedefault
            
            for k in ['name', 'parameters']:
                rcpdict[k]=rcpd[k]
                exprund[k]=rcpd[k]
            rcpdict['parameters']['plate_id']=self.plate_idstr
            exprund['run_path']=r'/%s/%s/%s/%s' %(self.datatype, rcpdict['computer_name'].lower(), self.rcpmainfoldname, rcpdict['name']+'.done')
            
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
                                    anak='ana__%d' %self.nextana
                                    self.nextana+=1
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
                                
                            modafdlist=self.mod_smp_afd_fcn(afd, anak, smpstr=smp)
                            for modafd in modafdlist:
                                antypek=modafd['type']
                                if not antypek in ana__d.keys():
                                    ana__d[antypek]={}
                                ana__d[antypek][modafd['anafn']]=modafd['fval']+smp#ana file val expected to have all other info included already
                                self.ana_filedict_tocopy+=[modafd]
            self.all_rcp_dict['rcp_file__%d' %(runcount+1)]=rcpdict
        if anabool:
            if 'multirun_ana_files' in self.maindatad.keys() and len(self.maindatad['multirun_ana_files'])>0:
                for an_name, anafiledlist in self.maindatad['multirun_ana_files'].iteritems():
                    ana__d=None
                    for afd in anafiledlist:
                        if ana__d is None:
                            anl=[k for k, v in self.anadict.iteritems() if k.startswith('ana__') and an_name==v['name']]
                            if len(anl)==0:
                                anak='ana__%d' %self.nextana
                                self.nextana+=1
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

                        modafdlist=self.mod_multi_afd_fcn(afd, anak)
                        for modafd in modafdlist:
                            antypek=modafd['type']
                            if not antypek in ana__d.keys():
                                ana__d[antypek]={}
                            ana__d[antypek][modafd['anafn']]=modafd['fval']
                            self.ana_filedict_tocopy+=[modafd]
                            
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
        afd={}
        afd['folderpath']=fold
        afd['type']='misc_files'
        afd['fn']=fn
        afd['fval']='xrds_user_import_file;'
        afd['anafn']=newfn
        afd['copy_fcn']=self.stdcopy_afd
        if not afd['type'] in d.keys():
            d[afd['type']]={}
        d[afd['type']][afd['anafn']]=afd['fval']
        
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

    def importfolder(self, p=None, plate_idstr=None, **kwargs):
        self.cleardata()
        self.profiledefintionfcns[self.ProfileComboBox.currentIndex()]()#defines the functions
        
        if p is None:
            p=mygetdir(parent=self, markstr=self.openmessage)
        if len(p)==0:
            return
        if plate_idstr is None:
            pid=self.get_plate_from_folder_path(p)
        else:
            pid=plate_idstr
        if pid is None:
            ans=userinputcaller(self, inputs=[('plate_id', str, '')], title='Enter plate_id',  cancelallowed=True)
            if ans is None or len(ans[0].strip())==0 or not ans[0].isdigit():
                return
            pid=ans[0]
        self.plate_idstr=pid

        self.maindatad=self.importfolderfcn(p, parent=self, **kwargs)
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
        ellist=getelements_plateidstr(self.plate_idstr)
        if ellist is None:
            self.rcplabelLineEdit.setText('')
        else:
            self.rcplabelLineEdit.setText(''.join(ellist))


    def get_plate_from_folder_path(self, p):
        foldn=os.path.split(p)[1]
        serialstr=foldn.partition('_')[0]
        if len(serialstr)<3 or not serialstr.isdigit():
            serialstr=foldn.rpartition('_')[2]
            if len(serialstr)<3 or not serialstr.isdigit():
                return None
        return serialstr[:-1]
    def openplatemap(self, plate_idstr=None):
        
        if plate_idstr is None:
            pmpath=mygetopenfile(parent=self, xpath=PLATEMAPFOLDERS[0], markstr='select platemap')
            if len(pmpath)==0:
                return None
            self.pmidstr=None
        else:
            pmpath, self.pmidstr=getplatemappath_plateid(plate_idstr, return_pmidstr=True)
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
        if len(self.inds_rcpdlist)==0:
            return
        dropfolder=tryprependpath(EXPERIMENT_DROP_FOLDERS, os.path.join(self.datatype, 'drop'))
        if dropfolder is None:
            messageDialog(self, 'Aborting SAVE because cannot find drop folder').exec_()
            return
        
        rcpmainfolder=os.path.join(dropfolder, self.rcpmainfoldname)

        
        if os.path.isdir(rcpmainfolder):
            messageDialog(self, 'Aborting SAVE because %s folder exists' %rcpmainfolder).exec_()
            return
        os.mkdir(rcpmainfolder)
        
        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpfiled=self.all_rcp_dict['rcp_file__%d' %(runcount+1)]
            rcpname=rcpfiled['name']+'.done'
            rcpfolder=os.path.join(rcpmainfolder, rcpname)
            if os.path.isdir(rcpfolder):
                messageDialog(self, 'Aborting SAVE because at least 1 rcp drop folder exists').exec_()
                return

        for runcount, ind_rcp in enumerate(self.inds_rcpdlist):
            rcpfiled=self.all_rcp_dict['rcp_file__%d' %(runcount+1)]
            rcpname=rcpfiled['name']+'.done'
            rcpfolder=os.path.join(rcpmainfolder, rcpname)
            os.mkdir(rcpfolder)

            rcpd=self.maindatad['rcpdlist'][ind_rcp]
            for fd in rcpd['file_dlist']:
                shutil.copy(os.path.join(fd['folderpath'], fd['fn']), os.path.join(rcpfolder, fd['fn']))

            rcppath=os.path.join(rcpfolder, rcpname.replace('.done', '.rcp'))
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
            
            anatempfolder=getanadefaultfolder()
            self.anadict['name']=os.path.split(anatempfolder)[1].rpartition('.')[0]
            self.copy_all_to_ana_fcn(anatempfolder)

            self.AnaTreeWidgetFcns.filltree(self.anadict, startkey='ana_version', laststartswith='ana__')
            anafilestr=self.AnaTreeWidgetFcns.createtxt()
            anafolder=saveana_tempfolder(anafilestr, anatempfolder, anadict=None, analysis_type='temp' if saveopt==1 else self.datatype, rundone='.done' if saveopt==3 else '.run')


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
        critdist2=float(self.critdistSpinBox.value())**2

        xyplotinfo=[]
        for count, rcpd in enumerate(self.maindatad['rcpdlist']):
            for fd in rcpd['file_dlist']:
                if 'xyarr' in fd.keys():
                    xv, yv=xypmall.pop(0)
                    if numpy.isnan(xv) or numpy.isnan(yv):
                        continue
                    pmi=numpy.argmin((pmx-xv)**2+(pmy-yv)**2)
                    if ((pmx[pmi]-xv)**2+(pmy[pmi]-yv)**2)>critdist2:
                        xyplotinfo+=[(xv, yv, None, None, '')]
                        continue
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
            xl+=[xv]
            yl+=[yv]
            if xp is None:
                ax.plot(xv, yv, 'rx')
                continue
            ax.plot(xv, yv, 'ko')
            ax.plot([xv, xp], [yv, yp], 'r-')
            ax.text(xv, yv, s, ha='center', va='bottom')
            
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
        if len(d)==0:
            return
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
