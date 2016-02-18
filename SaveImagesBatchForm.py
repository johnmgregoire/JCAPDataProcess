# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\SaveImagesBatchForm.ui'
#
# Created: Thu Feb 18 09:44:07 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveImagesBatchDialog(object):
    def setupUi(self, SaveImagesBatchDialog):
        SaveImagesBatchDialog.setObjectName(_fromUtf8("SaveImagesBatchDialog"))
        SaveImagesBatchDialog.resize(579, 455)
        self.buttonBox = QtGui.QDialogButtonBox(SaveImagesBatchDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.FilesTreeWidget = QtGui.QTreeWidget(SaveImagesBatchDialog)
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
        self.overwriteCheckBox = QtGui.QCheckBox(SaveImagesBatchDialog)
        self.overwriteCheckBox.setGeometry(QtCore.QRect(10, 370, 101, 31))
        self.overwriteCheckBox.setChecked(True)
        self.overwriteCheckBox.setObjectName(_fromUtf8("overwriteCheckBox"))
        self.doneCheckBox = QtGui.QCheckBox(SaveImagesBatchDialog)
        self.doneCheckBox.setGeometry(QtCore.QRect(120, 370, 81, 31))
        self.doneCheckBox.setChecked(False)
        self.doneCheckBox.setObjectName(_fromUtf8("doneCheckBox"))
        self.epsCheckBox = QtGui.QCheckBox(SaveImagesBatchDialog)
        self.epsCheckBox.setGeometry(QtCore.QRect(215, 370, 71, 31))
        self.epsCheckBox.setChecked(True)
        self.epsCheckBox.setObjectName(_fromUtf8("epsCheckBox"))
        self.prependfilenameLineEdit = QtGui.QLineEdit(SaveImagesBatchDialog)
        self.prependfilenameLineEdit.setGeometry(QtCore.QRect(285, 381, 113, 20))
        self.prependfilenameLineEdit.setObjectName(_fromUtf8("prependfilenameLineEdit"))
        self.label = QtGui.QLabel(SaveImagesBatchDialog)
        self.label.setGeometry(QtCore.QRect(290, 350, 101, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.plotstyleoverrideCheckBox = QtGui.QCheckBox(SaveImagesBatchDialog)
        self.plotstyleoverrideCheckBox.setGeometry(QtCore.QRect(410, 360, 161, 31))
        self.plotstyleoverrideCheckBox.setChecked(False)
        self.plotstyleoverrideCheckBox.setObjectName(_fromUtf8("plotstyleoverrideCheckBox"))
        self.filenamesearchLineEdit = QtGui.QLineEdit(SaveImagesBatchDialog)
        self.filenamesearchLineEdit.setGeometry(QtCore.QRect(140, 420, 261, 20))
        self.filenamesearchLineEdit.setObjectName(_fromUtf8("filenamesearchLineEdit"))
        self.label_2 = QtGui.QLabel(SaveImagesBatchDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 410, 131, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(SaveImagesBatchDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SaveImagesBatchDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SaveImagesBatchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveImagesBatchDialog)

    def retranslateUi(self, SaveImagesBatchDialog):
        SaveImagesBatchDialog.setWindowTitle(QtGui.QApplication.translate("SaveImagesBatchDialog", "ChooseImagesToSave", None, QtGui.QApplication.UnicodeUTF8))
        self.overwriteCheckBox.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "overwrite files\n"
"with same name", None, QtGui.QApplication.UnicodeUTF8))
        self.doneCheckBox.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "convert .run \n"
"to .done", None, QtGui.QApplication.UnicodeUTF8))
        self.epsCheckBox.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "also save\n"
".eps", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "Prepend to filename, in\n"
"addition to auto-prepend", None, QtGui.QApplication.UnicodeUTF8))
        self.plotstyleoverrideCheckBox.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "Override std plot plot options\n"
"(colormap, fom range, etc.)", None, QtGui.QApplication.UnicodeUTF8))
        self.filenamesearchLineEdit.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "plate_id__, code__", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SaveImagesBatchDialog", "filename search strings for \n"
"selecting images to save", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveImagesBatchDialog = QtGui.QDialog()
    ui = Ui_SaveImagesBatchDialog()
    ui.setupUi(SaveImagesBatchDialog)
    SaveImagesBatchDialog.show()
    sys.exit(app.exec_())

