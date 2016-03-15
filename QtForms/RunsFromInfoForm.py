# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\RunsFromInfoForm.ui'
#
# Created: Mon Feb 22 14:31:00 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RunsFromInfoDialog(object):
    def setupUi(self, RunsFromInfoDialog):
        RunsFromInfoDialog.setObjectName(_fromUtf8("RunsFromInfoDialog"))
        RunsFromInfoDialog.resize(579, 408)
        self.buttonBox = QtGui.QDialogButtonBox(RunsFromInfoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 360, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.FilesTreeWidget = QtGui.QTreeWidget(RunsFromInfoDialog)
        self.FilesTreeWidget.setGeometry(QtCore.QRect(10, 10, 561, 341))
        self.FilesTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FilesTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.FilesTreeWidget.setHeaderHidden(True)
        self.FilesTreeWidget.setExpandsOnDoubleClick(False)
        self.FilesTreeWidget.setObjectName(_fromUtf8("FilesTreeWidget"))
        self.FilesTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.FilesTreeWidget.header().setVisible(False)
        self.FilesTreeWidget.header().setCascadingSectionResizes(False)
        self.FilesTreeWidget.header().setStretchLastSection(True)
        self.plateidLineEdit = QtGui.QLineEdit(RunsFromInfoDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(5, 380, 101, 20))
        self.plateidLineEdit.setObjectName(_fromUtf8("plateidLineEdit"))
        self.label = QtGui.QLabel(RunsFromInfoDialog)
        self.label.setGeometry(QtCore.QRect(10, 360, 91, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.typeLineEdit = QtGui.QLineEdit(RunsFromInfoDialog)
        self.typeLineEdit.setGeometry(QtCore.QRect(115, 380, 101, 20))
        self.typeLineEdit.setObjectName(_fromUtf8("typeLineEdit"))
        self.label_2 = QtGui.QLabel(RunsFromInfoDialog)
        self.label_2.setGeometry(QtCore.QRect(120, 360, 91, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.qualityLineEdit = QtGui.QLineEdit(RunsFromInfoDialog)
        self.qualityLineEdit.setGeometry(QtCore.QRect(225, 380, 101, 20))
        self.qualityLineEdit.setObjectName(_fromUtf8("qualityLineEdit"))
        self.label_3 = QtGui.QLabel(RunsFromInfoDialog)
        self.label_3.setGeometry(QtCore.QRect(230, 360, 91, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ReadInfoPushButton = QtGui.QPushButton(RunsFromInfoDialog)
        self.ReadInfoPushButton.setGeometry(QtCore.QRect(340, 370, 51, 31))
        self.ReadInfoPushButton.setObjectName(_fromUtf8("ReadInfoPushButton"))

        self.retranslateUi(RunsFromInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RunsFromInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RunsFromInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RunsFromInfoDialog)

    def retranslateUi(self, RunsFromInfoDialog):
        RunsFromInfoDialog.setWindowTitle(QtGui.QApplication.translate("RunsFromInfoDialog", "Plate Info File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "plate_id:", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLineEdit.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "eche", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "run type contains:", None, QtGui.QApplication.UnicodeUTF8))
        self.qualityLineEdit.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "Usable", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "\"Quality\" contains:", None, QtGui.QApplication.UnicodeUTF8))
        self.ReadInfoPushButton.setToolTip(QtGui.QApplication.translate("RunsFromInfoDialog", "Import multiple folders and/or .zip, each representing a RUN with a .rcp file", None, QtGui.QApplication.UnicodeUTF8))
        self.ReadInfoPushButton.setText(QtGui.QApplication.translate("RunsFromInfoDialog", "get .info", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RunsFromInfoDialog = QtGui.QDialog()
    ui = Ui_RunsFromInfoDialog()
    ui.setupUi(RunsFromInfoDialog)
    RunsFromInfoDialog.show()
    sys.exit(app.exec_())

