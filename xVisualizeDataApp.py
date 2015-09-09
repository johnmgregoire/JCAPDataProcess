from fcns_io import smp_dict_generaltxt
from csvfilewriter import createcsvfilstr, selectexportfom
from fcns_ui import *
import copy
from fcns_compplots import *


class legendformatwidget(QDialog):
    def __init__(self, parent=None, title='', arr=None):
        super(legendformatwidget, self).__init__(parent)
        self.parent=parent

        templab=QLabel()
        templab.setText('fom fmt')
        self.fomfmtLineEdit=QLineEdit()
        self.fomfmtLineEdit.setText('%.2e')
        
        templab2=QLabel()
        templab2.setText('comp fmt')
        self.compfmtLineEdit=QLineEdit()
        self.compfmtLineEdit.setText('%d')
        
        templab3=QLabel()
        templab3.setText('legend contents, for example\n<sample>, <A><a><B><b><C><c><D><d>, <code>, <fom>')
        self.legendLineEdit=QLineEdit()
        self.legendLineEdit.setText('<sample>')
        
        mainlayout=QGridLayout()
        mainlayout.addWidget(templab, 0, 0)
        mainlayout.addWidget(self.fomfmtLineEdit, 1, 0)
        mainlayout.addWidget(templab2, 0, 1)
        mainlayout.addWidget(self.compfmtLineEdit, 1, 1)
        mainlayout.addWidget(templab3, 2, 0, 1, 2)
        mainlayout.addWidget(self.legendLineEdit, 3, 0, 1, 2)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        #QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        
        self.setLayout(mainlayout)

        self.resize(300, 250)
        self.selectinds=[]
    
    def ExitRoutine(self):
        fomfmt=str(self.fomfmtLineEdit.text())
        compfmt=str(self.compfmtLineEdit.text())
        legendcmd=str(self.legendLineEdit.text())
        
        def genlegtext(sample, els, comp, code, fom, fomfmt=fomfmt, compfmt=compfmt, legendcmd=legendcmd):
            legstr=legendcmd[:]
            for count, (n, ss) in enumerate(zip((fom, sample, code), ('<fom>', '<sample>', '<code>'))):
                if n is None:
                    legstr=legstr.replace(ss, '')
                    continue
                if count==0:
                    s=fomfmt %n
                else:
                    s='%d' %n
                legstr=legstr.replace(ss, s)
            if 'd' in compfmt:
                compstr=[compfmt %int(round(c*100.)) for c in comp]
            else:
                compstr=[compfmt %c for c in comp]
            for l, ssl in zip([els, compstr], [['<A>', '<B>', '<C>', '<D>'], ['<a>', '<b>', '<c>', '<d>']]):
                for s, ss in zip(l, ssl):
                    legstr=legstr.replace(ss, s)
            return legstr
        self.genlegfcn=genlegtext
        
class filtersampleswidget(QDialog):
    def __init__(self, parent=None, title='', arr=None, minval=None, maxval=None, minmaxfmt='%.2e'):
        super(filtersampleswidget, self).__init__(parent)
        self.parent=parent
        self.setWindowTitle(title)
        self.arr=arr
        
        self.selectbelowCheckBox=QCheckBox()
        self.selectbelowCheckBox.setText("(-INF,min)")
        
        self.selectbetweenCheckBox=QCheckBox()
        self.selectbetweenCheckBox.setText("[min,max)")
        self.selectbetweenCheckBox.setChecked(True)
        
        self.selectaboveCheckBox=QCheckBox()
        self.selectaboveCheckBox.setText("[max,INF)")
        
        mainlayout=QGridLayout()

        mainlayout.addWidget(self.selectbelowCheckBox, 0, 0, 1, 2)
        mainlayout.addWidget(self.selectbetweenCheckBox, 1, 0, 1, 2)
        mainlayout.addWidget(self.selectaboveCheckBox, 2, 0, 1, 2)
        
        templab=QLabel()
        templab.setText('min FOM')
        self.vminLineEdit=QLineEdit()
        if not minval is None:
            self.vminLineEdit.setText(minmaxfmt %minval)
        
        templab2=QLabel()
        templab2.setText('max FOM')
        self.vmaxLineEdit=QLineEdit()
        if not maxval is None:
            self.vmaxLineEdit.setText(minmaxfmt %maxval)
        
        mainlayout.addWidget(templab, 3, 0)
        mainlayout.addWidget(self.vminLineEdit, 3, 1)
        mainlayout.addWidget(templab2, 4, 0)
        mainlayout.addWidget(self.vmaxLineEdit, 4, 1)
        
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 5, 0, 1, 2)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        #QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        
        self.setLayout(mainlayout)

        self.resize(300, 250)
        self.selectinds=[]
    
    def ExitRoutine(self):
        if not isinstance(self.arr, numpy.ndarray):
            print 'not filtering because fom array not provided'
            return
        abovebool=self.selectaboveCheckBox.isChecked()
        betweenbool=self.selectbetweenCheckBox.isChecked()
        belowbool=self.selectbelowCheckBox.isChecked()
        
        if abovebool or betweenbool:
            try:
                maxval=myeval(str(self.vmaxLineEdit.text()).strip())
            except:
                print 'error interpreting max value'
                return
        if belowbool or betweenbool:
            try:
                minval=myeval(str(self.vminLineEdit.text()).strip())
            except:
                print 'error interpreting min value'
                return
        if belowbool:
            self.selectinds+=list(numpy.where(self.arr<minval)[0])
        if betweenbool:
            self.selectinds+=list(numpy.where((self.arr>=minval)&(self.arr<maxval))[0])
        if abovebool:
            self.selectinds+=list(numpy.where(self.arr>=maxval)[0])
        
class fomplotoptions(QDialog):
    def __init__(self, parent=None, vmin=0, vmax=1, rev_cols=None, fomkey='', fommultstr='1.', title=''):
        super(fomplotoptions, self).__init__(parent)
        self.parent=parent
        
        self.revcmapCheckBox=QCheckBox()
        self.revcmapCheckBox.setText('reverse cmap?')
        
        self.fommultstr=fommultstr
        self.fomkey=fomkey
        
        templab=QLabel()
        templab.setText('min,max colorbar')
        
        self.vminmaxLineEdit=QLineEdit()
        self.vminmaxLineEdit.setText(','.join(['%.2e' %n for n in [vmin, vmax]]))
        vminmaxlayout=QVBoxLayout()
        vminmaxlayout.addWidget(templab)
        vminmaxlayout.addWidget(self.vminmaxLineEdit)

        templab=QLabel()
        templab.setText('below,above range colors:\nEnter a char,0-1 gray,tuple,\n"None" for ignore')
        
        self.aboverangecolLineEdit=QLineEdit()
        self.belowrangecolLineEdit=QLineEdit()
        
        
        if rev_cols is None or len(rev_cols)!=3:
            self.belowrangecolLineEdit.setText('k')
            self.aboverangecolLineEdit.setText('(0.5,0,0)')
        else:
            self.revcmapCheckBox.setChecked(rev_cols[0])
            self.belowrangecolLineEdit.setText(rev_cols[1])
            self.aboverangecolLineEdit.setText(rev_cols[2])
            
        outrangecollayout=QGridLayout()
        outrangecollayout.addWidget(templab, 0, 0, 2, 1)
        outrangecollayout.addWidget(self.belowrangecolLineEdit, 0, 1)
        outrangecollayout.addWidget(self.aboverangecolLineEdit, 1, 1)
        
        mainlayout=QGridLayout()

        mainlayout.addWidget(self.revcmapCheckBox, 0, 0)
        mainlayout.addLayout(vminmaxlayout, 0, 1)
        mainlayout.addLayout(outrangecollayout, 0, 2)
        
        templab3=QLabel()
        templab3.setText('FOM label')
        self.fomkeyLineEdit=QLineEdit()
        self.fomkeyLineEdit.setText(fomkey)
        
        templab4=QLabel()
        templab4.setText('FOM multiplier')
        self.fommultLineEdit=QLineEdit()
        self.fommultLineEdit.setText(fommultstr)

        fomkeyLayout=QVBoxLayout()
        fomkeyLayout.addWidget(templab3)
        fomkeyLayout.addWidget(self.fomkeyLineEdit)
        fommultLayout=QVBoxLayout()
        fommultLayout.addWidget(templab4)
        fommultLayout.addWidget(self.fommultLineEdit)
        mainlayout.addLayout(fomkeyLayout, 1, 0, 1, 2)
        mainlayout.addLayout(fommultLayout, 1, 2, 1, 2)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 2, 0, 1, 3)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        #QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        
        self.setLayout(mainlayout)

        self.resize(600, 250)
        self.error=True
        self.rev_cols=rev_cols
    
    def ExitRoutine(self):
        self.rev_cols=[]
        if self.revcmapCheckBox.isChecked():
            self.cmap=cm.jet_r
            self.rev_cols+=[True]
        else:
            self.cmap=cm.jet
            self.rev_cols+=[False]
        self.skipoutofrange=[False, False]
        
        vstr=str(self.vminmaxLineEdit.text()).strip()
        self.fomkey=str(self.fomkeyLineEdit.text()).strip()
        self.fommultstr=str(self.fommultLineEdit.text()).strip()
        
            
        try:
            self.fommult=myeval(self.fommultstr)
            a, b, c=vstr.partition(',')
            a=myeval(a.strip())
            c=myeval(c.strip())
            self.vmin=a
            self.vmax=c
            for count, (fcn, le) in enumerate(zip([self.cmap.set_under, self.cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
                vstr=str(le.text()).strip()
                self.rev_cols+=[vstr]
                vstr=vstr.replace('"', '').replace("'", "")
                if 'none' in vstr or 'None' in vstr:
                    self.skipoutofrange[count]=True
                    continue
                if len(vstr)==0:
                    continue
                c=col_string(vstr)
                try:
                    fcn(c)
                except:
                    print 'color entry not understood:', vstr
            self.error=False
        except:
            self.error=True
            self.rev_cols=None
            
class visdataDialog(QDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(visdataDialog, self).__init__(parent)
        self.parent=parent
        

        self.plotw_stack_cbaxrect=[.85, .1, .04, .8]
        
        self.plotw_stack=plotwidget(self)

        self.cbax_stack=self.plotw_stack.fig.add_axes(self.plotw_stack_cbaxrect)
        
        axrect=[0.82, 0.1, 0.04, 0.8]
        
        self.plotw_plate=plotwidget(self)
        self.plotw_plate.axes.set_aspect(1)
        
        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)

        self.plotw_xy=plotwidget(self, width=6, height=6)
        self.plotw_xy.fig.subplots_adjust(left=0.12, bottom=.12, right=.9)
        
        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)
        QObject.connect(self.plotw_stack, SIGNAL("genericclickonplot"), self.stackclickprocess)

        xplotchoiceComboBoxLabel=QLabel()
        xplotchoiceComboBoxLabel.setText('x-axis')
        
        yplotchoiceComboBoxLabel=QLabel()
        yplotchoiceComboBoxLabel.setText('y-axis')
        xycolplotchoiceComboBoxLabel=QLabel()
        xycolplotchoiceComboBoxLabel.setText('color by')
        self.xplotchoiceComboBox=QComboBox()
        self.xplotchoiceComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.yplotchoiceComboBox=QComboBox()
        self.xycolplotchoiceComboBox=QComboBox()
#        for i, nam in enumerate(['t(s)', 'I(A)', 'Ewe(V)', 'Ece(V)']):
#            self.xplotchoiceComboBox.insertItem(i, nam)
#            self.yplotchoiceComboBox.insertItem(i, nam)
#        self.xplotchoiceComboBox.setCurrentIndex(0)
#        self.yplotchoiceComboBox.setCurrentIndex(1)
#        

        templab=QLabel()
        templab.setText('x min,max')
        self.xminmaxLineEdit=QLineEdit()
        self.xminmaxLineEdit.setFixedWidth(140)
        xminmaxlayout=QVBoxLayout()
        xminmaxlayout.addWidget(templab)
        xminmaxlayout.addWidget(self.xminmaxLineEdit)
        
        templab=QLabel()
        templab.setText('y min,max')
        self.yminmaxLineEdit=QLineEdit()
        self.yminmaxLineEdit.setFixedWidth(140)
        yminmaxlayout=QVBoxLayout()
        yminmaxlayout.addWidget(templab)
        yminmaxlayout.addWidget(self.yminmaxLineEdit)
        
        
        self.overlayselectCheckBox=QCheckBox()
        self.overlayselectCheckBox.setText("overlay on\n'select' plot")
        
        customxylegendPushButton=QPushButton()
        customxylegendPushButton.setText("customize\nlegend")
        QObject.connect(customxylegendPushButton, SIGNAL("pressed()"), self.getcustomlegendfcn)
        self.customlegendfcn=lambda sample, els, comp, code, fom: `sample`
        
        self.fileLineEdit=QLineEdit()        
        self.fileLineEdit.setText('')
        fileLineEditLabel=QLabel()
        fileLineEditLabel.setText('Platemap\nFile:')
        fileLineEditlayout=QVBoxLayout()

        self.folderLineEdit=QLineEdit()        
        self.folderLineEdit.setText('')
        folderLineEditLabel=QLabel()
        folderLineEditLabel.setText('Folder with\nPck\Txt Data:')
        folderLineEditlayout=QVBoxLayout()

        ternstackComboBoxLabel=QLabel()
        ternstackComboBoxLabel.setText('Pseudo-tern\nstack wrt:')
        self.ternstackComboBox=QComboBox()
        self.ternstackComboBox.clear()
        for i, l in enumerate(['D', 'A', 'B', 'C']):
                self.ternstackComboBox.insertItem(i, l)
        self.ternstackComboBox.setCurrentIndex(0)
        QObject.connect(self.ternstackComboBox,SIGNAL("activated(QString)"),self.setupcomppermute)
        
        
        compLineEditLabel=QLabel()
        compLineEditLabel.setText('Composition:\n(as in a,b,c,d)')
        self.compLineEdit=QLineEdit()
        self.compLineEdit.setText('0.5,0.4,0.1,0.0')
        
        
        xyLineEditLabel=QLabel()
        xyLineEditLabel.setText('x,y position:')
        self.xyLineEdit=QLineEdit()
        self.xyLineEdit.setText('5.45, 6.33')
        
        sampleLineEditLabel=QLabel()
        sampleLineEditLabel.setText('Sample No(s).:')
        self.sampleLineEdit=QLineEdit()
        self.sampleLineEdit.setText('254')


        selectMap=QPushButton()
        selectMap.setText("select\nplatemap")
        QObject.connect(selectMap, SIGNAL("pressed()"), self.openPlateMap)
        
        
        self.elsLineEdit=QLineEdit()        
        self.elsLineEdit.setText('A,B,C,D')
        elsLineEditLabel=QLabel()
        elsLineEditLabel.setText('elements:')
        QObject.connect(self.elsLineEdit,SIGNAL("editingFinished()"),self.setupcomppermute)
        
        ternfacesPushButton=QPushButton()
        ternfacesPushButton.setText("tern. faces")
        QObject.connect(ternfacesPushButton, SIGNAL("pressed()"), self.openternfacesplot)
        
        binlinesPushButton=QPushButton()
        binlinesPushButton.setText("bin. lines")
        QObject.connect(binlinesPushButton, SIGNAL("pressed()"), self.openbinlinesplot)
        
        openplotsLayout=QVBoxLayout()
        openplotsLayout.addWidget(ternfacesPushButton)
        openplotsLayout.addWidget(binlinesPushButton)
        
        selectFolder=QPushButton()
        selectFolder.setText("select\ndata folder")
        QObject.connect(selectFolder, SIGNAL("pressed()"), self.openDataFolder)
        
        savecsvPushButton=QPushButton()
        savecsvPushButton.setText("save FOM\n.csv file")
        QObject.connect(savecsvPushButton, SIGNAL("pressed()"), self.savefomcsv)
        
        self.codesLineEdit=QLineEdit()        
        self.codesLineEdit.setText('')
        codesLineEditLabel=QLabel()
        codesLineEditLabel.setText('only show these codes:\nwhen open platemap')
        
        (self.addComp, self.addValuesComp), 
        (self.remComp, self.remValuesComp), 
        (self.addxy, self.addValuesXY), 
        (self.remxy, self.remValuesXY), 
        (self.addSample, self.addValuesSample), 
        (self.remSample, self.remValuesSample)

        savesampleButton=QPushButton()
        savesampleButton.setText("save select\nsample IDs")
        QObject.connect(savesampleButton, SIGNAL("pressed()"), self.writesamplelist)
        
        fomComboBoxLabel=QLabel()
        fomComboBoxLabel.setText('select\nFOM:')
        self.fomComboBox=QComboBox()
        self.fomComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.fomComboBox.clear()
        self.fomComboBox.insertItem(0, 'composition/selected')
        self.fomComboBox.setCurrentIndex(0)
        QObject.connect(self.fomComboBox,SIGNAL("activated(QString)"),self.fomcolorselected)
        
        fomplotoptsPushButton=QPushButton()
        fomplotoptsPushButton.setText("edit FOM\ncolor scale")
        QObject.connect(fomplotoptsPushButton, SIGNAL("pressed()"), self.editfomopts)
        
        filtersmpsPushButton=QPushButton()
        filtersmpsPushButton.setText("select samples\nby FOM")
        QObject.connect(filtersmpsPushButton, SIGNAL("pressed()"), self.filtersmpbyfom)
        
        self.ctrlgriditems=[\
        (fileLineEditLabel, self.fileLineEdit, 0, 0),\
        (folderLineEditLabel, self.folderLineEdit, 1, 0),\
        (codesLineEditLabel, self.codesLineEdit, 2, 0), \
        (compLineEditLabel, self.compLineEdit, 3, 0), \
        (xyLineEditLabel, self.xyLineEdit, 4, 0),\
        (sampleLineEditLabel, self.sampleLineEdit, 5, 0),\
        ]
        
        mainlayout=QGridLayout()
        ctrllayout=QGridLayout()
        for labw, spw, i, j in self.ctrlgriditems:
            templayout=QHBoxLayout()
            templayout.addWidget(labw)
            templayout.addWidget(spw)
            ctrllayout.addLayout(templayout, i, j)
        
        ctrllayout.addWidget(selectMap, 0, 1)
        
        elsLayout=QVBoxLayout()
        elsLayout.addWidget(elsLineEditLabel)
        elsLayout.addWidget(self.elsLineEdit)
#        temp=QHBoxLayout()
#        temp.addLayout(elsLayout)
#        temp.addWidget(ternfacesPushButton)
        temp=QHBoxLayout()
        temp.addWidget(ternstackComboBoxLabel)
        temp.addWidget(self.ternstackComboBox)
        
        ctrllayout.addWidget(savecsvPushButton, 0, 2)
        ctrllayout.addLayout(elsLayout, 1, 2)
        ctrllayout.addWidget(selectFolder, 1, 1)
        #ctrllayout.addWidget(ternfacesPushButton, 2, 1)
        ctrllayout.addLayout(openplotsLayout, 2, 1)
        ctrllayout.addLayout(temp, 2, 2)
        #ctrllayout.addWidget(ternstackComboBoxLabel, 2, 1)
        #ctrllayout.addWidget(self.ternstackComboBox, 2, 2)

        ctrllayout.addWidget(addComp, 3, 1)
        ctrllayout.addWidget(remComp, 3, 2)
        ctrllayout.addWidget(addxy, 4, 1)
        ctrllayout.addWidget(remxy, 4, 2)
        ctrllayout.addWidget(addSample, 5, 1)
        ctrllayout.addWidget(remSample, 5, 2)
        
        ctrlbottomlayout=QHBoxLayout()
        ctrlbottomlayout.addWidget(fomComboBoxLabel)
        ctrlbottomlayout.addWidget(self.fomComboBox)
        ctrlbottomlayout.addWidget(fomplotoptsPushButton)
        ctrlbottomlayout.addWidget(filtersmpsPushButton)
        ctrllayout.addLayout(ctrlbottomlayout, 6, 0, 1, 3)
        
        self.browser = QTextBrowser()
        self.browser.setLineWrapMode(QTextEdit.NoWrap)
#        self.lineedit = self.addValuesComp
#        self.lineedit = QLineEdit("Type an expression and press Enter")
#        self.lineedit.selectAll()
#        self.connect(self.lineedit, SIGNAL("returnPressed()"),self.updateUi)


        
        mainlayout.addLayout(ctrllayout, 0, 0, 1, 2)

        mainlayout.addWidget(self.browser, 0, 2, 1, 2)
     
        
        xyctrllayout=QVBoxLayout()
        xyctrllayout.addWidget(xplotchoiceComboBoxLabel)
        xyctrllayout.addWidget(self.xplotchoiceComboBox)
        xyctrllayout.addWidget(yplotchoiceComboBoxLabel)
        xyctrllayout.addWidget(self.yplotchoiceComboBox)
        xyctrllayout.addWidget(xycolplotchoiceComboBoxLabel)
        xyctrllayout.addWidget(self.xycolplotchoiceComboBox)
        xyctrllayout.addLayout(xminmaxlayout)
        xyctrllayout.addLayout(yminmaxlayout)
        xyctrllayout.addWidget(self.overlayselectCheckBox)
        xyctrllayout.addWidget(customxylegendPushButton)
        mainlayout.addLayout(xyctrllayout, 0, 4, 1, 1)
        mainlayout.addWidget(self.plotw_xy, 0, 5, 1, 1)
        
        mainlayout.addWidget(self.plotw_plate, 1, 0, 1, 3)
        mainlayout.addWidget(self.plotw_stack, 1, 3, 1, 3)   
        
        pylab.figure()
        self.quat=QuaternaryPlot(pylab.gca())
        
        self.setLayout(mainlayout)
        self.resize(1700, 750)
        
        self.linefields=[('%d', 'Sample'), ('%.2f', 'x'), ('%.2f', 'y'), ('%.2f', 'A'), ('%.2f', 'B'), ('%.2f', 'C'), ('%.2f', 'D'), ('%d', 'code')]
        self.setupcomppermute(replot=False)
        #self.openPlateMap()
        #self.fom=None
        self.ternfacesdata=None
        
    def extractlist_dlistkey(self, k):
        return [d[k] for d in self.platemapdlist]
        
    def plot(self): #self.sampleselectinds
        
        if not self.fom is None:
            testfcn=lambda arr:numpy.logical_not(numpy.isnan(arr))
            if self.skipoutofrange[0]:
                testfcn=lambda arr:testfcn(arr)&(self.fom>=self.vmin)
            if self.skipoutofrange[1]:
                testfcn=lambda arr:testfcn(arr)&(self.fom<=self.vmax)
            inds=numpy.where(testfcn(self.fom))[0]
        
        #platemap plot
        self.plotw_plate.axes.cla()
        
        s_plate=20
        
        if self.fom is None:
            self.plotw_plate.axes.scatter(self.x, self.y, c=self.col, s=s_plate, marker='s', edgecolor='none')
            self.cbax_plate.axes.cla()
        else:
            m=self.plotw_plate.axes.scatter(self.x[inds], self.y[inds], c=self.fom[inds], s=s_plate, marker='s', cmap=self.cmap, norm=self.norm, edgecolor='none')
            cb=self.plotw_plate.fig.colorbar(m, cax=self.cbax_plate, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
            cb.set_label(self.fomkey, fontsize=18)
        for i in self.sampleselectinds:
            circ = pylab.Circle((self.x[i], self.y[i]), radius=1, edgecolor='r', facecolor='none')
            self.plotw_plate.axes.add_patch(circ)
        
        self.plotw_plate.axes.set_xlim(min(self.x)-3, max(self.x)+3)
        self.plotw_plate.axes.set_ylim(min(self.y)-3, max(self.y)+3)
        
        self.plotw_plate.fig.canvas.draw()
        
        #comp plot
        
        self.stackedplotsetup()
        permcomp=self.comp[:, self.comppermuteinds]
        self.cbax_stack.cla()
        if self.fom is None:
            fomcol=['k']*len(permcomp)
            for i in self.sampleselectinds:
                fomcol[i]='r'
            fomcol=numpy.array(fomcol)
            inds2=numpy.where(numpy.abs(permcomp.sum(axis=1)-1.)<0.02)[0]
            self.stackplotfcn(permcomp[inds2], fomcol[inds2], self.plotw_stack_stpl, s=8, edgecolors='none')
            self.ternfacesdata=(permcomp[inds2], fomcol[inds2], None)
        else:
            inds_inds=numpy.where(numpy.abs(permcomp[inds].sum(axis=1)-1.)<0.02)[0]
            inds2=inds[inds_inds]
            self.stackplotfcn(permcomp[inds2], self.fom[inds2], self.plotw_stack_stpl, s=8, edgecolors='none', cmap=self.cmap, norm=self.norm, cb=False)
            
            sm=cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
            sm.set_array(self.fom[inds2])
            cb=self.plotw_stack.fig.colorbar(sm, cax=self.cbax_stack, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
            
            #cb=self.plotw_stack.fig.colorbar(m, cax=self.cbax_plate, extend=self.extend))
            cb.set_label(self.fomkey, fontsize=18)

            self.ternfacesdata=(permcomp[inds2], self.fom[inds2], sm)
            
        self.plotw_stack.fig.canvas.draw()
        #browser text
        headline='\t'.join([k for fmtstr, k in self.linefields]+self.allfomkeys)
        selectsamplesstr='\n'.join([headline]+self.selectsamplelines)
        
        self.browser.setText(selectsamplesstr)

    def openternfacesplot(self):
        if self.ternfacesdata is None:
            print 'No data available for ternary faces plot'
            return
        comp, col, sm=self.ternfacesdata
        
        
        if not sm is None:
            tfwidget=ternaryfacesWidget(self.parent, comp, col, ellabels=self.ellabels, cmap=self.cmap, norm=self.norm)
            cb=tfwidget.plotw.fig.colorbar(sm, cax=tfwidget.cbax, extend=self.extend, format=autocolorbarformat((self.vmin, self.vmax)))
            cb.set_label(self.fomkey, fontsize=18)
        else:
            tfwidget=ternaryfacesWidget(self.parent, comp, col, ellabels=self.ellabels)
        tfwidget.exec_()
    
    def openbinlinesplot(self):
        if self.ternfacesdata is None or self.fom is None:
            print 'No data available for binary lines plot'
            return
        comp, col, sm=self.ternfacesdata
        
        widget=binarylinesWidget(self.parent, comp, col, ellabels=self.ellabels)
        widget.ax.set_ylabel(self.fomkey)
        widget.exec_()
        
    def plateclickprocess(self, coords_button_ax):
        if len(self.x)==0:
            return
        critdist=2.
        xc, yc, button, ax=coords_button_ax

        dist=((self.x-xc)**2+(self.y-yc)**2)**.5
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.updateinfo()

        if button==3:#right click
            self.addtoselectsamples()
        elif button==2:#center click
            self.remfromselectsamples()
        elif button==1:
            self.plotselect()

    def stackclickprocess(self, coords_button_ax):
        if len(self.x)==0:
            return
        critdist=.1
        xc, yc, button, ax=coords_button_ax
        if not ax in self.plotw_stack_axl:
            return
        i=self.plotw_stack_axl.index(ax)
        dclick=self.stackcompinterv*i
        bclick=yc*2./numpy.sqrt(3.)
        aclick=1.-xc-bclick/2.
        cclick=1.-aclick-bclick
        compclick=numpy.array([aclick, bclick, cclick, dclick])
        compclick[:3]*=1.-dclick
        
        permcomp=self.comp[:, self.comppermuteinds]
        
        dist=numpy.array([(((c-compclick)**2).sum())**.5 for c in permcomp])
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.updateinfo()

        if button==3:#right click
            self.addtoselectsamples()
        elif button==2:#center click
            self.remfromselectsamples()
        elif button==1:
            self.plotselect()
            
    def updateinfo(self):
        self.compLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['comps'][self.selectind]]))

        self.xyLineEdit.setText(','.join(['%.2f' %n for n in self.fomplotd['xy'][self.selectind]]))

        self.sampleLineEdit.setText('%d' %self.fomplotd['sample_no'][self.selectind])
    
    def plotselect(self):
        if len(self.datadlist)==0:
            return
        overlaybool=self.overlayselectCheckBox.isChecked()
        if not overlaybool:
            self.plotw_xy.axes.cla()
        xk=str(self.xplotchoiceComboBox.currentText())
        yk=str(self.yplotchoiceComboBox.currentText())
        if self.plotselect_usefombool:
            if self.xplotchoiceComboBox.currentIndex()==0 or self.yplotchoiceComboBox.currentIndex()==0:
                return
            plotfom_xy=[[d['fomd'][xk], d['fomd'][yk]] for d in self.datadlist if xk in d['fomd'].keys() and yk in d['fomd'].keys() and not numpy.isnan(d['fomd'][xk]*d['fomd'][yk])]
            if len(plotfom_xy)==0:
                return
            fomx, fomy=numpy.array(plotfom_xy).T
            self.plotw_xy.axes.plot(fomx, fomy, 'o',ms=2,mew=0)
        else:
            if self.xycolplotchoiceComboBox.currentIndex()==0:
                plotillumkey=None
            else:
                plotillumkey=str(self.xycolplotchoiceComboBox.currentText())
            d=self.datadlist[self.selectind]
            
            for k in [xk, yk, plotillumkey]:#loop through to check before reading file
                if k is None:
                    continue
                if not k in (d['rawkeys']+d['interkeys']):
                    print 'aborting because data key not available for this sample: ', k
                    return

            if d['raw_arrays'] is None:#open pck 
                f=open(d['p'], mode='r')
                dfile=pickle.load(f)
                f.close()
            else:#arrays already story in d
                dfile=d
            
            plotdata=[]
            for k in [xk, yk, plotillumkey]:
                if k is None:
                    continue
                if k in d['rawkeys']:
                    plotdata+=[dfile['raw_arrays'][k]]
                else:
                    plotdata+=[dfile['intermediate_arrays'][k]]
            

            #if all raw len then leave but if some interlen then take the rawlen and index down to interlen
            minlen=min([len(v) for v in plotdata])
            if minlen!=d['rawlen']:
                for count, v in enumerate(plotdata):
                    if len(v)==d['rawlen']:
                        plotdata[count]=v[d['rawselectinds']]
                        
            if self.fom is None:
                selfom=None
            else:
                selfom=self.fom[self.selectind]
            #lab='%d' %d['sample_no']***
            code=self.platemapdlist[self.platemapindswithdata[self.selectind]]['code']
            lab=self.customlegendfcn(d['sample_no'], self.ellabels, self.comp[self.selectind][self.comppermuteinds], code, selfom)
            self.plotw_xy.axes.plot(plotdata[0], plotdata[1], '.-', label=lab, markeredgecolor='none')
            
            autotickformat(self.plotw_xy.axes, x=1, y=1)

            if (not plotillumkey is None) and plotillumkey in d.keys() and not overlaybool:
                illuminds=numpy.where(plotdata[2])[0]
                self.plotw_xy.axes.plot(plotdata[0][illuminds], plotdata[1][illuminds], 'y.', markeredgecolor='none')
            
            leg=self.plotw_xy.axes.legend(loc=0)
            leg.draggable()
        
        self.plotw_xy.axes.set_xlabel(xk)
        self.plotw_xy.axes.set_ylabel(yk)
        for le, fcn in zip([self.xminmaxLineEdit, self.yminmaxLineEdit], [self.plotw_xy.axes.set_xlim, self.plotw_xy.axes.set_ylim]):
            vstr=str(le.text()).strip()
            if len(vstr)==0:
                continue
            try:
                a, b, c=vstr.partition(',')
                a=myeval(a.strip())
                c=myeval(c.strip())
                fcn(a, c)
            except:
                print 'problem with setting axes limits: ', vstr
                continue
        self.plotw_xy.fig.canvas.draw()
        
    def sampleline_ind(self):
        plated=self.platemapdlist[self.platemapindswithdata[self.selectind]]
        s='\t'.join([fmtstr %plated[k] for fmtstr, k in self.linefields])
        if len(self.datadlist)>0:
            fomd=self.datadlist[self.selectind]['fomd']
            s+='\t'+'\t'.join([(((k in fomd.keys()) and ('%.3e' %fomd[k], )) or ('',))[0] for k in self.allfomkeys])
        return s
        
    def addtoselectsamples(self, plot=True):# self.selectind
        if self.selectind in self.sampleselectinds:
            return
        self.sampleselectinds+=[self.selectind]
        self.selectsamplelines+=[self.sampleline_ind()]
        if plot:
            self.plot()#would be nice to only have to plot overlay of selected samples
    
    def setupcomppermute(self, replot=True):
        elstrlist=str(self.elsLineEdit.text()).strip().split(',')
        elstrlist=[s.strip() for s in elstrlist]
        if len(elstrlist)<4:
            elstrlist=elstrlist+['A', 'B', 'C', 'D'][len(elstrlist):]
        elstrlist=elstrlist*2#for permute
        i=self.ternstackComboBox.currentIndex()
        self.ellabels=elstrlist[i:i+4]
        self.comppermuteinds=[0, 1, 2, 3, 0, 1, 2][i:i+4]
        if replot:
            self.stackedplotsetup()
            self.plot()

    
    def remfromselectsamples(self, plot=True):# self.selectind
        if not self.selectind in self.sampleselectinds:
            return
        i=self.sampleselectinds.index(self.selectind)
        self.sampleselectinds.pop(i)
        self.selectsamplelines.pop(i)
        if plot:
            self.plot()#would be nice to only have to plot overlay of selected samples
    
    def stackedplotsetup(self):
        a=numpy.array(self.extractlist_dlistkey('A'))
        asort=numpy.argsort(a)
        a=a[asort]
        try:
            a=a([self.code==0][asort])
        except:
            pass
        adiffall=(a[1:]-a[:-1])
        adiff=(adiffall[adiffall>.001]).mean()
        abcd=numpy.column_stack(numpy.array(self.extractlist_dlistkey(ch)) for ch in ['A', 'B', 'C', 'D'] if len(set(self.extractlist_dlistkey(ch)))>1)
        abcd=numpy.sum(abcd, axis=1)
        abcd=(abcd[abcd>0]).mean()
        adiff=adiff/abcd #rescale adiff by "thickness"
        nints=(1./adiff).round()
        intervopts=[5, 10, 20, 30, 100]
        intervchoice=intervopts[numpy.argmin((nints-numpy.array(intervopts))**2)]
        #print 'difference in A channel,  number of a intervals per 100% and stacked plot choice are:',  adiff, nints, intervchoice
        if intervchoice==100:
            makefcn=make9of100ternaxes
            self.stackplotfcn=scatter_9of100axes
        elif intervchoice==5:
            makefcn=make5ternaxes
            self.stackplotfcn=scatter_5axes
        elif intervchoice==10:
            makefcn=make10ternaxes
            self.stackplotfcn=scatter_10axes
        elif intervchoice==20:
            makefcn=make20ternaxes
            self.stackplotfcn=scatter_20axes
        elif intervchoice==30:
            makefcn=make30ternaxes
            self.stackplotfcn=scatter_30axes

        self.stackcompinterv=1./intervchoice
        self.plotw_stack.fig.clf()
        self.plotw_stack_axl, self.plotw_stack_stpl=makefcn(fig=self.plotw_stack.fig, ellabels=self.ellabels)
        self.cbax_stack=self.plotw_stack.fig.add_axes(self.plotw_stack_cbaxrect)

    
    def loadPckKeys(self, p, keys=None):
        try:
            f=open(p, mode='r')
            d=pickle.load(f)
            f.close()
            if keys is None:
                keys=d.keys()
            return [d[k] for k in keys]
        except:
            return None
    
    def initprepnewdatafile(self, smp):
        smp=int(round(smp))
        if smp in self.smplist:
            ind=self.smplist.index(smp)
            d=self.datadlist[ind]
        else:
            d={}
            d['sample_no']=smp
            i=self.platemapsmplist.index(smp)
            d['platemapind']=i
            d['p']=''#this path only used for reading arrays from disc so only put a path here if necesasary
            d['rawkeys']=[]
            d['raw_arrays']={}
            d['interkeys']=[]
            d['fomd']={}
            d['fomkeys']=[]
            d['rawlen']=None
            self.platemapindswithdata+=[i]
            self.smplist+=[smp]
            self.datadlist+=[d]

            
        return d #d passed by reference 
        
    def openDataFolder(self):
        #p='C:/Users/Gregoire/Documents/demodata/v2'
        p=mygetdir(parent=self, markstr='select folder with .pck files and/or .txt,.opt,.smp,.csv ascii files')
        #p='C:/Users/Gregoire/Documents/CaltechWork/echemuvvis/photoanodes/temp'
        if p is None or p=='':
            return
        self.folderLineEdit.setText(p)
        self.platemapindswithdata=[]
        self.smplist=[]
        self.allfomkeys=[]
        self.allarrkeys=[]
        self.datadlist=[]
        for fn in os.listdir(p):
            if fn.endswith('.txt') or fn.endswith('.opt') or fn.endswith('.smp') or fn.endswith('.csv'):
                if fn.endswith('.csv'):
                    delim=','
                else:
                    delim='\t'
                p2=os.path.join(p, fn)
                smp, dtxt=smp_dict_generaltxt(p2, delim=delim)
                #forcerror
                if smp is None:#FOM txt file, no array but many samples and foms
                    smpk=[k for k in ['sample_no', 'Sample No', 'Sample'] if k in dtxt.keys()]
                    if len(smpk)==0:
                        print 'invalid text file ', p2
                        continue
                    smpk=smpk[0]
                    for count, smp in enumerate(dtxt[smpk]):
                        if not smp in self.platemapsmplist:
                            continue
                        d=self.initprepnewdatafile(smp)
                        for k, v in dtxt.iteritems():
                            d['fomd'][k]=v[count]
                            d['fomkeys']+=[k]
                        self.allfomkeys+=[k for k in d['fomkeys'] if not k in self.allfomkeys]
                        
                else:#raw data txt file, 1 sample
                    if not smp in self.platemapsmplist:
                        continue
                        
                    d=self.initprepnewdatafile(smp)
                    if d['rawlen'] is None:
                        d['rawlen']=len(dtxt[dtxt.keys()[0]])
                    elif d['rawlen']!=len(dtxt[dtxt.keys()[0]]):# there was already a fiel ready previously that set the rawlen and this is incompatible
                        print 'skipping raw on ', p2, 'because wrong rawlen'
                        continue
                    
                    if not d['raw_arrays'] is None:
                        for k, v in dtxt.iteritems():
                            d['raw_arrays'][k]=v
                            d['rawkeys']+=[k]
                    
                    self.allarrkeys+=[k for k in d['rawkeys'] if not k in self.allarrkeys]

            elif fn.endswith('.pck'):#from here on out, pck file = 1 sample with both arrays and fom, must have rawd with an array inside
                
                p2=os.path.join(p, fn)
                tup=self.loadPckKeys(p2, keys=['measurement_info', "fom", 'raw_arrays', 'intermediate_arrays'])
                if tup is None:
                    print 'error with format of ', p
                    continue
                infod, fomd, rawd, interd=tup
                temp=[infod[k] for k in ['sample_no', 'Sample No', 'Sample'] if k in infod.keys()]
                if len(temp)==0 or not temp[0] in self.platemapsmplist:
                    print 'error with sample_no. ', temp
                    #raise
                    continue
                smp=temp[0]
                infod['sample_no']=smp
                
                d=self.initprepnewdatafile(smp)

                for k, v in infod.iteritems():
                    d[k]=v
                for k, v in fomd.iteritems():
                    d['fomd'][k]=v
                    d['fomkeys']+=[k]
                self.allfomkeys+=[k for k in d['fomkeys'] if not k in self.allfomkeys]
                
                d['p']=p2#this path used to eread arrays on the fly later
                
                for v in rawd.itervalues():
                    if isinstance(v, numpy.ndarray) and v.ndim==1:
                        rl=len(v)
                        break
                
                if d['rawlen'] is None:
                    d['rawlen']=rl
                    d['interlen']=rl
                elif d['rawlen']!=rl: #got the fom's added but rawlen was set by somethign previous and this isn't it. could allow inter but too copmlicated
                    print 'skipping raw/inter on ', p2, 'because wrong rawlen'
                    continue
                d['rawkeys']+=[k for k, v in rawd.iteritems() if isinstance(v, numpy.ndarray) and len(v)==d['rawlen']]
                d['raw_arrays']=None#triggers read array on fly later
                if 'rawselectinds' in interd.keys():
                    d['interlen']=len(interd['rawselectinds'])
                    d['rawselectinds']=interd['rawselectinds']

                d['interkeys']+=[k for k, v in interd.iteritems() if isinstance(v, numpy.ndarray) and (len(v)==d['interlen'] or len(v)==d['rawlen'])]
                #don't filter fom keys, assume the values are scalars
                self.allarrkeys+=[k for k in d['rawkeys']+d['interkeys'] if not k in self.allarrkeys]
            else:
                continue
#here the platemap is sorted to the data 
        
        self.allfomkeys.sort()
        self.allarrkeys.sort()
        for sortkey in ['Wavelength(nm)', 't(s)']:
            if sortkey in self.allarrkeys:
                self.allarrkeys=[self.allarrkeys.pop(self.allarrkeys.index(sortkey))]+self.allarrkeys
        self.x=numpy.array(self.extractlist_dlistkey('x'))[self.platemapindswithdata]
        self.y=numpy.array(self.extractlist_dlistkey('y'))[self.platemapindswithdata]
        self.col=numpy.array(self.extractlist_dlistkey('col'))[self.platemapindswithdata]
        self.comp=numpy.array(self.extractlist_dlistkey('comp'))[self.platemapindswithdata]
        
        self.fomComboBox.clear()
        self.fomComboBox.insertItem(0, 'composition/selected')
        for i, l in enumerate(self.allfomkeys):
            self.fomComboBox.insertItem(i+1, l)
        
        self.xplotchoiceComboBox.clear()
        self.yplotchoiceComboBox.clear()
        self.xycolplotchoiceComboBox.clear()
        
        self.xycolplotchoiceComboBox.insertItem(0, 'none')
        self.xycolplotchoiceComboBox.setCurrentIndex(0)
        self.plotselect_usefombool=len(self.allarrkeys)==0
        if self.plotselect_usefombool:
            self.xplotchoiceComboBox.insertItem(0, 'none')
            self.yplotchoiceComboBox.insertItem(0, 'none')
            self.xplotchoiceComboBox.setCurrentIndex(0)
            self.yplotchoiceComboBox.setCurrentIndex(0)
            for count, k in enumerate(self.allfomkeys):
                self.xplotchoiceComboBox.insertItem(count+1, k)
                self.yplotchoiceComboBox.insertItem(count+1, k)
        else:
            for count, k in enumerate(self.allarrkeys):
                self.xplotchoiceComboBox.insertItem(count, k)
                self.yplotchoiceComboBox.insertItem(count, k)
                self.xycolplotchoiceComboBox.insertItem(count+1, k)
            
            if len(self.allarrkeys)>0:
                self.xplotchoiceComboBox.setCurrentIndex(0)
            if len(self.allarrkeys)>1:
                self.yplotchoiceComboBox.setCurrentIndex(1)
            if 'Toggle' in self.allarrkeys:
                self.xycolplotchoiceComboBox.setCurrentIndex(self.allarrkeys.index('Toggle'))
            else:
                self.xycolplotchoiceComboBox.setCurrentIndex(0)
        self.sampleselectinds=[] #this is actually platemap select inds of the  already parsed inds in self.platemapindswithdata
        self.selectsamplelines=[]
        self.fomcolorselected()

    def openPlateMap(self):
        p=mygetopenfile(parent=self, markstr='select platemap .txt')
        #p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/0037-04-0730-mp.txt'
        #p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/0044-04-0820-mp.txt'
        #p='C:/Users/Gregoire/Documents/CaltechWork/platemaps/0028-04-0710-mp.txt'
        if p is None or p=='':
            return
        self.fileLineEdit.setText(p)

        self.platemapdlist=readsingleplatemaptxt(p)
        
        codesstr=str(self.codesLineEdit.text())
        if len(codesstr.strip())>0:
            try:
                self.filterbycodes=eval('['+codesstr+']')
                self.platemapdlist=[d for d in self.platemapdlist if d['code'] in self.filterbycodes]
            except:
                print 'error filtering by codes ', codesstr
        for d in self.platemapdlist:
            d['comp']=numpy.array([d[k] for k in ['A', 'B', 'C', 'D']])
            if d['comp'].sum()==0:
                col=numpy.array([.9, .9, .9])
            elif d['comp'].sum()!=1.:
                frac=d['comp'].sum()
                d['comp']/=frac
                
                col=self.quat.rgb_comp([d['comp']])[0]
#                if frac<1:
#                    col=self.quat.rgb_comp([d['comp']])[0]*frac
            else:
                col=self.quat.rgb_comp([d['comp']])[0]
            d['col']=col
            
        self.platemapsmplist=self.extractlist_dlistkey('Sample')
        
        
        #instead of open data folder clear options and plot the platemap
        #self.openDataFolder()#have to open new datafolder if open new platemap
        self.x=numpy.array(self.extractlist_dlistkey('x'))
        self.y=numpy.array(self.extractlist_dlistkey('y'))
        self.col=numpy.array(self.extractlist_dlistkey('col'))
        self.comp=numpy.array(self.extractlist_dlistkey('comp'))
        self.code=numpy.array(self.extractlist_dlistkey('code'))
        self.smplist=self.platemapsmplist
        
        self.stackedplotsetup()
        
        self.fomComboBox.clear()
        self.fomComboBox.insertItem(0, 'composition/selected')
        self.fomComboBox.setCurrentIndex(0)
        self.xplotchoiceComboBox.clear()
        self.yplotchoiceComboBox.clear()
        self.xycolplotchoiceComboBox.clear()
        
        self.datadlist=[]
        self.allfomkeys=[]
        self.allarrkeys=[]
        self.sampleselectinds=[] 
        self.selectsamplelines=[]
        self.platemapindswithdata=range(len(self.smplist))#until data folder is read, reat all samples as if they have data
        self.fomcolorselected() #this runs self.plot

    def fomcolorselected(self):
        if self.fomComboBox.currentIndex()==0 or len(self.datadlist)==0:
            self.fom=None
            if len(self.platemapindswithdata)>0:
                self.plot()
        else:
            k=str(self.fomComboBox.currentText())
            temp=numpy.array([(k in d['fomd'].keys() and (d['fomd'][k],) or (numpy.nan,))[0] for d in self.datadlist])
            if numpy.all(numpy.isnan(temp)):
                print k, ' is NaN for every sample. Cannot load that FOM'
                return
            self.fomraw=temp
            self.fom=copy.copy(self.fomraw)
            self.fomkey=k
            self.fommultstr='1.'
            fomnotnan=self.fom[numpy.logical_not(numpy.isnan(self.fom))]
            self.vmin=fomnotnan.min()
            self.vmax=fomnotnan.max()
            self.rev_cols=None
            self.editfomopts(dflt=True)
            
        

    def editfomopts(self, dflt=False):
        if self.fom is None:
            return
        if not dflt:
            fomoptswidget=fomplotoptions(self.parent, vmin=self.vmin, vmax=self.vmax, rev_cols=self.rev_cols, fomkey=self.fomkey, fommultstr=self.fommultstr)
            fomoptswidget.exec_()
            self.rev_cols=fomoptswidget.rev_cols
            self.vmin=fomoptswidget.vmin
            self.vmax=fomoptswidget.vmax
            self.cmap=fomoptswidget.cmap
            self.fomkey=fomoptswidget.fomkey
            self.fommultstr=fomoptswidget.fommultstr
            self.fom=self.fomraw*fomoptswidget.fommult
        if dflt or fomoptswidget.error:
            self.cmap=cm.jet
            self.skipoutofrange=[False, False]

        
        self.norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=False)
        
        if numpy.any(self.fom>self.vmax):
            if numpy.any(self.fom<self.vmin):
                self.extend='both'
            else:
                self.extend='max'
        elif numpy.any(self.fom<self.vmin): 
            self.extend='min'
        else:
            self.extend='neither'
        if len(self.platemapindswithdata)>0:
            self.plot()
    
    def filtersmpbyfom(self):
        if self.fom is None:
            if len(self.comp)==0:
                return
            selectinds=set(range(len(self.comp)))
            for el, compind in zip(self.ellabels, self.comppermuteinds):
                arr=self.comp[:, compind]
                filtsmpswidget=filtersampleswidget(self.parent, title='filter for element %s' %el, arr=arr, minval=0., maxval=1.01, minmaxfmt='%.2f')
                filtsmpswidget.exec_()
                selectinds=selectinds.intersection(filtsmpswidget.selectinds)
            selectinds=list(selectinds)
            selectinds.sort()
        else:
            filtsmpswidget=filtersampleswidget(self.parent, title='filter for selected fom', arr=self.fom)
            filtsmpswidget.exec_()
            selectinds=filtsmpswidget.selectinds
        lastind=len(selectinds)-1
        for count, i in enumerate(selectinds):
            self.selectind=i
            self.addtoselectsamples(plot=(count==lastind))
    
    def getcustomlegendfcn(self):
        widg=legendformatwidget(self.parent, arr=self.fom)
        widg.exec_()
        self.customlegendfcn=widg.genlegfcn
        
        
    def addValuesSample(self, remove=False):
        sampleNostr = str(self.sampleLineEdit.text())

        try:
            if ',' in sampleNostr:
                sampleNolist=eval('['+sampleNostr+']')
                inds=[self.smplist.index(n) for n in sampleNolist if n in self.smplist]
            else:
                sampleNo=int(eval(sampleNostr.strip()))
                inds=[self.smplist.index(sampleNo)]
        except:
            print 'error adding samples'
            return
        for i in inds:
            self.selectind=i
            if remove:
                self.remfromselectsamples()
            else:
                self.addtoselectsamples()
    
    def remValuesSample(self):
        self.addValuesSample(remove=True)
        
    def addValuesComp(self, remove=False):
        compstr = str(self.compLineEdit.text())
        codesstr=str(self.codesLineEdit.text())
        if len(codesstr.strip())>0:
            try:
                filterbycodes=eval('['+codesstr+']')
            except:
                print 'error filtering by codes ', codesstr
        else:
            filterbycodes=None
        try:
            abcd=numpy.array(eval('['+compstr.strip()+']'))
            if abcd.sum()<=0.:
                raise
            abcd/=abcd.sum()
            distarr=numpy.array([((comp-abcd)**2).sum() for comp in self.comp])
            inds=numpy.where(distarr==distarr.min())[0]
            inds=[i for i in inds if filterbycodes is None or self.code[i] in filterbycodes]
        except:
            print 'error adding samples'
            return
        for i in inds:
            plotbool=(i==inds[-1])
            self.selectind=i
            if remove:
                self.remfromselectsamples(plot=plotbool)
            else:
                self.addtoselectsamples(plot=plotbool)
        
#        try:
#            s=unicode(self.compLineEdit.text())
#            self.browser.append("%s = <b>%s</b>" % (s, eval('['+s+']')))
#        except:
#            self.browser.append("<font color=red>%s is invalid!</font>" %s)
#            print 'Need to write a set of compositions'
    def remValuesComp(self):
        self.addValuesComp(remove=True)
#        try:
#            s=unicode(self.compLineEdit.text())
#            print "try"
#            self.browser.cut(s)
#        except:
#            print 'Need to write a set of x&y coordinates'
    def addValuesXY(self, remove=False):
        xystr = str(self.xyLineEdit.text())
        try:
            xy=numpy.array(eval('['+xystr.strip()+']'))
            i=numpy.argmin(numpy.array([((numpy.array([x, y])-xy)**2).sum() for x, y in zip(self.x, self.y)]))
        except:
            print 'error adding samples'
            return
        self.selectind=i
        if remove:
            self.remfromselectsamples()
        else:
            self.addtoselectsamples()
#        try:
#            xy=unicode(self.xyLineEdit.text())
#            self.browser.append("%s = <b>%s</b>" % (xy, eval('['+xy+']')))
#        except:
#            self.browser.append("<font color=red>%s is invalid!</font>" %s)
#            print 'Need to write a set of x&y coordinates'
            
    def remValuesXY(self):
        self.addValuesXY(remove=True)
#        try:
#            xy=unicode(self.xyLineEdit.text())
#            self.browser.clear(xy)
#        except:
#            print 'Need to write a set of x&y coordinates'
            
        
    def writesamplelist(self, p=None):#not implemented yet
        self.statusLineEdit.setText('writing file')
        idstr=str(self.selectsamplesLineEdit.text()).split(',')
        try:
            ids=[int(myeval(s.strip())) for s in idstr]
        except:
            print 'data conversion problem for this list of strings:', idstr
            return
        if len(ids)==0:
            print 'no data to save'
            return

        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt' )
        elif os.path.isdir(p):
            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
            print p
        if not p:
            print 'save aborted'
            return
        ids=list(set(ids))
        ids.sort()
        savestr='\n'.join([`n` for n in ids])
        
        f=open(p, mode='w')
        f.write(savestr)
        f.close()
        
    def savefomcsv(self, p=None):
        if len(self.datadlist)==0 or len(self.allfomkeys)==0:
            print 'no data to save'
            return
        selkeyswidget=selectexportfom(self.parent,  self.allfomkeys)
        if not selkeyswidget.exec_():
            return
        savestr=createcsvfilstr(self.datadlist, selkeyswidget.selectkeys)
        
        if p is None:
            p=mygetsavefile(parent=self, markstr='save .csv fom file', filename='.csv' )
        if not p:
            print 'save aborted'
            return
            
        f=open(p, mode='w')
        f.write(savestr)
        f.close()
        


def readsingleplatemaptxt(p, returnfiducials=False):
    f=open(p, mode='r')
    ls=f.readlines()
    f.close()
    if returnfiducials:
        s=ls[0].partition('=')[2].partition('mm')[0].strip()
        if not ',' in s[s.find('('):s.find(')')]: #needed because sometimes x,y in fiducials is comma delim and sometimes not
            print 'WARNING: commas inserted into fiducials line to adhere to format.'
            print s
            s=s.replace('(   ', '(  ',).replace('(  ', '( ',).replace('( ', '(',).replace('   )', '  )',).replace(',  ', ',',).replace(', ', ',',).replace('  )', ' )',).replace(' )', ')',).replace('   ', ',',).replace('  ', ',',).replace(' ', ',',)
            print s
        fid=eval('[%s]' %s)
        fid=numpy.array(fid)
    for count, l in enumerate(ls):
        if not l.startswith('%'):
            break
    keys=ls[count-1][1:].split(',')
    keys=[(k.partition('(')[0]).strip() for k in keys]
    dlist=[]
    for l in ls[count:]:
        sl=l.split(',')
        d=dict([(k, myeval(s.strip())) for k, s in zip(keys, sl)])
        dlist+=[d]
    if returnfiducials:
        return dlist, fid
    return dlist

def myeval(c):
    if c=='None':
        c=None
    elif c=='nan' or c=='NaN':
        c=numpy.nan
    else:
        temp=c.lstrip('0')
        if (temp=='' or temp=='.') and '0' in c:
            c=0
        else:
            c=eval(temp)
    return c



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.visdataui=visdataDialog(self, title='Visualize Raw, Intermediate and FOM data', **kwargs)
            if execute:
                self.visdataui.exec_()                
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
