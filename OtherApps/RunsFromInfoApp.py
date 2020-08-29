import time, itertools, string
from PyQt5.QtWidgets import *
import os, os.path, shutil
import sys
import numpy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import operator
import matplotlib
from DBPaths import PLATEFOLDERS
import pickle

# from fcns_math import *
from fcns_io import *
from fcns_ui import *

# from VisualizeAuxFcns import *
from RunsFromInfoForm import Ui_RunsFromInfoDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions


class runsfrominfoDialog(QDialog, Ui_RunsFromInfoDialog):
    def __init__(self, parent, runtype="eche"):
        super(runsfrominfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.typeLineEdit.setText(runtype)
        button_fcn = [
            (self.ReadInfoPushButton, self.importinfo),
        ]
        self.plateidLineEdit.setFocus()

        def setfocus():
            self.ReadInfoPushButton.setFocus()

        self.plateidLineEdit.editingFinished.connect(setfocus)
        # (self.UndoExpPushButton, self.undoexpfile), \
        for button, fcn in button_fcn:
            button.pressed.connect(fcn)
        self.FilesTreeWidget.itemDoubleClicked[QTreeWidgetItem, int].connect(
            self.editname
        )
        self.buttonBox.accepted.connect(self.ExitRoutine)

    def importinfo(self):
        plateidstr = str(self.plateidLineEdit.text())
        fn = plateidstr + ".info"
        p = tryprependpath(
            PLATEFOLDERS, os.path.join(plateidstr, fn), testfile=True, testdir=False
        )
        if len(p) == 0:
            idialog = messageDialog(self, "no .info file found")
            idialog.exec_()
            return
        with open(p, mode="r") as f:
            lines = f.readlines()
        self.infofiled = filedict_lines(lines)
        self.FilesTreeWidget.clear()
        toplevelitem = QTreeWidgetItem([fn], 0)
        self.runditems = []
        self.nestedfill(self.infofiled, toplevelitem)
        self.FilesTreeWidget.addTopLevelItem(toplevelitem)
        toplevelitem.setExpanded(True)

    def nestedfill(
        self,
        d,
        parentitem,
        firststartswith="run",
        prependstr="",
        skipkeys=[],
        runparent=False,
    ):
        nondictkeys = sorted(
            [
                k
                for k, v in d.iteritems()
                if not isinstance(v, dict) and not k in skipkeys
            ]
        )
        for k in nondictkeys:
            item = QTreeWidgetItem([": ".join([prependstr + k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys2 = sorted(
            [k for k in d.keys() if k.startswith(firststartswith) and not k in skipkeys]
        )
        for k in dictkeys2:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            if runparent:  # a k==run__X dict gets here
                rd = d[k]
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if (
                    "type" in rd.keys() and str(self.typeLineEdit.text()) in rd["type"]
                ) and (
                    (not "quality" in rd.keys())
                    or str(self.qualityLineEdit.text()) in rd["quality"]
                ):
                    item.setCheckState(0, Qt.Checked)
                else:
                    item.setCheckState(0, Qt.Unchecked)
                self.runditems += [item]
            self.nestedfill(
                d[k], item, firststartswith="runs__", runparent=True
            )  # first time through the "runs" key is found and then runparent True passed to the next level where run__ are found
            parentitem.addChild(item)
            item.setExpanded(True)  # not working?
        dictkeys1 = sorted(
            [
                k
                for k, v in d.iteritems()
                if not k.startswith(firststartswith)
                and isinstance(v, dict)
                and not k in skipkeys
            ]
        )
        for k in dictkeys1:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            self.nestedfill(d[k], item, runparent=False)
            parentitem.addChild(item)

    def editname(self, item, column):
        if item is None:
            item = widget.currentItem()
        v = str(item.text(column))
        ans = userinputcaller(
            self,
            inputs=[("filename", str, v)],
            title="Enter new filename",
            cancelallowed=True,
        )

    #        if ans is None or ans[0].strip()==v:
    #            return
    #        ans=ans[0].strip()
    #        item.setText(column,''.join([ans, keepstr]))
    def ExitRoutine(self):
        rundlist = [
            self.infofiled["runs"][str(item.text(0)).strip().strip(":")]
            for item in self.runditems
            if bool(item.checkState(0))
        ]
        self.runpaths = [d["path"] for d in rundlist]
        self.rcpdictadditions = [
            [("run_quality: %s" % d["quality"], [])] if "quality" in d else []
            for d in rundlist
        ]  # this is the fileline, nested filelines list format of rcpd


if __name__ == "__main__":

    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):  # , TreeWidg):
            super(MainMenu, self).__init__(None)
            # self.setupUi(self)
            self.infoui = runsfrominfoDialog(self, **kwargs)
            if execute:
                self.infoui.exec_()

    mainapp = QApplication(sys.argv)
    form = MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
