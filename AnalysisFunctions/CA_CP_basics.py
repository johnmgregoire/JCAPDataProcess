import numpy, copy
from fcns_math import *
from fcns_io import *
from csvfilewriter import createcsvfilstr
from Analysis_Master import *

class Analysis__CA_Ifin(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_version=1
        self.dfltparams={}
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__CA_Ifin'
        self.requiredkeys=['I(A)']
        self.iterkeys=[]
        self.fomnames=['I(A)_fin']
    
    def fomtuplist_dataarr(self, dataarr):
        return [('I(A)_fin', dataarr[0][-1])]
        
class Analysis__CA_Iave(Analysis_Master_nointer):
    def __init__(self):
        self.analysis_version='1'
        self.dfltparams=dict([('duration_s', 2.), ('num_std_dev_outlier', 2.), ('num_pts_outlier_window', 999999), ('from_end', True)])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__CA_Iave'
        self.requiredkeys=['I(A)', 't(s)']
        self.iterkeys=[]
        self.fomnames=['I(A)_ave']

    def fomtuplist_dataarr(self, dataarr):
        x, t=dataarr
        if self.params['from_end']:
            x=x[::-1]
            t=t[::-1]
        x=x[numpy.abs(t-t[0])<self.params['duration_s']]
        x=removeoutliers_meanstd(x, self.params['num_pts_outlier_window']//2, self.params['num_std_dev_outlier'])
        return [('I(A)_ave', x.mean())]

class Analysis__CA_Iphoto(Analysis_Master_inter):
    def __init__(self):
        self.analysis_version='1'
        self.dfltparams=dict([\
  ('frac_illum_segment_start', 0.4), ('frac_illum_segment_end', 0.95), \
  ('frac_dark_segment_start', 0.4), ('frac_dark_segment_end', 0.95), \
  ('illum_key', 'Toggle'), ('illum_time_shift_s', 0.), ('illum_threshold', 0.5), \
  ('illum_invert', 0), ('num_illum_cycles', 2), ('from_end', True)\
                                       ])
        self.params=copy.copy(self.dfltparams)
        self.analysis_name='Analysis__CA_Iphoto'
        self.requiredkeys=['I(A)', 'Ewe(V)', 't(s)', 'Toggle']#0th is array whose photoresponse is being calculate, -1th is the Illum signal, and the rest get processed along the way

        self.fomnames=['I(A)_photo']
    #this is the default fcn but with requiredkeys changed to relfect user-entered illum key
    def getapplicablefilenames(self, expfiledict, usek, techk, typek, runklist=None):
        self.requiredkeys[-1]=self.params['illum_key']
        self.fn_nkeys_reqkeyinds, self.filenames=stdgetapplicablefilenames(expfiledict, usek, techk, typek, runklist=runklist, requiredkeys=self.requiredkeys)
        self.description='%s on %s' %(','.join(self.fomnames), techk)
        return self.filenames
    def fomtuplist_rawlend_interlend(self, dataarr):

        d=dict([(k, v) for k, v in zip(self.requiredkeys, dataarr)])
        ikey=self.params['illum_key']
        tshift=self.params['illum_time_shift_s']
        interdict={}
        if tshift!=0:
            newikey='IllumMod'
            illumtimeshift(d, ikey, 't(s)', tshift)
        if self.params['illum_invert']:
            d[ikey]=-1*d[ikey]

        interd={}
        err=calcdiff_ill_caller(d, interd, ikey=ikey, thresh=self.params['illum_threshold'], \
            ykeys=[self.requiredkeys[0]], xkeys=list(self.requiredkeys[1:-1]), \
            illfracrange=(self.params['frac_illum_segment_start'], self.params['frac_illum_segment_end']), \
            darkfracrange=(self.params['frac_dark_segment_start'], self.params['frac_dark_segment_end']))
            
        illkey=self.requiredkeys[0]+'_illdiff'
        fomk=self.fomnames[0]
        #try:
        if err or len(interd[illkey])==0:
            dfhgf
            return [(fomk, numpy.nan)], {}, {}

        ncycs=self.params['num_illum_cycles']
        fromend=self.params['from_end']
        if fromend:
            arr=interd[illkey][::-1]
        else:
            arr=interd[illkey]
        arr=arr[:ncycs]
        return [(fomk, arr.mean())], dict([('IllumBool', d['IllumBool'])]), interd
        #except:
        #    pass
        return [(fomk, numpy.nan)], {}, {}
#

#
#
#        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)
#
##in options, always make an option that does not require user input at index 0
#        CVops=[\
#        ['Imax', ['I(A)'], []], \
#        ['Imin', ['I(A)'], []], \
#        ['E_Ithresh', ['I(A)','Ewe(V)'], [['Ithresh(A)', float, '1e-5'], ['Num consec points', int, '20'], ['0 for below, 1 for above', int, '1'], ['Thresh not reached value', float, '1']]], \
#        ['Eh in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
#        ['Io in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
#        ['Iphoto_max', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
#        ['Iphoto_min', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
#        ['None', ['I(A)', 'Ewe(V)'], []], \
#        ]
#
#        OCVops=[\
#        ['Efin', ['Ewe(V)'], []], \
#        ['Eave', ['Ewe(V)', 't(s)'], [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
#        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
#        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
#        ]
#
#        CPops=[\
#        ['Efin', ['Ewe(V)'], []], \
#        ['Eave', ['Ewe(V)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
#        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
#        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
#        ]
#
#        CAops=[\
#        ['Ifin', ['I(A)'], []], \
#        ['Iave', ['I(A)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
#        ['Iss', ['I(A)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
#        ['Iphoto', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
#        ]
#
#        Bubbleops=[\
#        ['slopefin', ['Maxslope'], []], \
#        ['Intfin', ['Intensity'], []], \
#        ]
#
#
#        self.expmnt_calc_options=[['OCV', OCVops], ['CP', CPops], ['CA', CAops], ['CV', CVops], ['Bubble', Bubbleops]]
#        self.expmnt_calc_lastusedvals=[[[] for calcopt in opslist] for opname, opslist in self.expmnt_calc_options]
#        expmntComboBoxLabel=QLabel()
#        expmntComboBoxLabel.setText('Technique type:')
#        self.expmntComboBox=QComboBox()
#        for i, tup in enumerate(self.expmnt_calc_options):
#            self.expmntComboBox.insertItem(i, tup[0])
#        self.expmntComboBox.setCurrentIndex(0)
#
#        calcoptionComboBoxLabel=QLabel()
#        calcoptionComboBoxLabel.setText('FOM:')
#        self.calcoptionComboBox=QComboBox()
#
#        ternskipComboBoxLabel=QLabel()
#        ternskipComboBoxLabel.setText('Exclude for ternary:')
#        self.ternskipComboBox=QComboBox()
#        for i, l in enumerate(['A', 'B', 'C', 'D']):
#            self.ternskipComboBox.insertItem(i, l)
#        self.ternskipComboBox.setCurrentIndex(i)
#
#        QObject.connect(self.expmntComboBox,SIGNAL("activated(QString)"),self.fillcalcoptions)
#        QObject.connect(self.calcoptionComboBox,SIGNAL("activated(QString)"),self.getcalcparams)
#
#        self.xplotchoiceComboBox=QComboBox()
#        self.yplotchoiceComboBox=QComboBox()
#        self.plotkeys=['t(s)', 'I(A)', 'Ewe(V)', 'Ece(V)', 'Ewe-E0(V)', 'I*Is(A)']
#        #keys=['Intensity', 'Fit', 'Maxslope']
#        for i, nam in enumerate(self.plotkeys):
#            self.xplotchoiceComboBox.insertItem(i, nam)
#            self.yplotchoiceComboBox.insertItem(i, nam)
#        self.xplotchoiceComboBox.setCurrentIndex(0)
#        self.yplotchoiceComboBox.setCurrentIndex(1)
#
#        xplotchoiceComboBoxLabel=QLabel()
#        xplotchoiceComboBoxLabel.setText('x-axis')
#        yplotchoiceComboBoxLabel=QLabel()
#        yplotchoiceComboBoxLabel.setText('y-axis')
#
#        expmntLineEditLabel=QLabel()
#        expmntLineEditLabel.setText('Technique Name:')
#        self.expmntLineEdit=QLineEdit()
#        self.expmntLineEdit.setText('OCV0')
#
#        folderButton=QPushButton()
#        folderButton.setText("select\nfolder")
#        QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfolder)
#
#        plotButton=QPushButton()
#        plotButton.setText("update\nfigures")
#        QObject.connect(plotButton, SIGNAL("pressed()"), self.calcandplot)
#        #QObject.connect(plotButton, SIGNAL("pressed()"), self.writefileauto)
#
#        updateButton=QPushButton()
#        updateButton.setText("update\ndata")
#        QObject.connect(updateButton, SIGNAL("pressed()"), self.calcandplotwithupdate)
#
#        saveButton=QPushButton()
#        saveButton.setText("save FOM\nspreadhseet")
#        QObject.connect(saveButton, SIGNAL("pressed()"), self.writefomfile_txt)
#
#        savesampleButton=QPushButton()
#        savesampleButton.setText("save select\nsample IDs")
#        QObject.connect(savesampleButton, SIGNAL("pressed()"), self.writesamplelist)
#
#
#        filterfomComboBoxLabel=QLabel()
#        filterfomComboBoxLabel.setText('Filter/Smooth:')
#        self.filterfomComboBox=QComboBox()
#        self.filterfomComboBox.clear()
#        for i, l in enumerate(['None', 'Setup', 'Apply']):
#                self.filterfomComboBox.insertItem(i, l)
#        self.filterfomComboBox.setCurrentIndex(0)
#        QObject.connect(self.filterfomComboBox,SIGNAL("activated(QString)"),self.filterfomsetup)
#
#
#
#        savebuttonlayout=QHBoxLayout()
#        savebuttonlayout.addWidget(folderButton)
#        savebuttonlayout.addWidget(plotButton)
#        savebuttonlayout.addWidget(updateButton)
#        savebuttonlayout.addWidget(saveButton)
#        savebuttonlayout.addWidget(savesampleButton)
##        savebuttonlayout=QHBoxLayout()
##        savebuttonlayout.addWidget(saveButton)
##        savebuttonlayout.addWidget(savesampleButton)
#
#        self.infoLabel=QLabel()
#        self.infodef='Q=10,15,40,80 1/nm -> \nd=0.63,0.42,0.16,0.079 nm\n'
#
#        self.revcmapCheckBox=QCheckBox()
#        self.revcmapCheckBox.setText('reverse cmap?')
#
#        templab=QLabel()
#        templab.setText('min,max colorbar')
#
#        self.vminmaxLineEdit=QLineEdit()
#
#        vminmaxlayout=QVBoxLayout()
#        vminmaxlayout.addWidget(templab)
#        vminmaxlayout.addWidget(self.vminmaxLineEdit)
#        vminmaxlayout.addWidget(self.revcmapCheckBox)
#        templab=QLabel()
#        templab.setText('below,above range colors:\nEnter a char,0-1 gray,tuple,\n"None" for ignore')
#
#        self.aboverangecolLineEdit=QLineEdit()
#        self.aboverangecolLineEdit.setText('k')
#        self.belowrangecolLineEdit=QLineEdit()
#        self.belowrangecolLineEdit.setText('0.9')
#
#        outrangecollayout=QGridLayout()
#        outrangecollayout.addWidget(templab, 0, 0, 2, 1)
#        outrangecollayout.addWidget(self.belowrangecolLineEdit, 0, 1)
#        outrangecollayout.addWidget(self.aboverangecolLineEdit, 1, 1)
#
#        self.statusLineEdit=QLineEdit()
#        self.statusLineEdit.setReadOnly(True)
#
#        self.measdescLineEdit=QLineEdit()
#        templab=QLabel()
#        templab.setText('Meas. Desc. for csv')
#
#        measdescLayout=QVBoxLayout()
#        measdescLayout.addWidget(templab)
#        measdescLayout.addWidget(self.measdescLineEdit)
#
#        templab=QLabel()
#        templab.setText('DAQ time')
#        self.daqtimeLineEdit=QLineEdit()
#        daqtimelayout=QVBoxLayout()
#        daqtimelayout.addWidget(templab)
#        daqtimelayout.addWidget(self.daqtimeLineEdit)
#
#        stackedtern10Button=QPushButton()
#        stackedtern10Button.setText("Create stacked\ntern at 10%")
#        QObject.connect(stackedtern10Button, SIGNAL("pressed()"), self.stackedtern10window)
#
#        stackedtern20Button=QPushButton()
#        stackedtern20Button.setText("Create stacked\ntern at 5%")
#        QObject.connect(stackedtern20Button, SIGNAL("pressed()"), self.stackedtern20window)
#
#        stackedtern30Button=QPushButton()
#        stackedtern30Button.setText("Create stacked\ntern at 3.33%")
#        QObject.connect(stackedtern30Button, SIGNAL("pressed()"), self.stackedtern30window)
#
#        stackedtern100Button=QPushButton()
#        stackedtern100Button.setText("Create stacked\ntern at 1%")
#        QObject.connect(stackedtern100Button, SIGNAL("pressed()"), self.stackedtern100window)
#
#        tern4Button=QPushButton()
#        tern4Button.setText("Create ternary\nfaces")
#        QObject.connect(tern4Button, SIGNAL("pressed()"), self.tern4window)
#
#        binlinesButton=QPushButton()
#        binlinesButton.setText("Create binary\nlines")
#        QObject.connect(binlinesButton, SIGNAL("pressed()"), self.binlineswindow)
#
#        templab=QLabel()
#        templab.setText('E0=Equil.Pot.(V):')
#        self.E0SpinBox=QDoubleSpinBox()
#        self.E0SpinBox.setDecimals(3)
#        self.E0SpinBox.setMaximum(10)
#        self.E0SpinBox.setMinimum(-10)
#        self.E0SpinBox.setValue(0)
#        E0layout=QHBoxLayout()
#        E0layout.addWidget(templab)
#        E0layout.addWidget(self.E0SpinBox)
#
#        templab=QLabel()
#        templab.setText('Is=I scaling:')
#        self.IsSpinBox=QDoubleSpinBox()
#        self.IsSpinBox.setMaximum(10.)
#        self.IsSpinBox.setMinimum(-10.)
#        self.IsSpinBox.setValue(1.)
#        Islayout=QHBoxLayout()
#        Islayout.addWidget(templab)
#        Islayout.addWidget(self.IsSpinBox)
#
#        self.overlayselectCheckBox=QCheckBox()
#        self.overlayselectCheckBox.setText("overlay on\n'select' plot")
#        self.legendselectLineEdit=QLineEdit()
#        self.legendselectLineEdit.setText('4')
#        templab=QLabel()
#        templab.setText("'select' plot\nlegend loc (int)")
#        legendlayout=QVBoxLayout()
#        legendlayout.addWidget(templab)
#        legendlayout.addWidget(self.legendselectLineEdit)
#
#
#
#        selectbuttonlayout=QHBoxLayout()
#        selectbuttonlab=QLabel()
#        selectbuttonlab.setText("Select samples by mouse right-click\n  OR filter FOM in this range:")
#        #selectbuttonlayout.addWidget(templab, 0, 0, 1, 3)
#
#        selectbelowButton=QPushButton()
#        selectbelowButton.setText("(-INF,min)")
#        QObject.connect(selectbelowButton, SIGNAL("pressed()"), self.selectbelow)
#        selectbuttonlayout.addWidget(selectbelowButton)#, 1, 0)
#
#        selectbetweenButton=QPushButton()
#        selectbetweenButton.setText("[min,max)")
#        QObject.connect(selectbetweenButton, SIGNAL("pressed()"), self.selectbetween)
#        selectbuttonlayout.addWidget(selectbetweenButton)#, 1, 1)
#
#        selectaboveButton=QPushButton()
#        selectaboveButton.setText("[max,INF)")
#        QObject.connect(selectaboveButton, SIGNAL("pressed()"), self.selectabove)
#        selectbuttonlayout.addWidget(selectaboveButton)#, 1, 2)
#
#
#        selectsamplelab=QLabel()
#        selectsamplelab.setText("sample IDs selected for export")
#        #selectsamplelayout=QVBoxLayout()
#        #selectsamplelayout.addWidget(templab)
#        self.selectsamplesLineEdit=QLineEdit()
#        #selectsamplelayout.addWidget(self.selectsamplesLineEdit)
#
#        self.ctrlgriditems=[\
#        (expmntComboBoxLabel, self.expmntComboBox, 0, 0), \
#        (calcoptionComboBoxLabel, self.calcoptionComboBox, 0, 1), \
#        (expmntLineEditLabel, self.expmntLineEdit, 0, 2), \
#        (xplotchoiceComboBoxLabel, self.xplotchoiceComboBox, 1, 0), \
#        (yplotchoiceComboBoxLabel, self.yplotchoiceComboBox, 1, 1), \
#        (ternskipComboBoxLabel, self.ternskipComboBox, 1, 2), \
#        (filterfomComboBoxLabel, self.filterfomComboBox, 2, 0), \
#        ]
#
#        mainlayout=QGridLayout()
#        ctrllayout=QGridLayout()
#        for labw, spw, i, j in self.ctrlgriditems:
#            templayout=QHBoxLayout()
#            templayout.addWidget(labw)
#            templayout.addWidget(spw)
#            ctrllayout.addLayout(templayout, i+1, j)
#        i-=1
##        ctrllayout.addWidget(folderButton, 0, 0)
##        ctrllayout.addWidget(plotButton, 0, 1)
#        ctrllayout.addLayout(savebuttonlayout, 0, 0, 1, 4)
#
#        #ctrllayout.addWidget(self.revcmapCheckBox, i+2, 0)
#        ctrllayout.addLayout(vminmaxlayout, i+2, 1)
#        ctrllayout.addLayout(outrangecollayout, i+2, 2)
#
#        #ctrllayout.addWidget(self.statusLineEdit, i+3, 0)
#        ctrllayout.addLayout(measdescLayout, i+3, 0)
#        ctrllayout.addWidget(self.overlayselectCheckBox, i+3, 1)
#        ctrllayout.addLayout(legendlayout, i+3, 2)
#
#        ctrllayout.addLayout(daqtimelayout, i+4, 0)
#        ctrllayout.addWidget(stackedtern10Button, i+4, 1)
#        ctrllayout.addWidget(stackedtern30Button, i+4, 2)
#        ctrllayout.addWidget(stackedtern20Button, i+5, 0)
#        ctrllayout.addWidget(tern4Button, i+5, 1)
#        ctrllayout.addWidget(binlinesButton, i+5, 2)
#        ctrllayout.addWidget(stackedtern100Button, i+6, 0)
#
#        ctrllayout.addLayout(E0layout, i+6, 1, 1, 1)
#        ctrllayout.addLayout(Islayout, i+6, 2, 1, 1)
#
#        ctrllayout.addWidget(selectbuttonlab, i+7, 0)
#        #ctrllayout.addLayout(selectsamplelayout, i+6, 1, 1, 2)
#        ctrllayout.addWidget(selectsamplelab, i+7, 1, 1, 2)
#
#        ctrllayout.addLayout(selectbuttonlayout, i+8, 0)
#        ctrllayout.addWidget(self.selectsamplesLineEdit, i+8, 1, 1, 2)
#
#        mainlayout.addLayout(ctrllayout, 0, 0)
#        mainlayout.addWidget(self.plotw_select, 0, 1)
#        mainlayout.addWidget(self.plotw_aux, 0, 2)
#        mainlayout.addWidget(self.plotw_plate, 1, 0)
#        mainlayout.addWidget(self.plotw_quat, 1, 1)
#        mainlayout.addWidget(self.plotw_comp, 1, 2)
#
#
#        self.setLayout(mainlayout)
#        self.filterfomstr=''
#        self.filterparams=None
#        self.filterparamsentry=[['remnan:\nRemove NaN', int, '1'], ['nhigh:\nUse N highest FOM', int, '999'], ['nlow:\nUse N lowest FOM', int, '0'], ['nsig:\nRemove outliers beyond N sigma', float, '999.']]
#
#        self.fillcalcoptions()
#        self.statusLineEdit.setText('idle')
#        self.plate_id=None
#        if folderpath is None:
#            self.folderpath=None
#            self.selectfolder()
#            self.calcandplot()
#        else:
#            self.folderpath=folderpath
#        self.resize(1600, 750)
#








#    def CalcFOM(self):
#        self.plotillumkey=None
#        techdict=self.techniquedictlist[self.selectind]
#        i=self.expmntComboBox.currentIndex()
#        j=self.calcoptionComboBox.currentIndex()
#        tup=self.expmnt_calc_options[i][1][j]
#        fcnnam=tup[0]
#        self.calckeys=tup[1]
#        if fcnnam=='Ifin' or fcnnam=='Efin':
#            returnval=techdict[self.calckeys[0]][-1]
#        elif fcnnam=='Imax' or fcnnam=='Emax':
#            returnval=numpy.max(techdict[self.calckeys[0]])
#        elif fcnnam=='Imin' or fcnnam=='Emin':
#            returnval=numpy.min(techdict[self.calckeys[0]])
#        elif fcnnam=='Iss' or fcnnam=='Ess':
#            returnval=CalcArrSS(techdict[self.calckeys[0]], WeightExp=self.CalcParams[0], TestPts=self.CalcParams[1])
#        elif fcnnam=='Iave' or fcnnam=='Eave':
#            x=techdict[self.calckeys[0]]
#            t=techdict[self.calckeys[1]]
#            if self.CalcParams[3]:
#                x=x[::-1]
#                t=t[::-1]
#            x=x[numpy.abs(t-t[0])<self.CalcParams[0]]
#            x=removeoutliers_meanstd(x, self.CalcParams[2]//2, self.CalcParams[1])
#            returnval=x.mean()
#        elif fcnnam=='Eh in I=Io Exp(E/Eh)' or fcnnam=='Io in I=Io Exp(E/Eh)':
#            print 'not implemented yet'
#            returnval=0.
#        elif fcnnam=='E_Ithresh':
#            i=techdict[self.calckeys[0]]
#            v=techdict[self.calckeys[1]]
#            icrit=self.CalcParams[0]
#            if not self.CalcParams[2]:
#                i*=-1
#                icrit*=-1
#            b=numpy.int16(i>=icrit)
#            n=self.CalcParams[1]
#            bconsec=[b[i:i+n].prod() for i in range(len(b)-n)]
#            if True in bconsec:
#                i=bconsec.index(True)
#                returnval=v[i:i+n].mean()
#            else:
#                returnval=self.CalcParams[3]
#        elif 'photo' in fcnnam:
#            ikey=self.CalcParams[4]
#            tshift=self.CalcParams[5]
#            if tshift!=0:
#                newikey='IllumMod'
#                techdict[newikey]=illumtimeshift(techdict, ikey, self.calckeys[3], tshift)
#                ikey=newikey
#                if self.CalcParams[7]!=0:
#                    techdict[ikey]*=-1
#            elif self.CalcParams[7]!=0:
#                newikey='IllumMod'
#                techdict[newikey]=-1*techdict[ikey]
#                ikey=newikey
#
#            illkey=self.calckeys[1]+'_illdiff'
#            err=calcdiff_ill_caller(techdict, ikey=ikey, thresh=self.CalcParams[6], ykeys=[self.calckeys[1]], xkeys=list(self.calckeys[2:]), illfracrange=(self.CalcParams[0], self.CalcParams[1]), darkfracrange=(self.CalcParams[2], self.CalcParams[3]))
#            try:
#				if err or len(techdict[illkey])==0:
#					return 0
#				self.plotillumkey='IllumBool'
#
#				ncycs=self.CalcParams[8]
#				fromend=self.CalcParams[9]
#				if fromend:
#					arr=techdict[illkey][::-1]
#				else:
#					arr=techdict[illkey]
#				arr=arr[:ncycs]
#
#				if 'min' in fcnnam:
#					returnval=min(arr)
#				elif 'max' in fcnnam:
#					returnval=max(arr)
#				else:
#					returnval=numpy.mean(arr)
#            except:
#				return 0
#        else:
#            print 'FOM function not understood'
#            return 0.
#        if fcnnam.startswith('I'):
#            return returnval*self.IsSpinBox.value()
#        if fcnnam.startswith('E'):
#            return returnval-self.E0SpinBox.value()
#        else:
#            return returnval
#
#    def CalcAllFOM(self):
#        for i, d in enumerate(self.techniquedictlist):
#            self.selectind=i
#            d['FOM']=self.CalcFOM()
#        if self.filterfomComboBox.currentIndex()==2:
#            self.filterfom()
#            self.filterfomstr=self.filterparams['label']
#        else:
#            self.filterfomstr=''
#
#    def filterfom(self):
#        smps=[d['Sample'] for d in self.techniquedictlist]
#        data=[d['FOM'] for d in self.techniquedictlist]
#
#        d_smpstoave=self.filterparams['d_smpstoave']
#        newsmps=[sm for sm in d_smpstoave.keys() if sm in smps]
#
#        datacomparrs=[[data[numpy.where(smps==smp2)[0][0]] for smp2 in d_smpstoave[smp] if smp2 in smps] for smp in newsmps]
#        if self.filterparams['remnan']:
#            datacomparrs=[[v for v in arr if not numpy.isnan(v)] for arr in datacomparrs]
#        arrlens=[len(arr) for arr in datacomparrs]
#        if max([self.filterparams['nlow'], self.filterparams['nhigh']])<max(arrlens):
#            if self.filterparams['nlow']>self.filterparams['nhigh']:
#                datacomparrs=[sorted(arr)[:self.filterparams['nlow']] for arr in datacomparrs]
#            else:
#                datacomparrs=[sorted(arr)[::-1][:self.filterparams['nhigh']] for arr in datacomparrs]
#        if self.filterparams['nsig']<999.:
#            numstd=self.filterparams['nsig']
#            datacompave=[]
#            for arr in datacomparrs:#datacomparrs doesn't actually get updated here.
#                arr=numpy.array(arr)
#                arr2=numpy.abs((arr-arr.mean())/arr.std())
#                while numpy.any(arr2>numstd):
#                    #print (arr2>numstd).sum()
#                    arr=numpy.delete(arr, arr2.argmax())
#                    arr2=numpy.abs((arr-arr.mean())/arr.std())
#                datacompave+=[arr.mean()]
#        else:
#            datacompave=numpy.array([numpy.array(arr).mean() for arr in datacomparrs])
#
#
#        for d in self.techniquedictlist:
#            if d['Sample'] in newsmps:
#                d['FOM']=datacompave[newsmps.index(d['Sample'])]
#            else:
#                d['FOM']=numpy.nan
#
#        #self.techniquedictlist=[d for d in self.techniquedictlist if not numpy.isnan(d['FOM'])]
#
#
#
#    def filterfomsetup(self):
#        if self.filterfomComboBox.currentIndex()==0:
#            self.filterparams=None
#            return
#        elif self.filterfomComboBox.currentIndex()==2 and not self.filterparams is None:
#            return
#        #user-defined filterparams
#        self.filterparams={}
#        p=mygetopenfile(self, markstr='.pck file providing sample filter/smooth map', filename='.pck' )
#        f=open(p, mode='rU')
#        self.filterparams['d_smpstoave']=pickle.load(f)
#        f.close()
#        self.filterparams['label']='_'+p.rpartition('_')[2].partition('.')[0]
#
#
#        ans=userinputcaller(self, inputs=self.filterparamsentry, title='Enter database credentials', cancelallowed=True)
#        if ans is None:
#            self.filterparams=None
#            return
#        for a, tup in zip(ans, self.filterparamsentry):
#            self.filterparams[tup[0].partition(':')[0]]=a
#
#        self.filterfomComboBox.setCurrentIndex(2)
#
#    def get_techniquedictlist(self, ext='.txt', nfiles=99999, dbupdate=False):
#        self.statusLineEdit.setText('calculating FOM')
#        dlist=[]
#        existpaths=[d['path'] for d in self.techniquedictlist]
#        existmtimes=[d['mtime'] for d in self.techniquedictlist]
#        self.selectind=-1
#
#        techname=str(self.expmntLineEdit.text())
#
#        if self.dbdatasource is 1:
#            if len(techname)==0 and len(self.techniquedictlist)==0:
#                technamedflt=self.dbrecarrd['technique_name'][0]
#                for i, tup in enumerate(self.expmnt_calc_options):
#                    if technamedflt.startswith(tup[0]):
#                        self.expmntComboBox.setCurrentIndex(i)
#                        self.expmntLineEdit.setText(technamedflt)
#                        self.fillcalcoptions()
#                        break
#
#            if dbupdate:
#                ##this line for getting updated data
#                self.selectfolder(plate_id=self.plate_id, selectexids=self.selectexids)
#
#            fns=self.dbrecarrd['dc_data__t_v_a_c_i'][self.dbrecarrd['technique_name']==techname]
#
#            pathstoread=[os.path.join(os.path.join('J:/hte_echemdrop_proto/data','%d' %self.plate_id), fn) for fn in fns]
#            updateexcludebool=True
#
#            dlist=[(p in existpaths and (self.techniquedictlist[existpaths.index(p)],) or (readechemtxt(p, mtime_path_fcn=self.getepoch_path),))[0] for p in pathstoread[:nfiles]]
#            dlist=[d for d in dlist if d]#get rid of emtpy dictionaries
#        else:
#            fns=os.listdir(self.folderpath)
#            if len(techname)==0 and len(self.techniquedictlist)==0:
#                for i, tup in enumerate(self.expmnt_calc_options):
#                    techstr='%s0' %tup[0]
#                    if True in [techstr in fn for fn in fns]:
#                        self.expmntComboBox.setCurrentIndex(i)
#                        self.expmntLineEdit.setText(techstr)
#                        self.fillcalcoptions()
#                        break
#            pathstoread=[os.path.join(self.folderpath, fn) for fn in fns if techname in fn and fn.endswith(ext) and fn.startswith('Sample')]
#
#            updateexcludebool=True
#
#            for p in pathstoread[:nfiles]:
#                mtime=self.getepoch_path(p)#os.path.getmtime(p)
#                if p in existpaths and existmtimes[existpaths.index(p)]==mtime:
#                    dlist+=[self.techniquedictlist[existpaths.index(p)]]
#                    updateexcludebool=False
#                else:
#                    d=readechemtxt(p)
#                    if not d:
#                        continue
#                    d['path']=p
#                    d['mtime']=mtime
#                    dlist+=[d]
#
#        inds=numpy.argsort(getarrfromkey(dlist, 'mtime'))
#        self.techniquedictlist=[dlist[i] for i in inds]
#        if len(self.techniquedictlist)>0:
#            d=self.techniquedictlist[0]
#            maxlen=max([len(v) for k, v in d.items() if isinstance(v, numpy.ndarray)])
#            plotkeys=set([k for k, v in d.items() if isinstance(v, numpy.ndarray) and len(v)==maxlen])
#            #plotkeys=set(.keys())-set(['path', 'mtime'])
#            if set(self.plotkeys)!=plotkeys:
#                self.plotkeys=list(plotkeys)
#                self.xplotchoiceComboBox.clear()
#                self.yplotchoiceComboBox.clear()
#                for i, nam in enumerate(self.plotkeys):
#                    self.xplotchoiceComboBox.insertItem(i, nam)
#                    self.yplotchoiceComboBox.insertItem(i, nam)
#                self.xplotchoiceComboBox.setCurrentIndex(0)
#                self.yplotchoiceComboBox.setCurrentIndex(1)
#    def getepoch_path(self, p, readbytes=1000):
#        try:
#            #print os.path.exists(p), p
#            try:#need to sometimes try twice so might as well try 3 times
#                f=open(p, mode='r')
#            except:
#                try:
#                    f=open(p, mode='r')
#                except:
#                    f=open(p, mode='r')
#            s=f.read(readbytes)
#            f.close()
#            return eval (s.partition('Epoch=')[2].partition('\n')[0].strip())
#        except:
#            return 0.
#
#    def calcandplotwithupdate(self, ext='.txt'):
#        self.calcandplot(ext='.txt', dbupdate=True)
#
#    def calcandplot(self, ext='.txt', dbupdate=False):
#        self.get_techniquedictlist(ext=ext, dbupdate=dbupdate)
#
#        self.CalcAllFOM()
##        for i, d in enumerate(self.techniquedictlist):
##            self.selectind=i
##            #if not 'FOM' in d.keys():
##            d['FOM']=self.CalcFOM()
#
#        i0=self.ternskipComboBox.currentIndex()
#        if len(self.techniquedictlist)>0: #and updateexcludebool
#            self.ternskipComboBox.clear()
#            for i, l in enumerate(self.techniquedictlist[0]['elements']):
#                self.ternskipComboBox.insertItem(i, l)
#            self.ternskipComboBox.setCurrentIndex(i0)
#        self.setWindowTitle(str(os.path.split(self.folderpath)[1]))
#        self.statusLineEdit.setText('idle')
#        self.plot()
#        self.writefileauto()#writes files if dbdatasource==2, which means source is on K:
#
#






#
#    def writefomfile_txt(self, p=None, explab=None, savedlist=False):
#        self.statusLineEdit.setText('writing file')
#        if len(self.techniquedictlist)==0:
#            print 'no data to save'
#            return
#        if explab is None:
#            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
#        if p is None:
#            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt', xpath=self.kexperiments)
#        elif os.path.isdir(p):
#            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
#            print p
#        if not p:
#            print 'save aborted'
#            return
#
#        labels=['Sample', 'x(mm)', 'y(mm)']
#        labels+=self.techniquedictlist[0]['elements']
#        labels+=[explab]
#        labels+=['Date', 'Time']
#        kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), ('FOM', '%.6e')]
#        arr=[]
#        for d in self.techniquedictlist:
#            arr2=[]
#            for k, fmt in kv_fmt:
#                v=d[k]
#                if isinstance(v, numpy.ndarray) or isinstance(v, list):
#                    for subv in v:
#                        arr2+=[fmt %subv]
#                else:
#                    arr2+=[fmt %v]
#            structtime=d['mtime']-2082844800
#            arr2+=[time.strftime("%Y-%m-%d",time.localtime(structtime))]
#            arr2+=[time.strftime("%H:%M:%S",time.localtime(structtime))]
#            arr+=['\t'.join(arr2)]
#        s='\t'.join(labels)+'\n'
#        s+='\n'.join(arr)
#
#        f=open(p, mode='w')
#        f.write(s)
#        f.close()
#
#        if savedlist:
#            f=open(p[:-4]+'_dlist.pck', mode='w')
#            pickle.dump(self.techniquedictlist, f)
#            f.close()
#
#        self.statusLineEdit.setText('idle')
#    def writefomfile_csv(self, p=None, explab=None, savedlist=False):
#        self.statusLineEdit.setText('writing file')
#        if len(self.techniquedictlist)==0:
#            print 'no data to save'
#            return
#        if explab is None:
#            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
#        if p is None:
#            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt', xpath=self.kexperiments)
#        elif os.path.isdir(p):
#            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
#            print p
#        if not p:
#            print 'save aborted'
#            return
#
#        labels=['sample_no']
#        labels+=[explab]
#        kv_fmt=[('Sample', '%d'), ('FOM', '%.5e')]
#        arr=[]
#        for d in self.techniquedictlist:
#            arr2=[]
#            for k, fmt in kv_fmt:
#                v=d[k]
#                if isinstance(v, numpy.ndarray) or isinstance(v, list):
#                    for subv in v:
#                        arr2+=[fmt %subv]
#                else:
#                    arr2+=[fmt %v]
#            arr+=[','.join(arr2)]
#        s=','.join(labels)+'\n'
#        s+='\n'.join(arr)
#        s=s.replace('nan', 'NaN')
#
#        desc=str(self.measdescLineEdit.text()).strip().replace('"', '')
#        if len(desc)>0:
#            s='#description = "'+desc+'"\n'+s
#
#        f=open(p, mode='w')
#        f.write(s)
#        f.close()
#
#        if savedlist:
#            f=open(p[:-4]+'_dlist.pck', mode='w')
#            pickle.dump(self.techniquedictlist, f)
#            f.close()
#
#        self.statusLineEdit.setText('idle')
#    def writefileauto(self, folder=None, explab=None):
#        self.statusLineEdit.setText('writing file')
#        if len(self.techniquedictlist)==0:
#            print 'abort autosave - no data to save'
#            return
#        if explab is None:
#            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
#
#        #try to get plate id from folder name; if successful (finds a string of digits) and dbdatasource=2, create folder in K: experiments; works on *nix and Windows, untested on OSX
#        #idfromfolder=os.path.split(self.folderpath)[1].rsplit('_',1)[1].split(' ',1)[0]
#        folderstrings=os.path.split(self.folderpath)[1].split('_')
#        idfromfolder=None
#        idsuffices=[]
#        for i in range(len(folderstrings)):
#            fs=folderstrings[-i-1].split(' ')[0]
#            if fs.isdigit():
#                fslist=map(int, list(fs))
#                checksum=sum(fslist[0:len(fslist)-1]) % 10 is fslist[-1]
#                if checksum:
#                    idfromfolder=' '.join([folderstrings[-i-1]]+idsuffices)
#                    break
#            else:
#                idsuffices=[folderstrings[-i-1]]+idsuffices
#        exptypes=('eche', 'ecqe')
#        if idfromfolder is None:
#            print 'cannot autosave due to lack of serial number'
#            return
#        if self.measdescLineEdit.text().isEmpty():
#            print 'cannot autosave due to lack of description'
#            return
#        if not folder is None:
#            txtfolder=folder
#            csvfolder=folder
#        elif self.dbdatasource is 2:
#            for exp in exptypes:
#                if exp in self.folderpath:
#                    txtfolder=os.path.join(self.kexperiments, exp, 'fom_data', idfromfolder)
#                    csvfolder=os.path.join(self.kexperiments, exp, 'csv')
#                    break
#        else:
#            return
#
#        if not os.path.isdir(txtfolder):
#            try:
#                os.mkdir(txtfolder)
#            except:
#                print 'cannot autosave because unable to make directory ', txtfolder
#                txtfolder=None
#        if not txtfolder is None:
#            txtp=os.path.join(txtfolder, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
#            print 'autosaving ', txtp
#            self.writefomfile_txt(p=txtp, explab=explab, savedlist=False)
#
#        if not os.path.isdir(csvfolder):
#            try:
#                os.mkdir(csvfolder)
#            except:
#                print 'cannot autosave because unable to make directory ', csvfolder
#                csvfolder=None
#        if not csvfolder is None:
#            csvp=os.path.join(csvfolder, idfromfolder+'-'+explab+'-EcVisAuto.csv')
#            print 'autosaving ', csvp
#            self.writefomfile_csv(p=csvp, explab=explab, savedlist=False)
