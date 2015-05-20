import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab
import pickle
from fcns_math import *
from fcns_io import *
from fcns_ui import *
from CalcFOMForm import Ui_CalcFOMDialog
from fcns_compplots import *
matplotlib.rcParams['backend.qt4'] = 'PyQt4'

os.chdir('AnalysisFunctions')
from CA_CP_basics import *

AnalysisClasses=[Analysis__CA_Ifin(), Analysis__CA_Iave(), Analysis__CA_Iphoto()]

class calcfomDialog(QDialog, Ui_CalcFOMDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(calcfomDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.parent=parent
#        self.echem30=echem30axesWidget()
#        self.echem30.show()
        self.plotillumkey=None

        self.dbdatasource=0

        self.techniquedictlist=[]

        self.plotwsetup()
        button_fcn=[\
        (self.BatchPushButton, self.runbatchprocess), \
        (self.ImportExpPushButton, self.importexp), \
        (self.GrabExpPushButton, self.grabexp), \
        (self.EditAnalysisParamsPushButton, self.editanalysisparams), \
        (self.AnalyzeDataPushButton, self.analyzedata), \
        (self.ViewResultPushButton, self.viewresult), \
        (self.EditDfltVisPushButton, self.editvisparams), \
        (self.SaveAnaPushButton, self.saveana), \
        (self.ClearAnalysisPushButton, self.clearanalysis), \
        (self.ImportAnalysisParamsPushButton, self.importanalysisparams), \

        ]
        #(self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            QObject.connect(button, SIGNAL("pressed()"), fcn)
        
        self.runcheckboxlist=[\
        self.RunCheckBox_0, self.RunCheckBox_1, self.RunCheckBox_2, \
        self.RunCheckBox_3, self.RunCheckBox_4, self.RunCheckBox_5, \
        self.RunCheckBox_6, self.RunCheckBox_7]
        for cb in self.runcheckboxlist:
            QObject.connect(cb, SIGNAL("toggled(bool)"), self.filltechtyperadiobuttons)
        
        QObject.connect(self.ExpRunUseComboBox,SIGNAL("activated(QString)"),self.fillruncheckboxes)
        
        #QObject.connect(self.TechTypeButtonGroup,SIGNAL("buttonClicked(QAbstractButton)"),self.fillanalysistypes)
        self.TechTypeButtonGroup.buttonClicked[QAbstractButton].connect(self.fillanalysistypes)
        
        QObject.connect(self.AnalysisNamesComboBox,SIGNAL("activated(QString)"),self.getactiveanalysisclass)
        
        QObject.connect(self.AnaTreeWidget, SIGNAL('itemDoubleClicked(QTreeWidgetItem*, int)'), self.edittreeitem)
        
        self.paramsdict_le_dflt=dict([\
         ('access', [self.AccessLineEdit, 'hte']), \
         ('name', [self.AnaNameLineEdit, 'none']), \
         ('ana_type', [self.AnaTypeLineEdit, 'eche']), \
         ('created_by', [self.UserNameLineEdit, 'eche']), \
         ('description', [self.AnaDescLineEdit, 'null']), \
        ])
        
        self.tempanafolder=getanadefaultfolder(erroruifcn=lambda s:mygetdir(parent=self, markstr='select ANA default folder'))
        self.AnaTreeWidgetFcns=treeclass_anadict(self.AnaTreeWidget)
        self.clearanalysis()

    def edittreeitem(self, item, column):
        self.editparams(self.AnaTreeWidget, item=item, column=column)
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
        warningbool = warningbool or True in [ws in parentstr or ws in k for ws in ['ana__', 'parameters', 'files_']]
        
        
        if warningbool:
            idialog=messageDialog(self, 'THIS IS CONSIDERED A READ-ONLY PARAMETER.\nYOU SHOULD PROBABLY "Cancel"')
            if not idialog.exec_():
                return
        item.setText(column,''.join([k, ans]))
        
    def importexp(self):
        #TODO: define default path
        #p='exp/sampleexp_uvis.dat'
        p=mygetopenfile(self, xpath=os.path.join(os.getcwd(), 'experiment'), markstr='Select .pck or .exp EXP file', filename='.pck' )
        temp=readexpasdict(p, includerawdata=False)
        if temp is None:
            print 'Problem opening EXP'
            return
        self.expfiledict=temp
        self.expfolder=os.path.split(p)[0]
        
        self.paramsdict_le_dflt['ana_type'][1]=self.expfiledict['exp_type']
        self.paramsdict_le_dflt['created_by'][1]=self.expfiledict['exp_type']

        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            if k in ['ana_type', 'created_by']:
                le.setText(dfltstr)
                
        self.fillexpoptions()
    
    def fillexpoptions(self):
        self.clearexp()
        
        self.runk_use=[(k, v['run_use']) for k, v in self.expfiledict.iteritems() if k.startswith('run__')]
        self.uselist=list(set(map(operator.itemgetter(1), self.runk_use)))
        if 'data' in self.uselist:
            temp=self.uselist.pop(self.uselist.index('data'))
            self.uselist=[temp]+self.uselist
        
        for i, k in enumerate(self.uselist):
            self.ExpRunUseComboBox.insertItem(i, k)

        self.ExpRunUseComboBox.setCurrentIndex(0)
        
        self.fillruncheckboxes()
    
    def fillruncheckboxes(self):
        self.usek=str(self.ExpRunUseComboBox.currentText())
        runklist=[runk for runk, usek in self.runk_use if usek==self.usek]
        for cb, runk in zip(self.runcheckboxlist, runklist):
            s=','.join([runk, self.expfiledict[runk]['name']])
            cb.setText(s)
            cb.setChecked(True)
        self.filltechtyperadiobuttons()
    
    def filltechtyperadiobuttons(self):
        qlist=self.TechTypeButtonGroup.buttons()
        numbuttons=len(qlist)
        for button in qlist:
            button.setText('')
            button.setToolTip('')
            
        self.selectrunklist=[str(cb.text()).partition(',')[0] for cb in self.runcheckboxlist if cb.isChecked()]
        self.selectrunklist=[s for s in self.selectrunklist if len(s)>0]
        runk_techk=[(runk, techk)
        for runk in self.selectrunklist \
        for techk in self.expfiledict[runk].keys() \
        if techk.startswith('files_technique__')]
        
        self.techk_typek=list(set([(techk.partition('files_technique__')[2], typek) \
        for runk, techk in runk_techk \
        for typek in self.expfiledict[runk][techk].keys()]))
        
        numfiles=[\
            numpy.array([len(self.expfiledict[runk]['files_technique__'+techk][typek].keys()) \
                for runk in self.selectrunklist \
                if 'files_technique__'+techk in self.expfiledict[runk].keys() and typek in self.expfiledict[runk]['files_technique__'+techk].keys()]).sum(dtype='int32')
            for techk, typek in self.techk_typek]
        
        count=0
        for nfiles, techk_typek in zip(numfiles, self.techk_typek):
            if count==numbuttons:
                break
            button=qlist[count]
            
            s=','.join(techk_typek)
            button.setText(s)
            button.setToolTip('%d files' %(nfiles))
            if count==0:
                button.setChecked(True)
                self.fillanalysistypes(button)
            count+=1
        
    
    def fillanalysistypes(self, button):
        if button is None:
            button=self.TechTypeButtonGroup.buttons()[0]
            button.setChecked(True)
        s=str(button.text())
        self.techk, garb, self.typek=s.partition(',')
        nfiles_classes=[len(c.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist)) for i, c in enumerate(AnalysisClasses)]
        self.AnalysisClassInds=[i for i, nf in enumerate(nfiles_classes) if nf>0]
        self.AnalysisNamesComboBox.clear()
        self.AnalysisNamesComboBox.insertItem(0, '')
        for count, i in enumerate(self.AnalysisClassInds):
            self.AnalysisNamesComboBox.insertItem(count+1, AnalysisClasses[i].analysis_name+('(%d)' %nfiles_classes[i]))
            self.AnalysisNamesComboBox.setCurrentIndex(1)
        self.getactiveanalysisclass()
    
    def getactiveanalysisclass(self):
        selind=int(self.AnalysisNamesComboBox.currentIndex())
        if selind==0:
            self.analysisclass=None
            return
        self.analysisclass=AnalysisClasses[self.AnalysisClassInds[selind-1]]
    
    def clearexp(self):
        self.ExpRunUseComboBox.clear()
        for cbl in [self.runcheckboxlist, self.TechTypeButtonGroup.buttons()]:
            for cb in cbl:
                cb.setText('')
                cb.setToolTip('')
                cb.setChecked(False)

    def runbatchprocess(self):
        return

    def grabexp(self):
        return
    def editanalysisparams(self):
        if self.analysisclass is None:
            return
        inputs=[(k, type(v), (isinstance(v, str) and (v,) or (`v`,))[0]) for k, v in self.analysisclass.params.iteritems()]
        if len(inputs)==0:
            return
        ans, changedbool=userinputcaller(self, inputs=inputs, title='Enter Calculation Parameters', returnchangedbool=True)
        somethingchanged=False
        for (k, tp, v), newv, chb in zip(inputs, ans, changedbool):
            if chb:
                self.analysisclass.params[k]=newv
                somethingchanged=True
        if somethingchanged:#soem analysis classes have different files applicable depending on user-enter parameters so update here but don't bother deleting if numfiles goes to 0
            selind=int(self.AnalysisNamesComboBox.currentIndex())
            nfiles=len(self.analysisclass.getapplicablefilenames(self.expfiledict, self.usek, self.techk, self.typek, runklist=self.selectrunklist))
            self.AnalysisNamesComboBox.setItemText(selind, self.analysisclass.analysis_name+('(%d)' %nfiles))
    def analyzedata(self):
        if self.analysisclass is None:
            return
        #rawd=readbinaryarrasdict(keys)
        #expdatfolder=os.path.join(self.expfolder, 'raw_binary')
        expdatfolder=self.expfolder
        
        kfcn=lambda i:'ana__%d' %i
        i=0
        while kfcn(i) in self.anadict.keys():
            i+=1
        anak=kfcn(i)
        #try:
        self.analysisclass.perform(self.tempanafolder, expdatfolder=expdatfolder, anak=anak)
        #except: return
        self.anadict[anak]={}
        self.activeana=self.anadict[anak]
        
        self.activeana['name']=self.analysisclass.analysis_name
        self.activeana['version']=self.analysisclass.analysis_version
        self.activeana['description']=self.analysisclass.description
        
        le, dflt=self.paramsdict_le_dflt['description']
        s=str(le.text()).strip()
        if len(s)==0 or 'null' in s:
            newdflt=self.activeana['description']
        else:
            newdflt=','.join([s, self.activeana['description']])
        if s==dflt:            
            le.setText(newdflt)
        self.paramsdict_le_dflt['description'][1]=newdflt
        
        self.activeana['parameters']={}
        for k, v in self.analysisclass.params.iteritems():
            self.activeana['parameters'][k]=str(v)
        if len(self.analysisclass.interfiledict.keys())>0:
            self.activeana['files_technique__'+self.techk]=copy.copy(self.analysisclass.interfiledict)
        if len(self.analysisclass.fomfiledict.keys())>0:
            self.activeana['files_fom_technique__'+self.techk]=copy.copy(self.analysisclass.fomfiledict)
        
        self.fomdlist=self.analysisclass.fomdlist
        self.updateana()
        #self.plot()
        
        
    def updateana(self):
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            s=str(le.text()).strip()
            if len(s)==0:
                s=dfltstr
            self.anadict[k]=s
        
        self.AnaTreeWidgetFcns.filltree(self.anadict)
        
    def viewresult(self):
        return
    def editvisparams(self):
        return
    def savefom(self):
        return
    def clearanalysis(self):
        self.analysisclass=None
        self.anadict={}
        self.anadict['ana_version']='3'
        
        self.paramsdict_le_dflt['description'][1]='null'
        
        self.AnaTreeWidget.clear()
        
        for fn in os.listdir(self.tempanafolder):
            os.remove(os.path.join(self.tempanafolder, fn))
        
        
    def importanalysisparams(self):
        return


    def saveana(self):
        self.anafilestr=self.AnaTreeWidgetFcns.createtxt()
        if not 'ana_version' in self.anafilestr:
            return
        saveana_tempfolder(self.anafilestr, self.tempanafolder, erroruifcn=\
            lambda s:mygetdir(parent=self, xpath="%s" % os.getcwd(),markstr='Error: %s, select folder for saving ANA'))
        self.clearanalysis()

      
#    def plot(self):
#        self.statusLineEdit.setText('plotting')
#        s=25
#
#        self.plotw_comp.axes.cla()
#        self.plotw_quat.axes.cla()
#        self.plotw_plate.axes.cla()
#        self.plotw_aux.axes.cla()
#        self.cbax_quat.cla()
#        self.cbax_tern.cla()
#        self.cbax_plate.cla()
#
#        if len(self.techniquedictlist)==0:
#            self.statusLineEdit.setText('idle')
#            return
##        m=self.plotw_comp.axes.scatter(self.detx, self.detz, c=self.dsp, s=s, edgecolors='none')
##        cb=self.plotw_comp.fig.colorbar(m, cax=self.cbax_tern)
##        cb.set_label('d-spacing (nm)')
#
#        getarr=lambda k:getarrfromkey(self.techniquedictlist, k)
#        fom=getarr('FOM')
#        print fom[:10]
#        inds=numpy.where(numpy.logical_not(numpy.isnan(fom)))[0]
#        if len(inds)==0:
#            print 'ABORTING PLOTTING BECAUSE ALL FOMs ARE NaN'
#            return
#        fom=fom[inds]
#        print fom[:10]
#        sample=getarr('Sample')[inds]
#        comps=getarr('compositions')[inds]
#        x=getarr('x')[inds]
#        y=getarr('y')[inds]
#
#        if self.revcmapCheckBox.isChecked():
#            cmap=cm.jet_r
#        else:
#            cmap=cm.jet
#
#        clip=True
#        skipoutofrange=[False, False]
#        self.vmin=fom.min()
#        self.vmax=fom.max()
#        vstr=str(self.vminmaxLineEdit.text()).strip()
#        if ',' in vstr:
#            a, b, c=vstr.partition(',')
#            try:
#                a=myeval(a.strip())
#                c=myeval(c.strip())
#                self.vmin=a
#                self.vmax=c
#                for count, (fcn, le) in enumerate(zip([cmap.set_under, cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
#                    vstr=str(le.text()).strip()
#                    vstr=vstr.replace('"', '').replace("'", "")
#                    print '^^^', vstr, 'none' in vstr or 'None' in vstr
#                    if 'none' in vstr or 'None' in vstr:
#                        skipoutofrange[count]=True
#                        continue
#                    if len(vstr)==0:
#                        continue
#                    c=col_string(vstr)
#                    try:
#                        fcn(c)
#                        clip=False
#                    except:
#                        print 'color entry not understood:', vstr
#
#            except:
#                pass
#
#        norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
#        print 'fom min, max, mean, std:', fom.min(), fom.max(), fom.mean(), fom.std()
#
#        print 'skipoutofrange', skipoutofrange
#        print len(fom)
#        if skipoutofrange[0]:
#            inds=numpy.where(fom>=self.vmin)
#            fom=fom[inds]
#            comps=comps[inds]
#            x=x[inds]
#            y=y[inds]
#        print len(fom)
#        if skipoutofrange[1]:
#            inds=numpy.where(fom<=self.vmax)
#            fom=fom[inds]
#            comps=comps[inds]
#            x=x[inds]
#            y=y[inds]
#        print len(fom)
#
#
#        if numpy.any(fom>self.vmax):
#            if numpy.any(fom<self.vmin):
#                extend='both'
#            else:
#                extend='max'
#        elif numpy.any(fom<self.vmin):
#            extend='min'
#        else:
#            extend='neither'
#        print 'extend ', extend
#        m=self.plotw_plate.axes.scatter(x, y, c=fom, s=s, marker='s', cmap=cmap, norm=norm)
#        if x.max()-x.min()<2. or y.max()-y.min()<2.:
#            self.plotw_plate.axes.set_xlim(x.min()-1, x.max()+1)
#            self.plotw_plate.axes.set_ylim(y.min()-1, y.max()+1)
#        else:
#            self.plotw_plate.axes.set_aspect(1.)
#
#        cb=self.plotw_plate.fig.colorbar(m, cax=self.cbax_plate, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
#        #cb.set_label('|Q| (1/nm)')
#
#
#        comps=numpy.array([c[:4]/c[:4].sum() for c in comps])
#        i=self.ternskipComboBox.currentIndex()
#        inds=[j for j in range(4) if j!=i][:3]
#        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
#        reordercomps=comps[:, inds+[i]]
#        self.ellabels=self.techniquedictlist[0]['elements']
#        reorderlabels=[self.ellabels[j] for j in inds+[i]]
#
#
#        quat=QuaternaryPlot(self.plotw_quat.axes, ellabels=self.ellabels, offset=0)
#        quat.label()
#        quat.scatter(comps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
#        cb=self.plotw_quat.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
#
#        fomlabel=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
#        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel)])
#
#        tern=TernaryPlot(self.plotw_comp.axes, ellabels=reorderlabels[:3], offset=0)
#        tern.label()
#        tern.scatter(terncomps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
#        cb=self.plotw_comp.fig.colorbar(tern.mappable, cax=self.cbax_tern, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
#
#        self.plotw_aux.axes.plot(fom, 'g.-')
#        self.plotw_aux.axes.set_xlabel('sorted by experiment time')
#        self.plotw_aux.axes.set_ylabel('FOM')
#        autotickformat(self.plotw_aux.axes, x=0, y=1)
#
#        self.plotw_quat.axes.mouse_init()
#        self.plotw_quat.axes.set_axis_off()
#        self.plotw_comp.fig.canvas.draw()
#        self.plotw_quat.fig.canvas.draw()
#        self.plotw_plate.fig.canvas.draw()
#        self.plotw_aux.fig.canvas.draw()
#
#        self.selectind=-1
#        self.plotselect()
#        self.statusLineEdit.setText('idle')
#
#    def stackedtern10window(self):
#        d=self.stackedternplotdict
#        self.echem10=echem10axesWidget(parent=self.parent, ellabels=d['ellabels'])
#        self.echem10.plot(d, cb=True)
#
#        #scatter_10axes(d['comps'], d['fom'], self.echem10.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
#        self.echem10.exec_()
#
#    def stackedtern100window(self):
#        d=self.stackedternplotdict
#        self.echem100=echem100axesWidget(parent=None, ellabels=d['ellabels'])
#        self.echem100.plot(d, cb=True)
#
#        #scatter_30axes(d['comps'], d['fom'], self.echem30.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
#        #self.echem30.show()
#        self.echem100.exec_()
#
#    def stackedtern30window(self):
#        d=self.stackedternplotdict
#        self.echem30=echem30axesWidget(parent=None, ellabels=d['ellabels'])
#        self.echem30.plot(d, cb=True)
#
#        #scatter_30axes(d['comps'], d['fom'], self.echem30.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
#        #self.echem30.show()
#        self.echem30.exec_()
#
#    def stackedtern20window(self):
#        d=self.stackedternplotdict
#        self.echem20=echem20axesWidget(parent=None, ellabels=d['ellabels'])
#        self.echem20.plot(d, cb=True)
#        self.echem20.exec_()
#
#    def tern4window(self):
#        d=self.stackedternplotdict
#        self.echem4=echem4axesWidget(parent=None, ellabels=d['ellabels'])
#        self.echem4.plot(d, cb=True)
#        self.echem4.exec_()
#
#    def binlineswindow(self):
#        d=self.stackedternplotdict
#        self.echembin=echembinWidget(parent=None, ellabels=d['ellabels'])
#        self.echembin.plot(d, cb=True)
#        self.echembin.exec_()
#
#    def plotselect(self):
#        overlaybool=self.overlayselectCheckBox.isChecked()
#        if not overlaybool:
#            self.plotw_select.axes.cla()
#        d=self.techniquedictlist[self.selectind]
#
#        xk=str(self.xplotchoiceComboBox.currentText())
#        yk=str(self.yplotchoiceComboBox.currentText())
#
#        xshift=0.
#        xmult=1.
#        yshift=0.
#        ymult=1.
#        if '-E0' in xk:
#            xshift=-1.*self.E0SpinBox.value()
#            xk=xk.replace('-E0', '')
#        if '*Is' in xk:
#            xmult=self.IsSpinBox.value()
#            xk=xk.replace('*Is', '')
#        if '-E0' in yk:
#            yshift=-1.*self.E0SpinBox.value()
#            yk=yk.replace('-E0', '')
#        if '*Is' in yk:
#            ymult=self.IsSpinBox.value()
#            yk=yk.replace('*Is', '')
#
#        if not xk in d.keys():
#            print 'cannot plot the selected x-y graph because %s not found' %xk
#            return
#        if not yk in d.keys():
#            print 'cannot plot the selected x-y graph because %s not found' %yk
#            return
#        x=d[xk]*xmult+xshift
#        y=d[yk]*ymult+yshift
#        lab=''.join(['%s%d' %(el, c*100.) for el, c in zip(d['elements'], d['compositions'])])+'\n'
#        if 'FOM' in d.keys():
#            lab+='%d,%.2e' %(d['Sample'], d['FOM'])
#        else:
#            lab+='%d' %d['Sample']
#        self.plotw_select.axes.plot(x, y, '.-', label=lab)
#
#        autotickformat(self.plotw_select.axes, x=0, y=1)
#
#        if (not self.plotillumkey is None) and self.plotillumkey in d.keys() and not overlaybool:
#            illuminds=numpy.where(d[self.plotillumkey])[0]
#            self.plotw_select.axes.plot(x[illuminds], y[illuminds], 'y.')
#        self.plotw_select.axes.set_xlabel(xk)
#        self.plotw_select.axes.set_ylabel(yk)
#        legtext=unicode(self.legendselectLineEdit.text())
#        if len(legtext)>0:
#            legloc=myeval(legtext)
#            if isinstance(legloc, int) and legloc>=0:
#                self.plotw_select.axes.legend(loc=legloc).draggable()
#        self.plotw_select.fig.canvas.draw()
#        t=d['mtime']-2082844800.
#        print '^^^^^^^^', t
#        if not isinstance(t, str):
#            try:
#                t=time.ctime(t)
#            except:
#                t='error'
#        print t
#        self.daqtimeLineEdit.setText(t)
#
#    def plateclickprocess(self, coords_button):
#        if len(self.techniquedictlist)==0:
#            return
#        critdist=3.
#        xc, yc, button=coords_button
#        x=getarrfromkey(self.techniquedictlist, 'x')
#        y=getarrfromkey(self.techniquedictlist, 'y')
#        dist=((x-xc)**2+(y-yc)**2)**.5
#        if min(dist)<critdist:
#            self.selectind=numpy.argmin(dist)
#            self.plotselect()
#        if button==3:
#            self.addtoselectsamples([self.techniquedictlist[self.selectind]['Sample']])
#    def selectbelow(self):
#        try:
#            vmin, vmax=(self.vmin, self.vmax)
#        except:
#            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
#        idlist=[]
#        for d in self.techniquedictlist:
#            if d['FOM']<vmin:
#                idlist+=[d['Sample']]
#        if len(idlist)>0:
#            self.addtoselectsamples(idlist)
#
    def plotwsetup(self):
        self.plotw_select=plotwidget(self)
        self.plotw_select.setGeometry(QRect(670, 10, 461, 271))
        self.plotw_select.axes.set_xlabel('')
        self.plotw_select.axes.set_ylabel('')

        self.plotw_plate=plotwidget(self)
        self.plotw_plate.setGeometry(QRect(570, 530, 561, 341))
        self.plotw_plate.axes.set_aspect(1)

#        self.plotw_comp=plotwidget(self)
#        self.plotw_comp.setGeometry(QRect(570, 530, 561, 291))
#
#
#        self.plotw_quat=plotwidget(self, projection3d=True)
#        self.plotw_quat.setGeometry(QRect(570, 530, 561, 291))
#        self.plotw_quat.hide()


        self.plotw_aux=plotwidget(self)
        self.plotw_aux.setGeometry(QRect(670, 280, 461, 251))


        axrect=[0.82, 0.1, 0.04, 0.8]

        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)

#        self.plotw_comp.fig.subplots_adjust(left=0, right=axrect[0]-.01)
#        self.cbax_tern=self.plotw_comp.fig.add_axes(axrect)
#
#        self.plotw_quat.fig.subplots_adjust(left=0, right=axrect[0]-.01)
#        self.cbax_quat=self.plotw_quat.fig.add_axes(axrect)

        self.plotw_select.fig.subplots_adjust(left=.2)
        self.plotw_aux.fig.subplots_adjust(left=.2)


class treeclass_anadict():
    def __init__(self, tree):
        self.treeWidget=tree
        self.treeWidget.clear()
        
        
    def filltree(self, d, startkey='ana_version', laststartswith='ana__'):
        self.treeWidget.clear()
        
        
        mainitem=QTreeWidgetItem([': '.join([startkey, d[startkey]])], 0)
        self.treeWidget.addTopLevelItem(mainitem)
        self.treeWidget.setCurrentItem(mainitem)
        
        for k, v in d.iteritems():
            if k==startkey or k.startswith(laststartswith):
                continue
            if isinstance(v, dict):
                mainitem=QTreeWidgetItem([k+':'], 0)
                self.nestedfill(v, mainitem)
            else:
                mainitem=QTreeWidgetItem([': '.join([k, str(v)])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            
            mainitem.setExpanded(False)
        anakl=sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in anakl:
            mainitem=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
    def nestedfill(self, d, parentitem, laststartswith='files_'):
        for k, v in d.iteritems():
            if isinstance(v, dict):
                continue
            item=QTreeWidgetItem([': '.join([k, str(v)])], 0)
            parentitem.addChild(item)
        for k, v in d.iteritems():
            if k.startswith(laststartswith) or not isinstance(v, dict):
                continue
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(v, item)
            parentitem.addChild(item)
        for k, v in d.iteritems():
            if not k.startswith(laststartswith) or not isinstance(v, dict):
                continue
            item=QTreeWidgetItem([k+':'], 0)
            self.nestedfill(v, item)
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
            self.calcui=calcfomDialog(self, title='Calculate FOM from EXP', **kwargs)
            if execute:
                self.calcui.exec_()
    os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
