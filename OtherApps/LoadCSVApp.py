import time, itertools, string
from PyQt5.QtWidgets import *
import os, os.path, shutil
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

try:
    from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QTAgg as NavigationToolbar,
    )
except ImportError:
    from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QT as NavigationToolbar,
    )
from matplotlib.figure import Figure

# import numpy.ma as ma
# import matplotlib.colors as colors
# import matplotlib.cm as cm
# import matplotlib.mlab as mlab
# import pylab
import pickle

# from fcns_math import *
from fcns_io import *
from fcns_ui import *

# from VisualizeAuxFcns import *
from LoadCSVForm import Ui_LoadCSVDialog


class loadcsvDialog(QDialog, Ui_LoadCSVDialog):
    def __init__(
        self,
        parent,
        ellabels=["A", "B", "C", "D"],
        platemappath=None,
        csvstartpath="",
        runk="run__1",
    ):
        super(loadcsvDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.ExitRoutine)
        self.csvpath = mygetopenfile(
            parent=self, xpath=csvstartpath, markstr="Select .csv file"
        )
        if len(self.csvpath) == 0:
            self.reject()
            return
        with open(self.csvpath, mode="r") as f:
            lines = f.readlines()
        for linecount, l in enumerate(lines):
            if linecount > 0 and (
                l[0].isdigit() or l[0] == "-"
            ):  # not first line and starts with number which may be negative
                break
        ans = userinputcaller(
            self,
            inputs=[("Num. header lines (incl headings)", int, repr( linecount))],
            title="Enter # header lines in .csv",
            cancelallowed=True,
        )
        if ans is None:
            self.reject()
            return
        self.fileattrd = {}
        self.fileattrd["file_type"] = "usercsv"
        self.fileattrd["num_header_lines"] = ans[0]
        button_fcn = [
            (self.platemapPushButton, self.openplatemap),
            (self.plateidPushButton, self.getinfousingplateid),
        ]  # (self.csvPushButton, self.opencsv), \
        # (self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            button.pressed.connect(fcn)
        self.sampleComboBox.activated["QString"].connect(self.setplatemapoption)
        self.comboboxdict = dict(
            [
                ("sample_no", self.sampleComboBox),
                ("x", self.xComboBox),
                ("y", self.yComboBox),
                ("A", self.aComboBox),
                ("B", self.bComboBox),
                ("C", self.cComboBox),
                ("D", self.dComboBox),
                ("code", self.codeComboBox),
            ]
        )
        self.ellabels = ellabels
        if self.ellabels != [
            "A",
            "B",
            "C",
            "D",
        ]:  # visualizer already has ellables so don't let user change them
            self.ellabelsLineEdit.setText(",".join(self.ellabels))
            self.ellabelsLineEdit.setReadOnly(True)
        else:
            self.ellabelsLineEdit.setText("A,B,C,D")
            self.ellabelsLineEdit.setReadOnly(False)
        self.rund = {}
        self.rund["parameters"] = {}
        self.rund["parameters"]["plate_id"] = 0
        self.opencsv()
        if self.csvd is None:
            self.error = True
            return
        self.runk = runk
        if not platemappath is None:
            self.platemapLineEdit.setText(platemappath)
            self.useplatemapCheckBox.setChecked(True)
        else:
            self.platemapLineEdit.setText("")
            self.useplatemapCheckBox.setChecked(False)
            for cb in list(self.comboboxdict.values()):
                cb.setCurrentIndex(0)
        self.findsamplecolumn()
        self.setplatemapoption()
        self.error = False

    def opencsv(self):
        try:
            self.csvd = readcsvdict(
                self.csvpath,
                self.fileattrd,
                returnheaderdict=False,
                zipclass=None,
                includestrvals=False,
            )
        except:
            print("csv load aborted due to issue with opening .csv")
            self.csvd = None
            return
        for k in [
            "runint",
            "anaint",
        ]:  # do not allow these keys because no guarantee they will match with the exp and anafiledict in visualizer
            if k in list(self.csvd.keys()):
                del self.csvd[k]
        if "plate_id" in list(self.csvd.keys()):
            self.plateidLineEdit.setText(repr( self.csvd["plate_id"][0]))
            # self.getinfousingplateid()#could auto do this but may nto want to sometimes so let user clikc the button
        for k, cb in list(self.comboboxdict.items()):
            if k == "sample_no":
                s = "Use row number"
            else:
                s = "Dummy value"
            cb.insertItem(0, s)
            for count, k in enumerate(self.csvd.keys()):
                cb.insertItem(
                    count + 1, k
                )  # fom choices are not associated with particular indeces of the l_ structures
            cb.setCurrentIndex(0)
        self.fileattrd["num_data_rows"] = len(self.csvd[k])
        self.fileattrd["keys"] = list(self.csvd.keys())

    def getinfousingplateid(self):
        plateidstr = str(self.plateidLineEdit.text())
        if len(plateidstr) == 0:
            return
        pmpath = getplatemappath_plateid(plateidstr)
        if len(pmpath) == 0:
            idialog = messageDialog(
                self, "Error loading plate from plate_id %s" % plateidstr
            )
            idialog.exec_()
            return
        self.rund["platemapdlist"] = readsingleplatemaptxt(pmpath)
        self.rund["parameters"]["plate_id"] = int(plateidstr)
        self.platemapLineEdit.setText(os.path.normpath(pmpath))
        self.useplatemapCheckBox.setEnabled(True)
        self.useplatemapCheckBox.setChecked(True)
        els = getelements_plateidstr(plateidstr)
        if not els is None:
            self.ellabels = els
            self.ellabelsLineEdit.setText(",".join(els))
            self.ellabelsLineEdit.setReadOnly(False)

    def findsamplecolumn(self):
        cbstrlist = [
            str(self.sampleComboBox.itemText(i))
            for i in range(self.sampleComboBox.count())
        ]
        for count, s in enumerate(cbstrlist):
            if "Sample" in s or "sample" in s:
                self.sampleComboBox.setCurrentIndex(count)

    def setplatemapoption(self, settrue=False):
        if (
            int(self.sampleComboBox.currentIndex()) == 0
            or len(str(self.platemapLineEdit.text())) == 0
        ):  # using indexes as fake sample_no so cannot use platemap, or platemap not available
            self.useplatemapCheckBox.setChecked(False)
            self.useplatemapCheckBox.setEnabled(False)
        else:
            self.useplatemapCheckBox.setEnabled(True)
            if settrue:
                self.useplatemapCheckBox.setChecked(True)

    def openplatemap(self, uselineeditpath=False, settrue=True):
        if uselineeditpath:
            pmpath = str(self.platemapLineEdit.text())
        else:
            pmpath = ""
        pmlines, pmpath = get_lines_path_file(
            p=pmpath,
            erroruifcn=lambda s: mygetopenfile(
                parent=self,
                xpath=PLATEMAPFOLDERS[0],
                markstr="Error: %s select platemap for csv file",
            ),
        )
        try:
            self.rund["platemapdlist"] = readsingleplatemaptxt("", lines=pmlines)
        except:
            pmpath = ""
        self.platemapLineEdit.setText(os.path.normpath(pmpath))
        self.setplatemapoption(settrue=settrue)
        return pmpath

    def defaultplatemaparray(self, k):
        csvrownum = numpy.arange(len(self.csvd[list(self.csvd.keys())[0]])) + 1
        if k == "sample_no":
            return csvrownum
        if k == "x" or k == "y":
            return csvrownum * 0.0
        if k == "code":
            return csvrownum * 0
        return (csvrownum * 1.0) * numpy.nan

    def createadhocplatemapdlist(self):
        arrd = {}
        for k, cb in list(self.comboboxdict.items()):
            # no platemap available so use dummy or column values for each item
            if int(cb.currentIndex()) == 0:
                arrd[k] = self.defaultplatemaparray(k)
            else:
                csvk = str(cb.currentText())
                arrd[k] = self.csvd[csvk]
        # transpose the arrays to a dlist
        return [
            dict([(k, arrd[k][i]) for k in list(arrd.keys())])
            for i in range(len(arrd["sample_no"]))
        ]

    def ExitRoutine(self):
        if self.rund["parameters"]["plate_id"] == 0:
            try:
                self.rund["parameters"]["plate_id"] = int(
                    str(self.plateidLineEdit.text())
                )
            except:
                pass
        adhocbool = False
        if (
            len(str(self.platemapLineEdit.text())) == 0
            or int(self.sampleComboBox.currentIndex()) == 0
        ):  # need to make dummy platemap if there is no platemap or using row number as sample_no
            self.rund["platemapdlist"] = self.createadhocplatemapdlist()
            adhocbool = True
            self.platemapLineEdit.setText("ad hoc")
        elif (
            not "platemapdlist" in list(self.rund.keys())
        ):  # the existing platemap sent from visualizer to be used,.......just load it again
            pmpath = self.openplatemap(
                uselineeditpath=True, settrue=False
            )  # get platemap but don't check the use platemap box as this is exitroutuine and the user's choices have already been made and cannot be edited
            if len(pmpath) == 0:  # problem laoding the "existing" platemap
                self.openplatemap(uselineeditpath=False, settrue=False)
        smpk = str(self.sampleComboBox.currentText())
        if (
            smpk != "sample_no"
        ):  # if using a csv sample column then make sure the key in csvd is 'sample_no'
            self.csvd["sample_no"] = self.csvd[smpk]
        self.rund["platemapsamples"] = [
            d["sample_no"] for d in self.rund["platemapdlist"]
        ]
        samplesinplatemap = [
            smp in self.rund["platemapsamples"] for smp in self.csvd["sample_no"]
        ]
        if False in samplesinplatemap:
            self.error = True
            idialog = messageDialog(
                self, "Error not all sample_no were found in the platemap"
            )
            idialog.exec_()
            return
        if adhocbool:
            print("ad-hoc platemap created fro loaded csv with %d samples" % len(
                self.rund["platemapdlist"]
            ))
        elif self.useplatemapCheckBox.isChecked():
            print("csv loaded with %d samples, which were located in the platemap" % len(
                samplesinplatemap
            ))
        else:  # if using platemap for the rest then this is "normal" like a .csv from an ana and we're done. otherwise, parse it down to only the used sample_no since there are cusotm modifications. if adhoc platemap then this is already done
            print("csv loaded and with custom platemap modifications for the following keys:")
            platemapinds = [
                self.rund["platemapsamples"].index(smp)
                for smp in self.csvd["sample_no"]
            ]
            newpmdlist = [self.rund["platemapdlist"][i] for i in platemapinds]
            self.rund["platemapdlist"] = copy.copy(newpmdlist)
            self.rund["platemapsamples"] = list(self.csvd["sample_no"])
            for k, cb in list(self.comboboxdict.items()):
                if (
                    k == "sample_no" or int(cb.currentIndex()) == 0
                ):  # ==0 means default value but to get here must have read the platemap and assume that these keys are there so dont' need to create default values, just use existing platemap ones
                    continue
                print(k)
                csvk = str(cb.currentText())
                arr = self.csvd[csvk]
                # goes through each platemapd and reaplces k with v from csvd column
                for d, v in zip(self.rund["platemapdlist"], arr):
                    d.update(dict([(k, v)]))
        runint = int(self.runk.lstrip("run__"))
        self.fomdlist = [
            dict(
                [("anaint", 0), ("runint", runint)]
                + [(k, self.csvd[k][i]) for k in list(self.csvd.keys())]
            )
            for i in range(len(self.csvd["sample_no"]))
        ]
        if (
            len(self.fomdlist) == 0
        ):  # not sure why this would happen but just in case to avoid later exceptions
            self.error = True
        self.fomnames = list(self.fomdlist[0].keys())
        self.runfilesdict = {}
        csvfn = os.path.split(self.csvpath)[1]
        for d in self.fomdlist:
            self.fileattrd["sample_no"] = d[
                "sample_no"
            ]  # placeholder samlpe_no for expfiled
            self.runfilesdict["%s-%d" % (csvfn, d["sample_no"])] = copy.copy(
                self.fileattrd
            )  # need to make a fake run file for every sample because visualizer only present tiopions for samples_no for which there is expfiledict data
