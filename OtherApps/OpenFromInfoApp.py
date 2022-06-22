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
from OpenFromInfoForm import Ui_OpenFromInfoDialog
from fcns_compplots import *
from quatcomp_plot_options import quatcompplotoptions


class openfrominfoDialog(QDialog, Ui_OpenFromInfoDialog):
    def __init__(self, parent, runtype="", exp=True, ana=True, run=False):
        super(openfrominfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.typeLineEdit.setText(runtype)
        button_fcn = [
            (self.ReadInfoPushButton, self.importinfo),
        ]
        if exp:
            button_fcn += [
                (self.SearchExpPushButton, self.searchexp),
            ]
        else:
            self.SearchExpPushButton.setVisible(False)
        self.exp = exp
        if ana:
            button_fcn += [
                (self.SearchAnaPushButton, self.searchana),
            ]
        else:
            self.SearchAnaPushButton.setVisible(False)
        self.ana = ana
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
        self.filltree(fn)

    def filltree(self, fn):
        self.FilesTreeWidget.clear()
        toplevelitem = QTreeWidgetItem([fn], 0)
        self.expanaditems = []
        self.nestedfill(self.infofiled, toplevelitem)
        self.FilesTreeWidget.addTopLevelItem(toplevelitem)
        toplevelitem.setExpanded(True)

    def nestedfill(self, d, parentitem, prependstr="", skipkeys=[], expanaparent=False):
        nondictkeys = sorted(
            [
                k
                for k, v in d.items()
                if not isinstance(v, dict) and not k in skipkeys
            ]
        )
        for k in nondictkeys:
            item = QTreeWidgetItem([": ".join([prependstr + k, str(d[k])])], 0)
            parentitem.addChild(item)
        dictkeys2 = sorted(
            [
                k
                for k in list(d.keys())
                if (self.exp and k.startswith("experiments"))
                or (self.ana and k.startswith("analyses"))
            ]
        )
        for k in dictkeys2:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            if expanaparent:  # a k==run__X dict gets here
                rd = d[k]
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                # if ('type' in rd.keys() and str(self.typeLineEdit.text()) in rd['type']) and ((not 'quality' in rd.keys()) or str(self.qualityLineEdit.text()) in rd['quality']):
                if ("searchbool" in list(rd.keys())) or (
                    (
                        "path" in list(rd.keys())
                        and str(self.searchLineEdit.text()) in rd["path"]
                    )
                    and (
                        "type" in list(rd.keys())
                        and str(self.typeLineEdit.text()) in rd["type"]
                    )
                ):
                    item.setCheckState(0, Qt.Checked)
                else:
                    item.setCheckState(0, Qt.Unchecked)
                self.expanaditems += [item]
            self.nestedfill(
                d[k], item, expanaparent=True
            )  # first time through the "runs" key is found and then runparent True passed to the next level where run__ are found
            parentitem.addChild(item)
            item.setExpanded(True)  # not working?
        dictkeys1 = sorted(
            [
                k
                for k, v in d.items()
                if (not k in dictkeys2) and isinstance(v, dict)
            ]
        )
        for k in dictkeys1:
            item = QTreeWidgetItem([prependstr + k + ":"], 0)
            self.nestedfill(d[k], item, expanaparent=False)
            parentitem.addChild(item)

    def searchexp(self):
        self.searchfcn(EXPFOLDERS_J + EXPFOLDERS_L, ana=False)

    def searchana(self):
        self.searchfcn(ANAFOLDERS_J + ANAFOLDERS_L, ana=True)

    def searchfcn(self, searchfolds, ana=True):
        searchstr = str(self.searchLineEdit.text())
        if len(searchstr) == 0:
            return
        foldn = str(self.typeLineEdit.text())
        if len(foldn) == 0:
            testpaths = [
                os.path.join(rootn, fn)
                for rootn in searchfolds
                for fn in os.listdir(rootn)
            ]
        else:
            testpaths = [os.path.join(rootn, foldn) for rootn in searchfolds]
        searchfolds = [s for s in testpaths if os.path.isdir(s)]
        for folder in searchfolds:
            fns = [fn for fn in os.listdir(folder) if searchstr in fn]
            if len(fns) > 0:
                break
        if len(fns) == 0:
            print("No EXP/ANA found")
            return
        self.infofiled = {}
        if ana:
            k = "analyses"
        else:
            k = "experiments"
        self.infofiled[k] = {}
        d = self.infofiled[k]
        for count, fn in enumerate(fns):
            k2 = "%s__%d" % (k, count + 1)
            d[k2] = {}
            d[k2]["path"] = os.path.join(folder, fn)
            d[k2]["searchbool"] = True
        self.filltree("search results")

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
        selectkeys = [
            str(item.text(0)).strip().strip(":")
            for item in self.expanaditems
            if bool(item.checkState(0))
        ]
        select_expanak_dlist = [
            (k.partition("__")[0], self.infofiled[k.partition("__")[0]][k])
            for k in selectkeys
        ]
        if len(select_expanak_dlist) == 0:
            self.selectexppaths = []
            self.selectanapaths = []
            self.selectpath = ""
            self.selecttype = None
            return
        # these could be folder or .zip
        self.selectexppaths = [
            d["path"] for expanak, d in select_expanak_dlist if expanak == "experiments"
        ]
        self.selectanapaths = [
            d["path"] for expanak, d in select_expanak_dlist if expanak == "analyses"
        ]
        self.findselectpath_anafile_orexpfile()

    def findselectpath_anafile_orexpfile(self):
        if len(self.selectanapaths) > 0:
            self.selectpath = self.selectanapaths[0]
            self.selecttype = "ana"
            if self.selectpath.endswith(".zip"):
                return
            ext = ".ana"
        elif len(self.selectexppaths) > 0:
            self.selectpath = self.selectexppaths[0]
            self.selecttype = "exp"
            if self.selectpath.endswith(".zip"):
                return
            ext = ".exp"
        l = [fn for fn in os.listdir(self.selectpath) if fn.endswith(ext)]
        if len(l) == 0:
            self.selectpath = ""
            return
        self.selectpath = os.path.join(self.selectpath, l[0])


if __name__ == "__main__":

    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):  # , TreeWidg):
            super(MainMenu, self).__init__(None)
            # self.setupUi(self)
            self.infoui = openfrominfoDialog(self, **kwargs)
            if execute:
                self.infoui.exec_()

    mainapp = QApplication(sys.argv)
    form = MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
