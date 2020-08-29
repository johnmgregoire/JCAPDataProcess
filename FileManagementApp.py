# cd C:\Python27\Lib\site-packages\PyQt4
# pyuic4 -x C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\QtDesign\CreateExpForm.ui -o C:\Users\Gregoire\Documents\PythonCode\JCAP\JCAPCreateExperimentAndFOM\CreateExpForm.py
import time, shutil
from PyQt5.QtWidgets import *
import os, os.path
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

try:
    from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QTAgg as NavigationToolbar,
    )
except ImportError:
    from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QT as NavigationToolbar,
    )
projectpath = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(os.path.join(projectpath, "QtForms"))
sys.path.append(os.path.join(projectpath, "AuxPrograms"))
sys.path.append(os.path.join(projectpath, "OtherApps"))
# from fcns_math import *
from fcns_io import *
from fcns_ui import *
from FileManagementForm import Ui_FileManDialog
from DBPaths import *


class filemanDialog(QDialog, Ui_FileManDialog):
    def __init__(self, parent=None, title="", folderpath=None):
        super(filemanDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        button_fcn = [
            (self.deletefoldersButton, self.deletefolders),
            (self.findfoldersButton, self.findfolders),
        ]
        # (self.UndoExpPushButton, self.undoexpfile), \
        #        (self.EditParamsPushButton, self.editrunparams), \
        # (self.EditExpParamsPushButton, self.editexpparams), \
        for button, fcn in button_fcn:
            button.pressed.connect(fcn)
        self.treeWidget = self.foldersTreeWidget
        self.toplevelitems = []
        self.anafolder = tryprependpath(ANAFOLDERS_L, "")
        self.expfolder = tryprependpath(EXPFOLDERS_L, "")
        if len(self.anafolder) == 0 and len(self.expfolder) == 0:
            print "cannot find exp or ana folder"
            return

    def deletefolders(self):
        for mainitem, fold in zip(self.toplevelitems, [self.expfolder, self.anafolder]):
            if mainitem is None or not bool(mainitem.checkState(0)):
                continue
            subitems = [
                mainitem.child(i)
                for i in range(mainitem.childCount())
                if bool(mainitem.child(i).checkState(0))
            ]
            delpaths = [
                os.path.join(
                    os.path.join(fold, str(subitem.text(0))),
                    str(subitem.child(i).text(0)),
                )
                for subitem in subitems
                for i in range(subitem.childCount())
                if bool(subitem.child(i).checkState(0))
            ]
            for p in delpaths:
                shutil.rmtree(p, ignore_errors=True)
                print "removed ", p
        if bool(mainitem.checkState(0)):
            idialog = messageDialog(
                self,
                "folders deleted: ANA temp folder possibly deleted \nso restart before performing analysis",
            )
            idialog.exec_()

    def findfolders(self):
        self.treeWidget.clear()
        self.toplevelitems = []
        self.endswith = str(self.endswithLineEdit.text())
        for i, (lab, fold) in enumerate(
            zip(["EXP", "ANA"], [self.expfolder, self.anafolder])
        ):
            if len(fold) == 0:  # didn't find exp or ana folder but found other one
                self.toplevelitems += [None]
                continue
            mainitem = QTreeWidgetItem([lab], 0)
            mainitem.setFlags(mainitem.flags() | Qt.ItemIsUserCheckable)
            mainitem.setCheckState(0, Qt.Checked)
            if i == 0:
                item0 = mainitem
            self.treeWidget.addTopLevelItem(mainitem)
            self.nestedfill(fold, mainitem, "top", endswith=None)
            mainitem.setExpanded(True)
            self.toplevelitems += [mainitem]
        self.treeWidget.setCurrentItem(item0)

    def nestedfill(self, fold, parentitem, level, endswith=".run"):
        subfolds = [
            fn for fn in os.listdir(fold) if os.path.isdir(os.path.join(fold, fn))
        ]
        if not endswith is None:
            subfolds = [fn for fn in subfolds if fn.endswith(endswith)]
        for fn in subfolds:
            item = QTreeWidgetItem([fn], 0)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if (
                level == "top" and fn != "temp"
            ):  # don't auto check the non-temp folders like eche, uvis, imag
                item.setCheckState(0, Qt.Unchecked)
            else:
                item.setCheckState(0, Qt.Checked)
            if level == "top":
                p = os.path.join(fold, fn)
                # print p
                addbool = self.nestedfill(p, item, "sub", endswith=self.endswith)
                addbool = addbool > 0
            else:
                addbool = True
            if addbool:
                parentitem.addChild(item)
        return len(subfolds)


if __name__ == "__main__":

    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):  # , TreeWidg):
            super(MainMenu, self).__init__(None)
            # self.setupUi(self)
            self.filemanui = filemanDialog(
                self, title="Delete obsolete .run folders", **kwargs
            )
            # self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            # self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.filemanui.exec_()

    os.chdir("//htejcap.caltech.edu/share/home/users/hte/demo_proto")
    mainapp = QApplication(sys.argv)
    form = MainMenu(None)
    form.show()
    form.setFocus()
    mainapp.exec_()
