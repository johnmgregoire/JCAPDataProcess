import string
from PyQt5.QtWidgets import *

# import time
import os, os.path  # , shutil
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import matplotlib

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# try:
#    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QTAgg as NavigationToolbar
# except ImportError:
#    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure
# import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm

# import matplotlib.mlab as mlab
# import pylab
# import pickle
# __file__=r'D:\Google Drive\Documents\PythonCode\JCAP\JCAPDataProcess\CalcFOMApp.py'
projectpath = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath, "QtForms"))
sys.path.append(os.path.join(projectpath, "AuxPrograms"))
sys.path.append(os.path.join(projectpath, "OtherApps"))
sys.path.append(os.path.join(projectpath, "AnalysisFunctions"))
from fcns_math import *
from fcns_io import *
from fcns_ui import *
from csvfilewriter import createcsvfilstr_bare
from CalcFOMForm import Ui_CalcFOMDialog
from SaveButtonForm import Ui_SaveOptionsDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions


from Analysis_Master import calcfom_analyzedata_calcfomdialogclass, gethighestanak
from CA_CP_basics import *
from CV_photo import *
from OpenFromInfoApp import openfrominfoDialog
from xrfs_basics import *
from FOM_process_basics import *
from FOM_process_merge import *
from import_scipy_foruvis import *
from eche_spectral import Analysis__SpectralPhoto
from ecms import (
    Analysis__ECMS_Time_Join,
    Analysis__ECMS_Calibration,
    Analysis__ECMS_Fit_MS,
)

AnalysisClasses = [
    Analysis__Imax(),
    Analysis__Imin(),
    Analysis__Ifin(),
    Analysis__Efin(),
    Analysis__EchemMinMax(),
    Analysis__Etafin(),
    Analysis__Iave(),
    Analysis__Eave(),
    Analysis__Etaave(),
    Analysis__Iphoto(),
    Analysis__Ephoto(),
    Analysis__Etaphoto(),
    Analysis__E_Ithresh(),
    Analysis__Eta_Ithresh(),
    Analysis__Pphotomax(),
    Analysis__SpectralPhoto(),
    Analysis__TR_UVVIS(),
    Analysis__BG(),
    Analysis__T_UVVIS(),
    Analysis__DR_UVVIS(),
    Analysis__XRFS_EDAX(),
    Analysis__PlatemapComps(),
    Analysis__ECMS_Time_Join(),
    Analysis__ECMS_Calibration(),
    Analysis__Iphotothresh(),
]
FOMProcessClasses = [
    Analysis__AveCompDuplicates(),
    Analysis__Process_XRFS_Stds(),
    Analysis__FOM_Merge_Aux_Ana(),
    Analysis__FOM_Merge_PlatemapComps(),
    Analysis__FOM_Interp_Merge_Ana(),
    Analysis__Filter_Linear_Projection(),
    Analysis__Process_B_vs_A_ByRun(),
    Analysis__ECMS_Fit_MS(),
    Analysis__FilterSmoothFromFile(),
]  # Analysis__FilterSmoothFromFile must always be last because it is referred to with index -1 in the code
# NumNonPckBasedFilterSmooth=len(FOMProcessClasses)
DEBUGMODE = False
for ac in AnalysisClasses + FOMProcessClasses:
    ac.debugmode = DEBUGMODE
GUIMODE = True  # when running this program all the classes will default to True and then if writing a batch script, need to turn gui_mode_bool to False
for ac in AnalysisClasses + FOMProcessClasses:
    ac.gui_mode_bool = GUIMODE


class SaveOptionsDialog(QDialog, Ui_SaveOptionsDialog):
    def __init__(self, parent, dflt):
        super(SaveOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.dfltButton.setText(dflt)
        button_fcn = [
            (self.dfltButton, self.dflt),
            (self.tempButton, self.temp),
            (self.browseButton, self.browse),
            (self.cancelButton, self.cancel),
        ]
        # (self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            button.pressed.connect(fcn)
        self.choice = dflt

    def dflt(self):
        self.close()

    def temp(self):
        self.choice = "temp"
        self.close()

    def browse(self):
        self.choice = "browse"
        self.close()

    def cancel(self):
        self.choice = ""
        self.close()


class calcfomDialog(QDialog, Ui_CalcFOMDialog):
    def __init__(
        self,
        parent=None,
        title="",
        folderpath=None,
        modifyanainplace=False,
        guimode=GUIMODE,
    ):
        super(calcfomDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.guimode = guimode
        if guimode != GUIMODE:
            for ac in AnalysisClasses + FOMProcessClasses:
                ac.gui_mode_bool = guimode
        #        self.echem30=echem30axesWidget()
        #        self.echem30.show()
        self.plotillumkey = None
        self.modifyanainplace = modifyanainplace
        self.dbdatasource = 0
        self.techniquedictlist = []
        self.plotwsetup()
        if guimode:
            button_fcn = [
                (self.BatchPushButton, self.runbatchprocess),
                (self.ImportExpPushButton, self.importexp),
                (self.ImportAnaPushButton, self.importana),
                (self.OpenInfoPushButton, self.importfrominfo),
                (self.EditAnalysisParamsPushButton, self.editanalysisparams),
                (self.AnalyzeDataPushButton, self.analyzedata),
                (self.ViewResultPushButton, self.viewresult),
                (self.SaveViewPushButton, self.saveview),
                (self.EditDfltVisPushButton, self.editvisparams),
                (self.SaveAnaPushButton, self.saveana),
                (self.ClearAnalysisPushButton, self.clearanalysis_pushbutton),
                (self.ClearSingleAnalysisPushButton, self.clearsingleanalysis),
                (self.ImportAnalysisParamsPushButton, self.importanalysisparams),
                (self.UpdatePlotPushButton, self.plotwithcaution),
                (self.OpenAuxExpAnaPushButton, self.openauxexpana),
                (self.RaiseErrorPushButton, self.raiseerror),
                (self.AttachMiscPushButton, self.attachfilestoana),
            ]
            # (self.UndoExpPushButton, self.undoexpfile), \
            for button, fcn in button_fcn:
                button.pressed.connect(fcn)
            self.UserFOMLineEdit.editingFinished.connect(self.updateuserfomd)
            self.RunSelectTreeWidget.itemChanged[QTreeWidgetItem, int].connect(
                self.runselectionchanged
            )
            self.ExpRunUseComboBox.activated["QString"].connect(self.fillruncheckboxes)
            # QObject.connect(self.TechTypeButtonGroup,SIGNAL("buttonClicked(QAbstractButton)"),self.fillanalysistypes)
            self.TechTypeButtonGroup.buttonClicked[QAbstractButton].connect(
                self.fillanalysistypes
            )
            self.AnalysisNamesComboBox.activated["QString"].connect(
                self.getactiveanalysisclass
            )
            self.FOMProcessNamesComboBox.activated["QString"].connect(
                self.getactiveanalysisclass
            )
            self.fomplotchoiceComboBox.activated["QString"].connect(
                self.plot_generatedata
            )
            self.CompPlotTypeComboBox.activated["QString"].connect(
                self.plot_generatedata
            )
            self.stdcsvplotchoiceComboBox.activated["QString"].connect(
                self.plot_preparestandardplot
            )
            self.usedaqtimeCheckBox.stateChanged.connect(self.plot_generatedata)
            self.AnaTreeWidget.itemDoubleClicked[QTreeWidgetItem, int].connect(
                self.edittreeitem
            )
        self.AnaTreeWidgetFcns = treeclass_anadict(self.AnaTreeWidget)
        self.runtreeclass = treeclass_anadict(self.RunSelectTreeWidget)
        self.paramsdict_le_dflt = dict(
            [
                ("access", [self.AccessLineEdit, "hte"]),
                ("name", [self.AnaNameLineEdit, "temp_eche_name"]),
                ("analysis_type", [self.AnaTypeLineEdit, "eche"]),
                ("created_by", [self.UserNameLineEdit, "eche"]),
                ("description", [self.AnaDescLineEdit, "null"]),
            ]
        )
        self.batchprocesses = [
            self.batch_processallana,
            self.batch_analyzethenprocess,
            self.batch_process_allsubspace,
            self.batch_analyzethenprocess_allsubspace,
            self.batch_analyze_fcn_same_techclass,
            self.batch_merge_atfrac_from_aux,
            self.batch_set_params_for_photo_mAcm2_scaling,
        ]
        batchdesc = [
            "Run Prcoess FOM on all present ana__x",
            "Run select Analysis and then Process",
            "FOM Process: all Sub-Space w/ same root name",
            "Run Analysis + Process all w/ same root name",
            "Run select Analysis on all similar techniques",
            "Merge AtFrac from an Aux ANA, each ana__",
            "setup parameters for scaling Iphoto to mAcm2",
        ]
        for i, l in enumerate(batchdesc):
            self.BatchComboBox.insertItem(i, l)
        self.getplatemapCheckBox.setChecked(True)
        self.exppath = "null"
        self.tempanafolder = ""
        self.expzipclass = None
        self.anafolder = None
        self.clearanalysis()
        self.updateuserfomd(clear=True)

    def raiseerror(self):
        raiseerror

    def updateuserfomd(self, clear=False):
        if clear:
            self.userfomd = {}
            self.UserFOMLineEdit.setText("")
            self.text_UserFOMLineEdit = ""
            return
        s = str(self.UserFOMLineEdit.text())
        if (
            self.text_UserFOMLineEdit == s
        ):  # "duplicate" signals being emitted so ignore them
            return
        self.text_UserFOMLineEdit = s
        vals = s.split(",")
        keys = ["user_ana_fom__%d" % i for i, v in enumerate(vals)]
        ans = []
        count = 0
        while ans != keys:
            inputs = [("key for %s" % v, str, k) for k, v in zip(keys, vals)]
            ans = userinputcaller(
                self, inputs=inputs, title="Enter user FOM keys", cancelallowed=True
            )
            if ans is None:
                return
            keys = [filterchars(k) for k in ans]
            count += 1
        vals = [attemptnumericconversion(v.strip()) for v in vals]
        self.userfomd = dict([(k, v) for k, v in zip(keys, vals)])

    def edittreeitem(self, item, column):
        self.editparams(self.AnaTreeWidget, item=item, column=column)

    def editparams(self, widget, item=None, column=0):
        if item is None:
            item = widget.currentItem()
        s = str(item.text(column))
        st = s.partition(": ")
        k = "".join(st[:2])
        v = st[2].strip()
        if len(v) == 0:
            print "Error editing param,  no value detected: ", s
            return
        ans = userinputcaller(
            self,
            inputs=[(k, str, v)],
            title="Enter new param value",
            cancelallowed=True,
        )
        if ans is None or ans[0].strip() == v:
            return
        ans = ans[0].strip()
        warningbool = True in [ws in k for ws in ["version"]]
        parent = item.parent()
        if parent is None:
            parentstr = ""
        else:
            parentstr = parent.text(0)
        warningbool = warningbool or True in [
            ws in parentstr or ws in k for ws in ["ana__", "parameters", "files_"]
        ]
        if warningbool:
            idialog = messageDialog(
                self,
                'THIS IS CONSIDERED A READ-ONLY PARAMETER.\nYOU SHOULD PROBABLY "Cancel"',
            )
            if not idialog.exec_():
                return
        item.setText(column, "".join([k, ans]))
        kl = [k.partition(":")[0].strip()]
        while not item.parent() is None:
            item = item.parent()
            kl = [str(item.text(0)).partition(":")[0].strip()] + kl
        d = self.anadict
        while len(kl) > 1:
            d = d[kl.pop(0)]
        d[kl[0]] = ans

    def openauxexpana(self, tryexp=True):
        msg = "Select .ana/.pck or containing .zip"
        if tryexp:
            msg += " - CANCEL FOR EXP"
        p = selectexpanafile(self, exp=False, markstr=msg)
        if len(p) > 0:
            self.importauxexpana(p, exp=False)
            return
        if tryexp:
            p = selectexpanafile(
                self, exp=True, markstr="Select .exp/.pck EXP file, or containing .zip"
            )
            if len(p) > 0:
                self.importauxexpana(p, exp=True)
        if len(p) == 0:  # cancelled out of everything so clear aux
            self.aux_exp_dlist = []
            self.aux_ana_dlist = []

    def importauxexpana(self, auxexpanapath, exp=False):
        ext_str = ".exp" if exp else ".ana"
        dlist = self.aux_exp_dlist if exp else self.aux_ana_dlist
        if not (
            auxexpanapath.endswith(ext_str)
            or auxexpanapath.endswith(".pck")
            or not os.path.isabs(auxexpanapath)
        ):
            auxexpanapath = (buildexppath if exp else buildanapath)(auxexpanapath)
        auxexpanadict = (
            readexpasdict(auxexpanapath, includerawdata=False, returnzipclass=True)
            if exp
            else readana(auxexpanapath, stringvalues=False, erroruifcn=None)
        )
        #        rp=os.path.split(auxexpanapath)[0]
        #        dbpath_folds=(EXPFOLDERS_J+EXPFOLDERS_L) if exp else (ANAFOLDERS_J+ANAFOLDERS_L)
        #        rp=compareprependpath(dbpath_folds, rp)
        #        auxexpanadict['auxexpanapath_relative']=rp.replace(chr(92),chr(47))
        rp = get_relative_path_for_exp_or_ana_full_path(
            os.path.split(auxexpanapath)[0], exp=exp
        )
        auxexpanadict["auxexpanapath_relative"] = rp
        auxexpanadict["auxexpanapath"] = auxexpanapath
        dlist += [auxexpanadict]
        ###do not save apths as top level key but instead gets saved when used in ana__ blocks, typically in params
        ###self.anadict['aux_exp_paths' if exp else 'aux_ana_paths']=','.join([d['auxexpanapath_relative'] for d in dlist])
        # update analysis function options
        self.updateana()  # fill analysis types to enable auxs-related fucntions will happen here

    def importexp(self, expfiledict=None, exppath=None, expzipclass=None, anadict=None):
        if expfiledict is None:
            if exppath is None:
                exppath = selectexpanafile(
                    self,
                    exp=True,
                    markstr="Select .exp/.pck EXP file, or containing .zip",
                )
            if len(exppath) == 0:
                return
            if not (
                exppath.endswith(".exp")
                or exppath.endswith(".pck")
                or not os.path.isabs(exppath)
            ):
                exppath = buildexppath(exppath)
            expfiledict, expzipclass = readexpasdict(
                exppath, includerawdata=False, erroruifcn=None, returnzipclass=True
            )
            if expfiledict is None:
                print "Problem opening EXP"
                return
        self.clearexp()
        self.exppath = exppath
        self.expfolder = os.path.split(exppath)[0]
        self.expfiledict = expfiledict
        if self.expzipclass:
            self.expzipclass.close()
        self.expzipclass = expzipclass
        self.FilterSmoothMapDict = {}
        if "experiment_type" in expfiledict.keys():
            for runk, rund in self.expfiledict.items():
                if (
                    runk.startswith("run__")
                    and "parameters" in rund.keys()
                    and isinstance(rund["parameters"], dict)
                    and not "technique_name" in rund["parameters"].keys()
                ):
                    rund["parameters"]["technique_name"] = expfiledict[
                        "experiment_type"
                    ]
        if self.getplatemapCheckBox.isChecked():
            for runk, rund in self.expfiledict.items():
                if runk.startswith("run__") and not "platemapdlist" in rund.keys():
                    if not (
                        "parameters" in rund.keys()
                        and isinstance(rund["parameters"], dict)
                    ):
                        rund["parameters"] = {}
                    if (
                        not "plate_id" in rund["parameters"].keys()
                    ):  # this handles when plate_id only specified at top of file and not in run params, requires there only be 1 plate_id in the exp
                        if "plate_ids" in self.expfiledict.keys() and isinstance(
                            self.expfiledict["plate_ids"], int
                        ):  # integer means it got auto converted because wasn't a list
                            rund["parameters"]["plate_id"] = self.expfiledict[
                                "plate_ids"
                            ]
                    if "plate_id" in rund["parameters"].keys():
                        pmpath, pmidstr = getplatemappath_plateid(
                            str(rund["parameters"]["plate_id"]), return_pmidstr=True
                        )
                        if len(pmidstr) > 0:
                            for temprunk, temprund in self.expfiledict.iteritems():
                                if (
                                    temprunk.startswith("run__")
                                    and "platemap_id" in temprund.keys()
                                    and temprund["platemap_id"] == pmidstr
                                ):
                                    rund["platemapdlist"] = temprund[
                                        "platemapdlist"
                                    ]  # presumably share platemap by reference
                                    rund["platemap_id"] = pmidstr
                        if not "platemapdlist" in rund.keys():
                            rund["platemapdlist"] = readsingleplatemaptxt(
                                pmpath,
                                erroruifcn=lambda s: mygetopenfile(
                                    parent=self,
                                    xpath=PLATEMAPFOLDERS[0],
                                    markstr="Error: %s select platemap for plate_no %s"
                                    % (s, rund["parameters"]["plate_id"]),
                                ),
                            )
                    if len(pmidstr) > 0:
                        rund["platemap_id"] = pmidstr
                if runk.startswith("run__") and not "platemap_id" in rund.keys():
                    rund["platemap_id"] = userinputcaller(
                        self,
                        inputs=[("platemap id: ", str, "")],
                        title="Reading platemap failed. Enter map_id",
                        cancelallowed=False,
                    )[0]
            platemapids = [
                rund["platemap_id"]
                for runk, rund in self.expfiledict.iteritems()
                if runk.startswith("run__") and "platemap_id" in rund
            ]
            self.FilterSmoothMapDict = generate_filtersmoothmapdict_mapids(platemapids)
        self.paramsdict_le_dflt["analysis_type"][1] = self.expfiledict[
            "experiment_type"
        ]
        self.paramsdict_le_dflt["created_by"][1] = self.expfiledict["experiment_type"]
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            if k in ["analysis_type", "created_by"]:
                le.setText(dfltstr)
        self.clearanalysis(anadict=anadict)
        # rp=self.exppath.replace('.pck', '.exp')
        rp = os.path.split(self.exppath)[0]
        rp = compareprependpath(EXPFOLDERS_J + EXPFOLDERS_L, rp)
        self.anadict["experiment_path"] = rp.replace(chr(92), chr(47))
        print "active experiment_path is %s" % (self.anadict["experiment_path"])
        self.anadict["experiment_name"] = self.expfiledict["name"]
        if "access" in self.expfiledict.keys():
            self.anadict["access"] = self.expfiledict[
                "access"
            ]  # this will set access here and then not overwritten later
        self.fillexpoptions()
        self.expfilenameLineEdit.setText(self.exppath)

    def fillexpoptions(self):
        self.clearexp()
        self.runk_use = [
            (k, v["run_use"].partition("__")[0])
            for k, v in self.expfiledict.iteritems()
            if k.startswith("run__")
        ]
        self.uselist = list(set(map(operator.itemgetter(1), self.runk_use)))
        if "data" in self.uselist:
            temp = self.uselist.pop(self.uselist.index("data"))
            self.uselist = [temp] + self.uselist
        for i, k in enumerate(self.uselist):
            self.ExpRunUseComboBox.insertItem(i, k)
        self.ExpRunUseComboBox.setCurrentIndex(0)
        self.fillruncheckboxes()

    def fillruncheckboxes(self):
        self.runselectionaction = False
        self.usek = str(self.ExpRunUseComboBox.currentText())
        runklist = [runk for runk, usek in self.runk_use if usek == self.usek]
        d = dict(
            [
                (
                    "-".join(
                        [
                            runk,
                            self.expfiledict[runk]["description"]
                            if "description" in self.expfiledict[runk].keys()
                            else "",
                        ]
                    ),
                    dict(
                        [
                            (k, v)
                            for k, v in self.expfiledict[runk].iteritems()
                            if not k.startswith("platemap")
                        ]
                    ),
                )
                for runk in runklist
            ]
        )
        self.runtreeclass.filltree(d, startkey="")
        self.runtreeclass.maketoplevelchecked()
        self.filltechtyperadiobuttons()
        self.runselectionaction = True

    def runselectionchanged(self, item, column):
        if not self.runselectionaction:
            return
        if item.parent() is None:  # top level run
            self.filltechtyperadiobuttons()

    def filltechtyperadiobuttons(self, startind=0):
        qlist = self.TechTypeButtonGroup.buttons()
        numbuttons = len(qlist)
        for button in qlist:
            button.setText("")
            button.setToolTip("")
            button.setVisible(False)
        self.selectrunklist = self.runtreeclass.getlistofchecktoplevelitems()
        self.selectrunklist = [
            s.partition("-")[0]
            for s in self.selectrunklist
            if len(s.partition("-")[0]) > 0
        ]
        runk_techk = [
            (runk, techk)
            for runk in self.selectrunklist
            for techk in self.expfiledict[runk].keys()
            if techk.startswith("files_technique__")
        ]
        self.techk_typek = list(
            set(
                [
                    (techk.partition("files_technique__")[2], typek)
                    for runk, techk in runk_techk
                    for typek in self.expfiledict[runk][techk].keys()
                ]
            )
        )
        numfiles = [
            numpy.array(
                [
                    len(
                        self.expfiledict[runk]["files_technique__" + techk][
                            typek
                        ].keys()
                    )
                    for runk in self.selectrunklist
                    if "files_technique__" + techk in self.expfiledict[runk].keys()
                    and typek
                    in self.expfiledict[runk]["files_technique__" + techk].keys()
                ]
            ).sum(dtype="int32")
            for techk, typek in self.techk_typek
        ]
        if (
            len(self.techk_typek) == 0
        ):  # 201809fix to allow exp that don't have files, i.e. only paramaters. This doesn't allow exp to have a mix of run__ with and without files
            self.techk_typek = set(
                [
                    (
                        self.expfiledict[runk]["parameters"]["technique_name"],
                        self.expfiledict[runk]["parameters"]["technique_name"],
                    )
                    for runk in self.selectrunklist
                    if "parameters" in self.expfiledict[runk].keys()
                    and "technique_name" in self.expfiledict[runk]["parameters"].keys()
                ]
            )
            numfiles = [1] * len(self.techk_typek)
        temp_t_t = self.techk_typek
        numcanlist = numbuttons
        displaystrs = []
        if startind > 0:
            numcanlist -= 1
            temp_t_t = temp_t_t[startind:]
            numfiles = numfiles[startind:]
            displaystrs += ["Display 0-9"]
        if len(temp_t_t) > numcanlist:
            numcanlist -= 1
            temp_t_t = temp_t_t[:numcanlist]
            numfiles = numfiles[:numcanlist]
            displaystrs += ["Display %d-?" % (startind + numcanlist)]
        count = 0
        for nfiles, techk_typek in zip(numfiles, self.techk_typek):
            button = qlist[count]
            s = ",".join(techk_typek)
            button.setText(s)
            button.setToolTip("%d files" % (nfiles))
            button.setVisible(True)
            if count == 0:
                button.setChecked(True)
                self.fillanalysistypes(button)
            count += 1
        for s in displaystrs:
            button = qlist[count]
            button.setText(s)
            button.setVisible(True)
            count += 1

    def fillanalysistypes(self, button):
        if button is None:
            button = self.TechTypeButtonGroup.buttons()[0]
            button.setChecked(True)
        s = str(button.text())
        if s.startswith("Display "):
            i = int(s.partition("Display ")[2].partition("-")[0])
            filltechtyperadiobuttons(startind=i)
            return
        self.techk, garb, self.typek = s.partition(",")
        nfiles_classes = [
            len(
                c.getapplicablefilenames(
                    self.expfiledict,
                    self.usek,
                    self.techk,
                    self.typek,
                    runklist=self.selectrunklist,
                    anadict=self.anadict,
                    calcFOMDialogclass=self,
                )
            )
            for i, c in enumerate(AnalysisClasses)
        ]
        self.AnalysisClassInds = [i for i, nf in enumerate(nfiles_classes) if nf > 0]
        self.AnalysisNamesComboBox.clear()
        self.AnalysisNamesComboBox.insertItem(0, "")
        for count, i in enumerate(self.AnalysisClassInds):
            self.AnalysisNamesComboBox.insertItem(
                count + 1,
                AnalysisClasses[i].analysis_name + ("(%d)" % nfiles_classes[i]),
            )
            self.AnalysisNamesComboBox.setCurrentIndex(1)
        filternames = list(
            set([k for d in self.FilterSmoothMapDict.values() for k in d.keys()])
        )
        nfiles_classes = [
            len(
                c.getapplicablefilenames(
                    self.expfiledict,
                    self.usek,
                    self.techk,
                    self.typek,
                    runklist=self.selectrunklist,
                    anadict=self.anadict,
                    calcFOMDialogclass=self,
                )
            )
            for i, c in enumerate(FOMProcessClasses[:-1])
        ]
        self.FOMProcessClassInds = [i for i, nf in enumerate(nfiles_classes) if nf > 0]
        self.FOMProcessNamesComboBox.clear()
        self.FOMProcessNamesComboBox.insertItem(0, "use analysis function")
        for count, i in enumerate(self.FOMProcessClassInds):
            self.FOMProcessNamesComboBox.insertItem(
                count + 1,
                "%s(%s)"
                % (
                    FOMProcessClasses[i].analysis_name,
                    FOMProcessClasses[i].params["select_ana"],
                ),
            )
        if (
            len(FOMProcessClasses[-1].getapplicablefomfiles(self.anadict)) > 0
            and len(filternames) > 0
        ):
            for filtername in filternames:
                self.FOMProcessClassInds += [
                    -1
                ]  # each filtername from a .pck file uses the same analysis class
                count += 1
                self.FOMProcessNamesComboBox.insertItem(
                    count + 1,
                    "%s(%s)" % (filtername, FOMProcessClasses[-1].params["select_ana"]),
                )
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        self.getactiveanalysisclass()

    def getactiveanalysisclass(self):
        procselind = int(self.FOMProcessNamesComboBox.currentIndex())
        if procselind > 0:
            procclassind = self.FOMProcessClassInds[procselind - 1]
            self.analysisclass = FOMProcessClasses[procclassind]
            if procclassind == -1:  # filter from pck
                filtername = str(self.FOMProcessNamesComboBox.currentText()).partition(
                    "("
                )[
                    0
                ]  # write the filter_path__runint while handy here to use later
                self.analysisclass.filter_path__runint = dict(
                    [
                        (
                            int(runk.partition("__")[2]),
                            self.FilterSmoothMapDict[str(rund["platemap_id"])][
                                filtername
                            ],
                        )
                        for runk, rund in self.expfiledict.iteritems()
                        if runk.startswith("run__")
                    ]
                )
                if "__" in filtername:
                    self.analysisclass.params["platemap_comp4plot_keylist"] = ",".join(
                        list(filtername.partition("__")[2])
                    )
                else:
                    self.analysisclass.params[
                        "platemap_comp4plot_keylist"
                    ] = self.analysisclass.dfltparams["platemap_comp4plot_keylist"]
        else:
            selind = int(self.AnalysisNamesComboBox.currentIndex())
            if selind == 0:
                self.analysisclass = None
                return
            self.analysisclass = AnalysisClasses[self.AnalysisClassInds[selind - 1]]
        # self.activeana=None
        le, dflt = self.paramsdict_le_dflt["description"]
        s = filterchars(
            str(le.text()),
            valid_chars="-_.; ()%s%s" % (string.ascii_letters, string.digits),
        )
        if ";" in s:
            s = s.partition(";")[0]
            newdflt = "; ".join([s, self.analysisclass.description])
        else:
            newdflt = self.analysisclass.description
        le.setText(newdflt)
        self.paramsdict_le_dflt["description"][1] = newdflt

    def clearexp(self):
        self.ExpRunUseComboBox.clear()
        self.RunSelectTreeWidget.clear()
        self.plotd = {}
        self.expfilenameLineEdit.setText("")

    def runbatchprocess(self):
        self.batchprocesses[self.BatchComboBox.currentIndex()]()

    def importfrominfo(self):
        idialog = openfrominfoDialog(self, runtype="", exp=True, ana=False, run=False)
        idialog.exec_()
        if idialog.selecttype == "ana":
            self.importana(p=idialog.selectpath)
        if idialog.selecttype == "exp":
            self.importexp(exppath=idialog.selectpath)

    def importana(self, p=None):
        if p is None:
            p = selectexpanafile(
                self, exp=False, markstr="Select .ana/.pck to import, or .zip file"
            )
        if len(p) == 0:
            return
        anadict = readana(
            p, stringvalues=True, erroruifcn=None
        )  # don't allow erroruifcn because dont' want to clear temp ana folder until exp successfully opened and then clearanalysis and then copy to temp folder, so need the path defintion to be exclusively in previous line
        anadict["description"] = "; loaded from %s -> %s" % (
            anadict["name"],
            anadict["description"],
        )
        if not "experiment_path" in anadict.keys():
            return
        #        if anadict['ana_version']!='3':
        #            idialog=messageDialog(self, '.ana version %s is different from present. continue?' %anadict['ana_version'])
        #            if not idialog.exec_():
        #                return
        exppath = buildexppath(
            anadict["experiment_path"]
        )  # this is the place an experiment folder is turned into an exp fiel path so for the rest of this App exppath is the path of the .exp file
        expfiledict, expzipclass = readexpasdict(
            exppath, includerawdata=False, returnzipclass=True
        )
        if len(expfiledict) == 0:
            idialog = messageDialog(self, "abort .ana import because fail to open .exp")
            idialog.exec_()
            return
        # self.anadict=anadict
        if p.endswith(".ana") or p.endswith(".pck"):
            self.anafolder = os.path.split(p)[0]
        else:
            self.anafolder = p
        self.importexp(
            expfiledict=expfiledict,
            exppath=exppath,
            expzipclass=expzipclass,
            anadict=anadict,
        )  # clearanalysis happens here and anadcit is ported into self.anadict in the clearanalysis
        if not self.modifyanainplace:
            copyanafiles(self.anafolder, self.tempanafolder)
        self.updateana()
        print self.anadict.keys()

    def editanalysisparams(self):
        if self.analysisclass is None or len(self.analysisclass.params) == 0:
            return
        keys_paramsd = [
            k for k, v in self.analysisclass.params.iteritems() if isinstance(v, dict)
        ]
        if len(keys_paramsd) == 0:
            self.editanalysisparams_paramsd(self.analysisclass.params)
            return
        else:
            keys_paramsd = ["<non-nested params>"] + keys_paramsd
        i = userselectcaller(
            self, options=keys_paramsd, title="Select type of parameter to edit"
        )
        if i == 0:
            self.editanalysisparams_paramsd(self.analysisclass.params)
        else:
            self.editanalysisparams_paramsd(self.analysisclass.params[keys_paramsd[i]])

    def editanalysisparams_paramsd(self, paramsd):
        inputs = [
            (k, type(v), (isinstance(v, str) and (v,) or (str(v),))[0])
            for k, v in paramsd.iteritems()
            if not isinstance(v, dict)
        ]
        if len(inputs) == 0:
            return
        ans = userinputcaller(
            self,
            inputs=inputs,
            title="Enter Calculation Parameters",
            returnchangedbool=True,
        )
        if ans is None:
            return
        ans, changedbool = ans
        somethingchanged = False
        for (k, tp, v), newv, chb in zip(inputs, ans, changedbool):
            if chb:
                paramsd[k] = newv
                somethingchanged = True
        if (
            somethingchanged
        ):  # soem analysis classes have different files applicable depending on user-enter parameters so update here but don't bother deleting if numfiles goes to 0
            self.processeditedparams()

    def processeditedparams(self):
        if "process_fom" in self.analysisclass.getgeneraltype():
            # processnewparams happens in getapplicablefilenames
            self.analysisclass.getapplicablefilenames(
                self.expfiledict,
                self.usek,
                self.techk,
                self.typek,
                runklist=self.selectrunklist,
                anadict=self.anadict,
                calcFOMDialogclass=self,
            )
            selind = int(self.FOMProcessNamesComboBox.currentIndex())
            self.FOMProcessNamesComboBox.setItemText(
                selind,
                "%s(%s)"
                % (
                    str(self.FOMProcessNamesComboBox.currentText()).partition("(")[0],
                    self.analysisclass.params["select_ana"],
                ),
            )
        else:
            self.analysisclass.processnewparams(calcFOMDialogclass=self)
            nfiles = len(
                self.analysisclass.getapplicablefilenames(
                    self.expfiledict,
                    self.usek,
                    self.techk,
                    self.typek,
                    runklist=self.selectrunklist,
                    anadict=self.anadict,
                    calcFOMDialogclass=self,
                )
            )
            selind = int(self.AnalysisNamesComboBox.currentIndex())
            self.AnalysisNamesComboBox.setItemText(
                selind, self.analysisclass.analysis_name + ("(%d)" % nfiles)
            )
        self.getactiveanalysisclass()  # this is only to update the description if necessary

    def analyzedata(self):
        errbool = calcfom_analyzedata_calcfomdialogclass(self)
        if errbool:
            print errbool
            return errbool
        self.updateuserfomd(clear=True)
        self.fomplotchoiceComboBox.clear()
        for count, s in enumerate(self.fomnames):
            self.fomplotchoiceComboBox.insertItem(count, s)
        self.fomplotchoiceComboBox.setCurrentIndex(0)
        self.stdcsvplotchoiceComboBox.clear()
        if (
            "plot_parameters" in self.csvheaderdict.keys()
            and "plot__1" in self.csvheaderdict["plot_parameters"].keys()
        ):
            keys = sorted(
                [
                    k
                    for k in self.csvheaderdict["plot_parameters"].keys()
                    if k.startswith("plot__")
                ]
            )
            for count, s in enumerate(keys):
                self.stdcsvplotchoiceComboBox.insertItem(count, s)
            if len(keys) == 0:
                count = -1
                newk = "new plot__1"
            else:
                newk = "new plot__%d" % (int(keys[-1].partition("__")[2]) + 1)
            self.stdcsvplotchoiceComboBox.insertItem(count + 1, newk)
        self.stdcsvplotchoiceComboBox.setCurrentIndex(0)
        self.updateana()
        self.plot_preparestandardplot(plotbool=False)
        if self.autoplotCheckBox.isChecked():
            self.plot_generatedata(plotbool=True)
        return False

    def attachfilestoana(self, anak=None, pathlist=None):
        if anak is None:
            ans = userinputcaller(
                self,
                inputs=[
                    ("ana key", str, gethighestanak(self.anadict, getnextone=False))
                ],
                title="Enter ana__# to attach files",
                cancelallowed=True,
            )
            if ans is None or not ans[0].strip() in self.anadict.keys():
                return
            anak = ans[0].strip()
            anad = self.anadict[anak]
        if pathlist is None:
            pathlist = mygetopenfiles(self, markstr="select files to add as misc_files")
            if pathlist is None or len(pathlist) == 0:
                return
        fns = [os.path.split(p)[1] for p in pathlist]
        newfns = [("" if fn.startswith(anak) else (anak + "__")) + fn for fn in fns]
        if not "files_multi_run" in anad.keys():
            anad["files_multi_run"] = {}
        if not "misc_files" in anad["files_multi_run"].keys():
            anad["files_multi_run"]["misc_files"] = {}
        for p, newfn in zip(pathlist, newfns):
            vs = 1
            newp = os.path.join(self.tempanafolder, newfn)
            while os.path.exists(newp):
                vs += 1
                a, b = os.path.splitext(newfn)
                newp = os.path.join(self.tempanafolder, "%s_v%d%s" % (a, vs, b))
            shutil.copy(p, newp)
            anad["files_multi_run"]["misc_files"][
                os.path.split(newp)[1]
            ] = "user_misc_file;"
        self.updateana()

    def updateana(self):
        for k, (le, dfltstr) in self.paramsdict_le_dflt.items():
            if (
                k == "access" and "access" in self.expfiledict.keys()
            ):  # only allow access specification from UI if not already provded by exp
                continue
            s = str(le.text()).strip()
            if len(s) == 0:
                s = dfltstr
            self.anadict[
                k
            ] = s  # this makes description just the last ana__ description
        # plateids=sorted(list(set(['%d' %rund['parameters']['plate_id'] for rund in [v for k, v in self.expfiledict.iteritems() if k.startswith('run__')]]))) #this old way of getting plate_ids will include plates for which analysis was not done
        ananames = sorted(
            list(
                set(
                    [
                        anad["name"]
                        for anad in [
                            v
                            for k, v in self.anadict.iteritems()
                            if k.startswith("ana__")
                        ]
                    ]
                )
            )
        )
        plateidsstrlist_list = [
            anad["plate_ids"]
            for anad in [
                v for k, v in self.anadict.iteritems() if k.startswith("ana__")
            ]
            if "plate_ids" in anad.keys()
        ]
        plateidsstrlist = sorted(
            list(
                set(
                    [
                        idstr
                        for liststr in plateidsstrlist_list
                        for idstr in liststr.split(",")
                    ]
                )
            )
        )
        plateidsstr = ",".join(plateidsstrlist)
        # self.anadict['plate_ids']=plateidsstr
        self.anadict["description"] = "%s on plate_id %s" % (
            ", ".join(ananames),
            plateidsstr,
        )
        self.AnaTreeWidgetFcns.filltree(self.anadict)
        self.fillanalysistypes(self.TechTypeButtonGroup.checkedButton())

    def viewresult(self, anasavefolder=None, show=True):
        if anasavefolder is None:
            anasavefolder = self.tempanafolder
        d = copy.deepcopy(self.anadict)
        convertfilekeystofiled(d)
        # importfomintoanadict(d)
        if show:
            self.hide()
        self.parent.visexpana(anafiledict=d, anafolder=anasavefolder, show=show)

    def saveview(self):
        anasavefolder = self.saveana(dontclearyet=True)
        self.viewresult(
            anasavefolder=anasavefolder
        )  # just hide+show so shouldn't get hung here
        self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)

    def clearsingleanalysis(self, anak=None):
        keys = sort_dict_keys_by_counter(self.anadict, keystartswith="ana__")
        if anak is None:
            if len(keys) == 0:
                return
            i = userselectcaller(self, options=keys, title="select ana__ to delete")
            if i is None:
                return
            if len(keys) == 1:
                self.clearanalysis_pushbutton()
                return
        else:
            i = keys.index(anak)
        anad = self.anadict[keys[i]]
        fnlist = [
            fn
            for d in [
                v
                for k, v in anad.iteritems()
                if k.startswith("files_") and isinstance(v, dict)
            ]
            for d2 in d.itervalues()
            for fn in d2.keys()
        ]
        removefiles(self.tempanafolder, fnlist)
        if i < (len(keys) - 1):
            for ki, knext in zip(keys[i:-1], keys[i + 1 :]):
                self.anadict[ki] = self.anadict[knext]
        del self.anadict[keys[-1]]
        self.activeana = None
        self.updateana()

    def clearanalysis_pushbutton(self):
        if self.exppath == "null":
            self.clearanalysis()
        else:  # analysis will be cleared while importing exp
            self.importexp(expfiledict=self.expfiledict, exppath=self.exppath)

    def clearanalysis(self, anadict=None):
        self.analysisclass = None
        self.activeana = None
        self.anadict = {}
        self.AnaTreeWidget.clear()
        self.aux_exp_dlist = []
        self.aux_ana_dlist = []
        self.paramsdict_le_dflt["description"][1] = "null"
        if not anadict is None:
            for k, v in anadict.iteritems():
                self.anadict[k] = v
            if "description" in anadict.keys():
                self.paramsdict_le_dflt["description"][1] = anadict["description"]
            if self.modifyanainplace:  # can only modify in place if anadict provided
                self.anadict["ana_version"] = "3"
                if not self.anafolder is None:
                    self.tempanafolder = self.anafolder
                if "name" in self.anadict.keys():
                    self.AnaNameLineEdit.setText(self.anadict["name"])
                    self.paramsdict_le_dflt["name"][1] = self.anadict["name"]
                return
        self.anadict["ana_version"] = "3"
        if os.path.isdir(self.tempanafolder):
            for fn in os.listdir(self.tempanafolder):
                os.remove(os.path.join(self.tempanafolder, fn))
        else:
            self.tempanafolder = getanadefaultfolder(
                erroruifcn=lambda s: mygetdir(
                    parent=self,
                    markstr="select ANA default folder - to meet compliance this should be format %Y%m%d.%H%M%S.incomplete",
                )
            )
            # this is meant to result in rund['name']=%Y%m%d.%H%M%S but doesn't guarantee it
            timestr = (os.path.split(self.tempanafolder)[1]).rstrip(".incomplete")
            self.AnaNameLineEdit.setText(timestr)
            self.paramsdict_le_dflt["name"][1] = timestr

    def importanalysisparams(self):
        return

    def saveana(self, dontclearyet=False, anatype=None, rundone=None):
        self.anafilestr = self.AnaTreeWidgetFcns.createtxt()
        if self.modifyanainplace:
            savep = os.path.join(self.anafolder, self.anadict["name"] + ".ana")
            saveanafiles(savep, anafilestr=self.anafilestr, anadict=self.anadict)
            return self.anafolder
        if not "ana_version" in self.anafilestr:
            if self.guimode:
                idialog = messageDialog(self, "Aborting SAVE because no data in ANA")
                idialog.exec_()
            else:
                print "Aborting SAVE because no data in ANA"
            return
        if anatype is None:
            savefolder = None
            dfltanatype = self.anadict["analysis_type"]
            idialog = SaveOptionsDialog(self, dfltanatype)
            idialog.exec_()
            if not idialog.choice or len(idialog.choice) == 0:
                return
            anatype = idialog.choice
            if anatype == "browse":
                savefolder = mygetdir(
                    parent=self,
                    xpath="%s" % os.getcwd(),
                    markstr="Select folder for saving ANA",
                )
                if savefolder is None or len(savefolder) == 0:
                    return
                rundone = ""  # rundone not used if user browses for folder
            elif (
                anatype == dfltanatype
            ):  # ***saving in a place like eche or uvis then need to check if other things are there too
                needcopy_dlist = find_paths_in_ana_need_copy_to_anatype(
                    self.anadict, anatype
                )
                if len(needcopy_dlist) > 0:
                    if None in needcopy_dlist:
                        if self.guimode:
                            idialog = messageDialog(
                                self, "Aborting Save: Aux exp/ana in temp or not on K"
                            )
                            idialog.exec_()
                        else:
                            print "Aborting Save: Aux exp/ana in temp or not on K"
                        return
                    idialog = messageDialog(
                        self,
                        "Need to copy EXP and/or ANA to %s to continue\nOK to attempt copy, Cancel to abort save."
                        % anatype,
                    )
                    if not idialog.exec_():
                        return
                    for d_needcopy in needcopy_dlist:
                        errormsg = copyfolder_1level(
                            d_needcopy["srcabs"], d_needcopy["destabs"]
                        )
                        if errormsg:
                            if self.guimode:
                                idialog = messageDialog(
                                    self, "Aborting Save on exp/ana copy: " % errormsg
                                )
                                idialog.exec_()
                            else:
                                print "Aborting Save on exp/ana copy: " % errormsg
                            return
                        get_dict_item_keylist(
                            self.anadict, d_needcopy["anadkeylist"][:-1]
                        )[d_needcopy["anadkeylist"][-1]] = d_needcopy["destrel"]
                    self.anafilestr = self.AnaTreeWidgetFcns.createtxt()
        else:
            savefolder = None
        if len(self.anafilestr) == 0 or not "ana_version" in self.anafilestr:
            return
        if rundone is None:
            idialog = messageDialog(self, "save as .done ?")
            if idialog.exec_():
                rundone = ".done"
            else:
                rundone = ".run"
        anasavefolder = saveana_tempfolder(
            self.anafilestr,
            self.tempanafolder,
            analysis_type=anatype,
            anadict=self.anadict,
            savefolder=savefolder,
            rundone=rundone,
            erroruifcn=lambda s: mygetdir(
                parent=self,
                xpath="%s" % os.getcwd(),
                markstr="Error: %s, select folder for saving ANA",
            ),
        )
        if not dontclearyet:
            self.importexp(
                expfiledict=self.expfiledict, exppath=self.exppath
            )  # clear analysis happens here but exp_path wont' be lost
        # self.clearanalysis()
        return anasavefolder

    def editvisparams(self):
        if self.activeana is None:
            print "active ana__ has been lost so nothing done."
            return
        k = str(self.stdcsvplotchoiceComboBox.currentText())
        if not k in self.csvheaderdict["plot_parameters"].keys():
            k = k.partition("new ")[2]
            self.csvheaderdict["plot_parameters"][k] = {}
        d = self.csvheaderdict["plot_parameters"][k]
        d["fom_name"] = str(self.fomplotchoiceComboBox.currentText())
        for k, le in [
            ("colormap", self.colormapLineEdit),
            ("colormap_over_color", self.aboverangecolLineEdit),
            ("colormap_under_color", self.belowrangecolLineEdit),
        ]:
            if len(str(le.text()).strip()) == 0:
                continue
            v = str(le.text()).strip()
            if "_color" in k and v in colors.ColorConverter.colors.keys():
                v = str(colors.ColorConverter.colors[v])
            elif (
                "_color" in k and not "(" in v
            ):  # kinda require the color values to be (r,g,b)
                continue
            d[k] = v.replace(" ", "")
        s = str(self.vminmaxLineEdit.text())
        if "," in s:
            a, temp, b = s.partition(",")
            if len(a.strip()) > 0:
                d["colormap_min_value"] = a.strip()
            if len(b.strip()) > 0:
                d["colormap_max_value"] = b.strip()
        totnumheadlines = writecsv_smpfomd(
            self.primarycsvpath, "", headerdict=self.csvheaderdict, replaceheader=True
        )
        fnf = os.path.split(self.primarycsvpath)[1]
        files_techd = self.activeana["files_multi_run"]
        files_fomd = files_techd["fom_files"]
        s = files_fomd[fnf]
        l = s.split(";")
        l[2] = "%d" % (totnumheadlines)
        files_fomd[fnf] = ";".join(l)
        self.updateana()

    def plot_preparestandardplot(self, plotbool=True):
        k = str(self.stdcsvplotchoiceComboBox.currentText())
        if not "plot_parameters" in self.csvheaderdict.keys():
            return
        d = self.csvheaderdict["plot_parameters"][k]
        if not "fom_name" in d.keys() or not d["fom_name"] in self.fomnames:
            return
        self.fomplotchoiceComboBox.setCurrentIndex(self.fomnames.index(d["fom_name"]))
        for k, le in [
            ("colormap", self.colormapLineEdit),
            ("colormap_over_color", self.aboverangecolLineEdit),
            ("colormap_under_color", self.belowrangecolLineEdit),
        ]:
            if not k in d.keys():
                continue
            le.setText(d[k])
        if "colormap_min_value" in d.keys() and "colormap_max_value" in d.keys():
            self.vminmaxLineEdit.setText(
                "%s,%s" % (d["colormap_min_value"], d["colormap_max_value"])
            )
        if plotbool:
            self.plot_generatedata(plotbool=True)

    def plot_generatedata(self, plotbool=True):
        self.plotd = {}
        if len(self.fomdlist) == 0:
            return
        fi = self.fomplotchoiceComboBox.currentIndex()
        fom = numpy.array([d[self.fomnames[fi]] for d in self.fomdlist])
        runkarr = numpy.array(["run__%d" % (d["runint"]) for d in self.fomdlist])
        if "expkeys" in self.filedlist[0].keys():  # generally standard analysis class
            # runkarr=numpy.array([d['expkeys'][0] for d in self.filedlist])
            daqtimebool = self.usedaqtimeCheckBox.isChecked()
        else:  # generally Process FOM
            daqtimebool = False
        # inds are inds from  self.fomdlist, not all of which are used because some are NaN
        fomdlistinds = numpy.where(numpy.logical_not(numpy.isnan(fom)))[0]
        if len(fomdlistinds) == 0:
            print "ABORTING PLOTTING BECAUSE ALL FOMs ARE NaN"
            return
        # here the fom and runkarr and sample arrays are setup
        fom = fom[fomdlistinds]
        runkarr = runkarr[fomdlistinds]
        sample = numpy.array([self.fomdlist[i]["sample_no"] for i in fomdlistinds])
        # and now this is a dictionary that given a runk looks ups the inds from the above arrays, i.e. these inds are inds of the selction from fomdlist, NOT from fomdlist
        inds_runk = dict(
            [(runk, numpy.where(runkarr == runk)[0]) for runk in list(set(runkarr))]
        )
        t = []
        #        else:
        #            hx=numpy.arange(len(fom))
        # remapinds=[i for runk in sorted(inds_runk.keys()) for i in inds_runk[runk]]
        if daqtimebool:
            t = numpy.zeros(len(fom), dtype="float64")
            for runk in sorted(inds_runk.keys()):
                fns = [
                    self.filedlist[fomdlistinds[i]]["expkeys"][-1]
                    for i in inds_runk[runk]
                ]  # reduce(dict.get, ['x','q','w'], d)
                t[inds_runk[runk]] = applyfcn_txtfnlist_run(
                    gettimefromheader, self.expfiledict[runk]["run_path"], fns
                )
            t = numpy.array(t)
            t -= t.min()
        #        else:
        #            hx=numpy.array(sample)
        compplottype = str(self.CompPlotTypeComboBox.currentText())
        nanxy = [numpy.nan] * 2
        nancomp = [numpy.nan] * 4
        xy = numpy.ones((len(fom), 2), dtype="float64") * numpy.nan
        comps = numpy.ones((len(fom), 4), dtype="float64") * numpy.nan
        for runk in sorted(inds_runk.keys()):
            if (
                not "platemapdlist" in self.expfiledict[runk].keys()
                or len(self.expfiledict[runk]["platemapdlist"]) == 0
            ):
                #                if not compplottype=='none':
                #                    comps+=[nancomp]*len(inds_runk[runk])
                #                xy+=[nanxy]*len(inds_runk[runk])
                continue
            pmsmps = [d["Sample"] for d in self.expfiledict[runk]["platemapdlist"]]
            xy[inds_runk[runk]] = numpy.float64(
                [
                    [
                        self.expfiledict[runk]["platemapdlist"][pmsmps.index(smp)][k]
                        for k in ["x", "y"]
                    ]
                    if smp in pmsmps
                    else nanxy
                    for smp in sample[inds_runk[runk]]
                ]
            )
            if compplottype == "none":
                continue
            comps[inds_runk[runk]] = numpy.float64(
                [
                    [
                        self.expfiledict[runk]["platemapdlist"][pmsmps.index(smp)][k]
                        for k in ["A", "B", "C", "D"]
                    ]
                    if smp in pmsmps
                    else nancomp
                    for smp in sample[inds_runk[runk]]
                ]
            )
        #        xy=numpy.float64(xy)
        #        comps=numpy.float64(comps)
        self.plotd["comps"] = numpy.array([c / c.sum() for c in comps])
        self.plotd["xy"] = xy
        self.plotd["fom"] = fom
        self.plotd["inds_runk"] = inds_runk
        self.plotd["t"] = t
        self.plotd["sample_no"] = sample
        self.plotd["fomname"] = self.fomnames[fi]
        if plotbool:
            self.plot()

    def plotwithcaution(self):
        try:
            self.plot()
        except:
            print "ERROR UPDATING PLOTS. Porbably data not setup, try selecting a standard plot"

    def plot(self):
        if len(self.plotd) == 0:
            return
        self.plotw_comp.axes.cla()
        self.plotw_quat3d.axes.cla()
        self.plotw_plate.axes.cla()
        self.plotw_h.axes.cla()
        self.cbax_quat.cla()
        self.cbax_plate.cla()
        if len(self.plotd["fom"]) == 0:
            return
        x, y = self.plotd["xy"].T
        comps = self.plotd["comps"]
        fom = self.plotd["fom"]
        # h plot
        daqtimebool = self.usedaqtimeCheckBox.isChecked()
        if daqtimebool:
            hxarr = self.plotd["t"]
            xl = "time (s)"
        else:
            hxarr = self.plotd["sample_no"]
            xl = "sample_no"
        for runk in sorted(self.plotd["inds_runk"].keys()):
            hx = hxarr[self.plotd["inds_runk"][runk]]
            hy = fom[self.plotd["inds_runk"][runk]]
            sinds = numpy.argsort(hx)
            self.plotw_h.axes.plot(hx[sinds], hy[sinds], ".-", label=runk)
        leg = self.plotw_h.axes.legend(loc=0)
        leg.draggable()
        self.plotw_h.axes.set_xlabel(xl)
        self.plotw_h.axes.set_ylabel(self.plotd["fomname"])
        autotickformat(self.plotw_h.axes, x=daqtimebool, y=1)
        self.plotw_h.fig.canvas.draw()
        # plate plot
        cmapstr = str(self.colormapLineEdit.text())
        try:
            cmap = eval("cm." + cmapstr)
        except:
            cmap = cm.jet
        clip = True
        skipoutofrange = [False, False]
        self.vmin = fom.min()
        self.vmax = fom.max()
        vstr = str(self.vminmaxLineEdit.text()).strip()
        if "," in vstr:
            a, b, c = vstr.partition(",")
            try:
                a = myeval(a.strip())
                c = myeval(c.strip())
                self.vmin = a
                self.vmax = c
                for count, (fcn, le) in enumerate(
                    zip(
                        [cmap.set_under, cmap.set_over],
                        [self.belowrangecolLineEdit, self.aboverangecolLineEdit],
                    )
                ):
                    vstr = str(le.text()).strip()
                    vstr = vstr.replace('"', "").replace("'", "")
                    if "none" in vstr or "None" in vstr:
                        skipoutofrange[count] = True
                        continue
                    if len(vstr) == 0:
                        continue
                    c = col_string(vstr)
                    try:
                        fcn(c)
                        clip = False
                    except:
                        print "color entry not understood:", vstr
            except:
                pass
        norm = colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
        if skipoutofrange[0]:
            inds = numpy.where(fom >= self.vmin)
            fom = fom[inds]
            comps = comps[inds]
            x = x[inds]
            y = y[inds]
        if skipoutofrange[1]:
            inds = numpy.where(fom <= self.vmax)
            fom = fom[inds]
            comps = comps[inds]
            x = x[inds]
            y = y[inds]
        if numpy.any(fom > self.vmax):
            if numpy.any(fom < self.vmin):
                extend = "both"
            else:
                extend = "max"
        elif numpy.any(fom < self.vmin):
            extend = "min"
        else:
            extend = "neither"
        pointsizestr = str(self.compplotsizeLineEdit.text())
        m = self.plotw_plate.axes.scatter(
            x, y, c=fom, s=20, marker="s", edgecolor="none", cmap=cmap, norm=norm
        )
        if x.max() - x.min() < 2.0 or y.max() - y.min() < 2.0:
            self.plotw_plate.axes.set_xlim(x.min() - 1, x.max() + 1)
            self.plotw_plate.axes.set_ylim(y.min() - 1, y.max() + 1)
        else:
            self.plotw_plate.axes.set_aspect(1.0)
        sm = cm.ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array(fom)
        cols = numpy.float32(map(sm.to_rgba, fom))[:, :3]  # ignore alpha
        cb = self.plotw_plate.fig.colorbar(
            sm,
            cax=self.cbax_plate,
            extend=extend,
            format=autocolorbarformat((self.vmin, self.vmax)),
        )
        cb.set_label(self.plotd["fomname"])
        self.plotw_plate.fig.canvas.draw()
        # comp plot
        compsinds = [
            i
            for i, (compv, colv) in enumerate(zip(comps, cols))
            if not (numpy.any(numpy.isnan(compv)) or numpy.any(numpy.isnan(colv)))
        ]
        if len(compsinds) == 0:
            return
        self.quatcompclass.loadplotdata(comps[compsinds], cols[compsinds])
        plotw3dbool = self.quatcompclass.plot()
        if not plotw3dbool is None:
            if plotw3dbool:
                self.plotw_comp.hide()
                self.plotw_quat3d.show()
                self.plotw_quat3d.axes.set_axis_off()
                cb = self.plotw_quat3d.fig.colorbar(
                    sm,
                    cax=self.cbax_quat,
                    extend=extend,
                    format=autocolorbarformat((self.vmin, self.vmax)),
                )
                self.plotw_quat3d.fig.canvas.draw()
            else:
                self.plotw_quat3d.hide()
                self.plotw_comp.show()
                cb = self.plotw_comp.fig.colorbar(
                    sm,
                    cax=self.quatcompclass.cbax,
                    extend=extend,
                    format=autocolorbarformat((self.vmin, self.vmax)),
                )
                self.plotw_comp.fig.canvas.draw()
            cb.set_label(self.plotd["fomname"])

    #        comps=numpy.array([c[:4]/c[:4].sum() for c in comps])
    #        i=self.ternskipComboBox.currentIndex()
    #        inds=[j for j in range(4) if j!=i][:3]
    #        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
    #        reordercomps=comps[:, inds+[i]]
    #        self.ellabels=self.techniquedictlist[0]['elements']
    #        reorderlabels=[self.ellabels[j] for j in inds+[i]]
    #        quat=QuaternaryPlot(self.plotw_quat3d.axes, ellabels=self.ellabels, offset=0)
    #        quat.label()
    #        quat.scatter(comps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
    #        cb=self.plotw_quat3d.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
    #        fomlabel=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText()), self.filterfomstr))
    #        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel)])
    #
    #        pointsizestr=str(self.compplotsizeLineEdit.text())
    #        tern=TernaryPlot(self.plotw_comp.axes, ellabels=reorderlabels[:3], offset=0)
    #        tern.label()
    #        tern.scatter(terncomps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
    #        cb=self.plotw_comp.fig.colorbar(tern.mappable, cax=self.cbax_comp, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
    #
    #
    #
    #        #self.plotw_quat3d.axes.mouse_init()
    #        self.plotw_quat3d.axes.set_axis_off()
    #        self.plotw_comp.fig.canvas.draw()
    #        self.plotw_quat3d.fig.canvas.draw()
    # self.selectind=-1
    # self.plotselect()
    def plateclickprocess(self, coords_button):
        if len(self.techniquedictlist) == 0:
            return

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
    def plotwsetup(self):
        self.plotw_comp = plotwidget(self)
        self.plotw_quat3d = plotwidget(self, projection3d=True)
        self.plotw_h = plotwidget(self)
        self.plotw_plate = plotwidget(self)
        for b, w in [
            (self.textBrowser_plate, self.plotw_plate),
            (self.textBrowser_h, self.plotw_h),
            (self.textBrowser_comp, self.plotw_comp),
            (self.textBrowser_comp, self.plotw_quat3d),
        ]:
            w.setGeometry(b.geometry())
            b.hide()
        self.plotw_quat3d.hide()
        self.plotw_plate.axes.set_aspect(1)
        axrect = [0.88, 0.1, 0.04, 0.8]
        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0] - 0.01)
        self.cbax_plate = self.plotw_plate.fig.add_axes(axrect)
        self.plotw_quat3d.fig.subplots_adjust(left=0, right=axrect[0] - 0.01)
        self.cbax_quat = self.plotw_quat3d.fig.add_axes(axrect)
        self.plotw_h.fig.subplots_adjust(left=0.22, bottom=0.17)
        self.quatcompclass = quatcompplotoptions(
            self.plotw_comp,
            self.CompPlotTypeComboBox,
            plotw3d=self.plotw_quat3d,
            plotwcbaxrect=axrect,
        )

    def batch_processallana(self, additionalfcn_runeachiteration=None):
        if int(self.FOMProcessNamesComboBox.currentIndex()) == 0:
            print "quitting batch process because use analysis function was selected instead of a FOM process"
            return
        selprocesslabel = str(self.FOMProcessNamesComboBox.currentText()).partition(
            "("
        )[0]
        presentanakeys = sort_dict_keys_by_counter(self.anadict, keystartswith="ana__")
        for anak in presentanakeys:
            self.analysisclass.params["select_ana"] = anak
            if not additionalfcn_runeachiteration is None:
                additionalfcn_runeachiteration(self)
            self.processeditedparams()  # self.getactiveanalysisclass() run in here
            self.analyzedata()
            matchbool = False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool = (
                    str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
                ) == selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print "skipping %s, probably because no appropriate fom_files found" % anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
        self.FOMProcessNamesComboBox.setCurrentIndex(0)

    def batch_analyzethenprocess(self):
        if int(self.FOMProcessNamesComboBox.currentIndex()) == 0:
            print "quitting batch process because use analysis function was selected instead of a FOM process"
            return
        selprocesslabel = str(self.FOMProcessNamesComboBox.currentText()).partition(
            "("
        )[0]
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        self.getactiveanalysisclass()
        anak = gethighestanak(self.anadict, getnextone=True)
        self.analyzedata()
        if anak != gethighestanak(self.anadict, getnextone=False):
            print "quitting batch process because analysis function did not successfully run"
            return
        matchbool = False
        for i in range(1, int(self.FOMProcessNamesComboBox.count())):
            matchbool = (
                str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
            ) == selprocesslabel
            if matchbool:
                break
        if not matchbool:
            print "skipping %s, probably because no appropriate fom_files found" % anak
        self.FOMProcessNamesComboBox.setCurrentIndex(i)
        self.getactiveanalysisclass()
        self.analysisclass.params["select_ana"] = anak
        self.processeditedparams()  # self.getactiveanalysisclass() run in here
        self.analyzedata()
        self.FOMProcessNamesComboBox.setCurrentIndex(0)

    def batch_analyzethenprocess_allsubspace(self):
        if int(self.FOMProcessNamesComboBox.currentIndex()) == 0:
            print "quitting batch process because use analysis function was selected instead of a FOM process"
            return
        selprocesslabel_original = str(
            self.FOMProcessNamesComboBox.currentText()
        ).partition("(")[0]
        selprocess_root = selprocesslabel_original.partition("__")[0]
        if len(selprocess_root) == 0:
            print 'quitting batch process because FOM process function not iterable (must be "<root>__<indexstr>")'
            return
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        self.getactiveanalysisclass()
        anak = gethighestanak(self.anadict, getnextone=True)
        self.analyzedata()
        if anak != gethighestanak(self.anadict, getnextone=False):
            print "quitting batch process because analysis function did not successfully run"
            return
        selprocesslabel_list = [
            str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
            for i in range(1, int(self.FOMProcessNamesComboBox.count()))
            if (str(self.FOMProcessNamesComboBox.itemText(i)).partition("__")[0])
            == selprocess_root
        ]
        for selprocesslabel in selprocesslabel_list:
            matchbool = False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool = (
                    str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
                ) == selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print "skipping %s, probably because no appropriate fom_files found" % anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
            self.analysisclass.params["select_ana"] = anak
            self.processeditedparams()  # self.getactiveanalysisclass() run in here
            anak_processed = gethighestanak(self.anadict, getnextone=True)
            self.analyzedata()
            if anak_processed != gethighestanak(self.anadict, getnextone=False):
                print "quitting batch process because processing function did not successfully run"
                return
        self.FOMProcessNamesComboBox.setCurrentIndex(0)
        # user would prompt running of editanalysisparams_paramsd at this point but skip this since only updates the label

    def batch_process_allsubspace(self):
        self.getactiveanalysisclass()
        if not "select_ana" in self.analysisclass.params.keys():
            print "quitting batch process because the presently selected FOM process function does not provide the select_ana"
            return
        anak = self.analysisclass.params["select_ana"]
        # anak=gethighestanak(self.anadict, getnextone=False)
        selprocesslabel_original = str(
            self.FOMProcessNamesComboBox.currentText()
        ).partition("(")[0]
        selprocess_root = selprocesslabel_original.partition("__")[0]
        if len(selprocess_root) == 0:
            print 'quitting batch process because FOM process function not iterable (must be "<root>__<indexstr>")'
            return
        selprocesslabel_list = [
            str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
            for i in range(1, int(self.FOMProcessNamesComboBox.count()))
            if (str(self.FOMProcessNamesComboBox.itemText(i)).partition("__")[0])
            == selprocess_root
        ]
        for selprocesslabel in selprocesslabel_list:
            matchbool = False
            for i in range(1, int(self.FOMProcessNamesComboBox.count())):
                matchbool = (
                    str(self.FOMProcessNamesComboBox.itemText(i)).partition("(")[0]
                ) == selprocesslabel
                if matchbool:
                    break
            if not matchbool:
                print "skipping %s, probably because no appropriate fom_files found" % anak
            self.FOMProcessNamesComboBox.setCurrentIndex(i)
            self.getactiveanalysisclass()
            self.analysisclass.params["select_ana"] = anak
            self.processeditedparams()  # self.getactiveanalysisclass() run in here
            anak_processed = gethighestanak(self.anadict, getnextone=True)
            self.analyzedata()
            if anak_processed != gethighestanak(self.anadict, getnextone=False):
                print "quitting batch process because processing function did not successfully run"
                return
        self.FOMProcessNamesComboBox.setCurrentIndex(0)

    def batch_analyze_fcn_same_techclass(self):
        # uses the presently-selected analysis name, file type and 1st 2 characters of techniuqe to run the analysis on all  tech,type that match
        anname = self.analysisclass.analysis_name
        buttonstrings = [
            ",".join([techv, typev])
            for techv, typev in self.techk_typek
            if techv[:2] == self.techk[:2] and typev == self.typek
        ]
        for buttonstr in buttonstrings:
            qlist = self.TechTypeButtonGroup.buttons()
            typetechfound = False
            for button in qlist:
                if str(button.text()).strip() == buttonstr:
                    button.setChecked(True)
                    typetechfound = True
                    break
            if not typetechfound:
                print "Skipped %s because could find it in the options list" % buttonstr
                continue
            self.fillanalysistypes(self.TechTypeButtonGroup.checkedButton())
            cb = self.AnalysisNamesComboBox
            selind = [
                i
                for i in range(int(cb.count()))
                if str(cb.itemText(i)).startswith(anname)
            ]
            if len(selind) == 0:
                print "Skipped %s because the analysis option was not available" % buttonstr
                continue
            cb.setCurrentIndex(selind[0])
            self.getactiveanalysisclass()
            self.analyzedata()

    def batch_merge_atfrac_from_aux(self, anainds="ALL"):
        if len(self.aux_ana_dlist) == 0:
            self.openauxexpana(tryexp=False)
        if len(self.aux_ana_dlist) != 1:
            print "can only run batch AtFrac merge with single aux ana"
            return
        # auto select the analysis fcn to see the all ana batck
        matchbool = False
        for i in range(1, int(self.FOMProcessNamesComboBox.count())):
            matchbool = "FOM_Merge_Aux_Ana" in str(
                self.FOMProcessNamesComboBox.itemText(i)
            )
            if matchbool:
                self.FOMProcessNamesComboBox.setCurrentIndex(i)
                break
        if not matchbool:
            print "skipping %s, probably because no appropriate fom_files found" % anak
            return
        auxanak = sort_dict_keys_by_counter(
            self.aux_ana_dlist[0], keystartswith="ana__"
        )[-1]
        auxanaintstr = auxanak.partition("__")[2]

        def additionalfcn_runeachiteration(selfclasslocal):
            selfclasslocal.analysisclass.params["select_aux_keys"] = ".AtFrac"
            selfclasslocal.analysisclass.params[
                "aux_ana_ints"
            ] = auxanaintstr  # only use the latest aux ana__ assuming that is the "best" or most complete composition analysis
            selfclasslocal.analysisclass.params["aux_ana_name"] = os.path.split(
                self.aux_ana_dlist[0]["auxexpanapath_relative"]
            )[1]

        self.batch_processallana(
            additionalfcn_runeachiteration=additionalfcn_runeachiteration
        )

    def batch_set_params_for_photo_mAcm2_scaling(self, measurement_area=None):
        if not self.select_procana_fcn("Process_B_vs_A_ByRun"):
            print "quitting because Process_B_vs_A_ByRun not available"
            return
        runklist = [
            k
            for k in sort_dict_keys_by_counter(self.expfiledict, keystartswith="run__")
            if self.expfiledict[k]["run_use"] == "data"
            and "eche" in self.expfiledict[k]["run_path"]
        ]
        runintliststr = ",".join([k[5:] for k in runklist])
        if measurement_area is None:
            areas = [
                self.expfiledict[runk]["parameters"]["measurement_area"]
                for runk in runklist
            ]
            if 0.0 in areas or False in [areas[0] == v for v in areas]:
                measurement_area = userinputcaller(
                    self,
                    inputs=[("measurement area in mm2: ", float, "0.")],
                    title="Inconsistent or 0 area in exp",
                    cancelallowed=False,
                )[0]
            else:
                measurement_area = areas[0]
        macm2divisor = 1.0e-5 * measurement_area
        self.analysisclass.params["select_ana"] = gethighestanak(self.anadict)
        self.analysisclass.params["runints_A"] = runintliststr
        self.analysisclass.params["runints_B"] = runintliststr
        self.analysisclass.params["keys_to_keep"] = "Voc.V,Vpmax.V,Fill_factor"
        self.analysisclass.params["method"] = "B_over_A"
        self.analysisclass.params["fom_keys_A"] = "%.3e" % macm2divisor
        self.analysisclass.params["fom_keys_B"] = "I.A,Pmax,Ipmax,Isc"
        self.analysisclass.params["relative_key_append"] = "_mAcm2"
        self.processeditedparams()
        if "Pmax" in self.analysisclass.params["fom_keys_B"]:
            self.analysisclass.params["relative_key_append"] = ",".join(
                [
                    "_mWcm2" if "Pmax" in k else "_mAcm2"
                    for k in self.analysisclass.params["fom_keys_B"].split(",")
                ]
            )
            self.processeditedparams()

    def select_procana_fcn(self, analabel):
        cb = self.FOMProcessNamesComboBox
        # print cb.count()
        for i in range(1, int(cb.count())):
            # print (str(cb.itemText(i)).partition('(')[0].partition('__')[2])
            if (str(cb.itemText(i)).partition("(")[0].partition("__")[2]) == analabel:
                cb.setCurrentIndex(i)
                self.getactiveanalysisclass()
                return True
        return False

    def create_default_fom_csv_from_runfiles(self, anak):
        smplist = []
        fomdl = []
        if (
            "plate_ids" in self.anadict[anak].keys()
            and not "," in self.anadict[anak]["plate_ids"]
        ):
            pid = int(self.anadict[anak]["plate_ids"])
        else:
            print "ABORTING fom csv creation because only supported for single plate_id ana__"
            return
        for rk, rd in self.anadict[anak].items():
            if not rk.startswith("files_run__"):
                continue
            runint = int(rk[11:])
            for tk, td in rd.items():
                for fn, fd in td.items():
                    if isinstance(fd, str):
                        fd = createfileattrdict(fd)
                    if (
                        "sample_no" in fd.keys()
                        and fd["sample_no"] > 0
                        and not fd["sample_no"] in smplist
                    ):
                        smplist += [fd["sample_no"]]
                        fomdl += [
                            {
                                "sample_no": fd["sample_no"],
                                "runint": runint,
                                "plate_id": pid,
                            }
                        ]  # if sample_no appears in multiple runs (which shouldn't happen) the csv will contain first run found
        file_desc, s = createcsvfilstr_bare(
            fomdl,
            [],
            intfomkeys=["sample_no", "runint", "plate_id"],
            return_file_desc=True,
        )
        fn = "%s__samplelog.csv" % anak
        p = os.path.join(self.tempanafolder, fn)
        with open(p, mode="w") as f:
            f.write(s)
        if not "files_multi_run" in self.anadict[anak].keys():
            self.anadict[anak]["files_multi_run"] = {}
        if not "fom_files" in self.anadict[anak]["files_multi_run"].keys():
            self.anadict[anak]["files_multi_run"]["fom_files"] = {}
        self.anadict[anak]["files_multi_run"]["fom_files"][fn] = file_desc
        self.updateana()  # the .ana file is not written - only udpating the anadict within this calcui


class treeclass_anadict:
    def __init__(self, tree):
        self.treeWidget = tree
        self.treeWidget.clear()

    def getlistofchecktoplevelitems(self):
        return [
            str(self.treeWidget.topLevelItem(count).text(0)).strip().strip(":")
            for count in range(int(self.treeWidget.topLevelItemCount()))
            if bool(self.treeWidget.topLevelItem(count).checkState(0))
        ]

    def maketoplevelchecked(self):
        for count in range(int(self.treeWidget.topLevelItemCount())):
            item = self.treeWidget.topLevelItem(count)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)

    def filltree(self, d, startkey="ana_version", laststartswith="ana__"):
        self.treeWidget.clear()
        # assume startkey is not for dict and laststatswith is dict
        if len(startkey) > 0:
            mainitem = QTreeWidgetItem([": ".join([startkey, d[startkey]])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
            self.treeWidget.setCurrentItem(mainitem)
        for k in sorted(
            [k for k, v in d.iteritems() if k != startkey and not isinstance(v, dict)]
        ):
            mainitem = QTreeWidgetItem([": ".join([k, str(d[k])])], 0)
            self.treeWidget.addTopLevelItem(mainitem)
        for k in sorted(
            [
                k
                for k, v in d.iteritems()
                if not k.startswith(laststartswith) and isinstance(v, dict)
            ]
        ):
            mainitem = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)
        anakl = sort_dict_keys_by_counter(d, keystartswith=laststartswith)
        for k in anakl:
            mainitem = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], mainitem)
            self.treeWidget.addTopLevelItem(mainitem)
            mainitem.setExpanded(False)

    def nestedfill(self, d, parentitem, laststartswith="files_"):
        nondictkeys = sorted([k for k, v in d.iteritems() if not isinstance(v, dict)])
        for k in nondictkeys:
            item = QTreeWidgetItem([": ".join([k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys1 = sorted(
            [
                k
                for k, v in d.iteritems()
                if not k.startswith(laststartswith) and isinstance(v, dict)
            ]
        )
        for k in dictkeys1:
            item = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], item)
            parentitem.addChild(item)
        dictkeys2 = sorted([k for k in d.keys() if k.startswith(laststartswith)])
        for k in dictkeys2:
            item = QTreeWidgetItem([k + ":"], 0)
            self.nestedfill(d[k], item)
            parentitem.addChild(item)

    def createtxt(self, indent="    "):
        self.indent = indent
        return "\n".join(
            [
                self.createtxt_item(self.treeWidget.topLevelItem(count))
                for count in range(int(self.treeWidget.topLevelItemCount()))
            ]
        )

    def createtxt_item(self, item, indentlevel=0):
        str(item.text(0))
        itemstr = self.indent * indentlevel + str(item.text(0)).strip()
        if item.childCount() == 0:
            return itemstr
        childstr = "\n".join(
            [
                self.createtxt_item(item.child(i), indentlevel=indentlevel + 1)
                for i in range(item.childCount())
            ]
        )
        return "\n".join([itemstr, childstr])

    def partitionlineitem(self, item):
        s = str(item.text(0)).strip()
        a, b, c = s.partition(":")
        return (a.strip(), c.strip())

    def createdict(self):
        return dict(
            [
                self.createdict_item(self.treeWidget.topLevelItem(count))
                for count in range(int(self.treeWidget.topLevelItemCount()))
            ]
        )

    def createdict_item(self, item):
        tup = self.partitionlineitem(item)
        if item.childCount() == 0:
            return tup
        d = dict(
            [self.createdict_item(item.child(i)) for i in range(item.childCount())]
        )
        return (tup[0], d)


if __name__ == "__main__":

    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):
            super(MainMenu, self).__init__(None)
            self.calcui = calcfomDialog(self, title="Calculate FOM from EXP", **kwargs)
            #            self.calcui.importana(p=r'L:\processes\analysis\temp\20190402.124053.run\20190402.124053.ana')
            #            for tech in ['CV1', 'CV2','CV3']:
            #                for i in range(1, int(self.calcui.FOMProcessNamesComboBox.count())):
            #                    if (str(self.calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__ECMS_Fit_MS':
            #                        self.calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            #                        self.calcui.getactiveanalysisclass()
            #                        self.calcui.analysisclass.params['eche_techniques']=tech
            #                        self.calcui.processeditedparams()
            #                        break
            #
            #                self.calcui.analyzedata()
            #            self.calcui.importana(p=r'L:\processes\analysis\temp\20190402.124053.run\20190402.124053.ana')
            #            for lossfcn in ['L2_5x_positive','L2', 'L1', 'LogCosh_1E9', 'L2_5x_first_half', 'L2_inv_prop_to_time']:
            #                for i in range(1, int(self.calcui.FOMProcessNamesComboBox.count())):
            #                    if (str(self.calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__ECMS_Fit_MS':
            #                        self.calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            #                        self.calcui.getactiveanalysisclass()
            #                        self.calcui.analysisclass.params['eche_techniques']='CV3'
            #                        self.calcui.analysisclass.params['loss_fcn']=lossfcn
            #                        self.calcui.processeditedparams()
            #                        break
            #
            #                self.calcui.analyzedata()
            #            self.calcui.importexp(exppath=r'//htejcap.caltech.edu/share/data/hte_jcap_app_proto/experiment/eche/20170802.120418.copied-20170802221206976PDT.zip\20170802.120418.exp')
            #            self.calcui.analyzedata()
            #            self.calcui.importauxexpana(r'L:\processes\analysis\ssrl\20190624.140000.run\20190624.140000.ana', exp=False)
            #
            #            for i in range(1, int(self.calcui.FOMProcessNamesComboBox.count())):
            #                if (str(self.calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__FOM_Interp_Merge_Ana':
            #                    self.calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            #                    self.calcui.getactiveanalysisclass()
            #                    c=self.calcui.analysisclass
            #                    break
            #            c.params.update({'select_aux_keys':'ALL', 'aux_ana_ints':'9',  'interp_is_phasemap':1})
            #            self.calcui.processeditedparams()
            #            self.calcui.getactiveanalysisclass()
            #            #self.calcui.exec_()
            #            self.calcui.analyzedata()
            # self.calcui.importexp(exppath=r'K:\processes\experiment\temp\20160218.162704.run\20160218.162704.exp')
            # TRdata:
            # self.calcui.importexp(exppath=r'K:\processes\experiment\temp\20160222.104337.run\20160222.104337.exp')
            # self.calcui.analyzedata()
            #            self.calcui.importana(p=r'L:\processes\analysis\eche\20170524.103449.copied-20170524221236494PDT\20170524.103449.ana')
            #            self.calcui.importauxexpana(r'L:\processes\analysis\xrfs\20170907.125058.copied-20170907221545763PDT\20170907.125058.ana', exp=False)
            #            c=FOMProcessClasses[4]
            #            c.params['select_aux_keys']='V.K.AtFrac,Cu.K.AtFrac,Bi.L.AtFrac'
            #            c.params['select_aux_ints']='2'
            #            c.params['interp_is_comp']=1
            #            c.processnewparams(calcFOMDialogclass=self.calcui, recalc_filedlist=True)
            #            for i in range(1, int(self.calcui.FOMProcessNamesComboBox.count())):
            #                if (str(self.calcui.FOMProcessNamesComboBox.itemText(i)).partition('(')[0])=='Analysis__SpectralPhoto':
            #                    self.calcui.FOMProcessNamesComboBox.setCurrentIndex(i)
            #                    self.calcui.getactiveanalysisclass()
            #                    self.calcui.processeditedparams()
            #                    break
            #            anak=gethighestanak(self.calcui.anadict, getnextone=True)
            #            cb=self.calcui.AnalysisNamesComboBox
            #            selind=[i for i in range(int(cb.count())) if str(cb.itemText(i)).startswith('Analysis__SpectralPhoto')]
            #            cb.setCurrentIndex(selind[0])
            #            self.calcui.getactiveanalysisclass()
            # c.perform(self.calcui.tempanafolder, expdatfolder=self.calcui.expfolder, anak=anak, zipclass=self.calcui.expzipclass, expfiledict=self.calcui.expfiledict, anauserfomd=self.calcui.userfomd)
            if execute:
                self.calcui.exec_()

    mainapp = QApplication(sys.argv)
    form = MainMenu(
        None, execute=False, modifyanainplace=False
    )  # modifyanainplace is a dangerous thing to turn on so no user-available way of doing it
    form.show()
    form.setFocus()
    form.calcui.show()
    mainapp.exec_()
