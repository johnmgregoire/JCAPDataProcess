# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\OpenFromInfoForm.ui'
#
# Created: Fri Mar 11 22:03:21 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OpenFromInfoDialog(object):
    def setupUi(self, OpenFromInfoDialog):
        OpenFromInfoDialog.setObjectName(_fromUtf8("OpenFromInfoDialog"))
        OpenFromInfoDialog.resize(579, 427)
        self.buttonBox = QtGui.QDialogButtonBox(OpenFromInfoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.FilesTreeWidget = QtGui.QTreeWidget(OpenFromInfoDialog)
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
        self.plateidLineEdit = QtGui.QLineEdit(OpenFromInfoDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(5, 380, 101, 20))
        self.plateidLineEdit.setObjectName(_fromUtf8("plateidLineEdit"))
        self.label = QtGui.QLabel(OpenFromInfoDialog)
        self.label.setGeometry(QtCore.QRect(10, 360, 91, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.typeLineEdit = QtGui.QLineEdit(OpenFromInfoDialog)
        self.typeLineEdit.setGeometry(QtCore.QRect(115, 380, 101, 20))
        self.typeLineEdit.setObjectName(_fromUtf8("typeLineEdit"))
        self.label_2 = QtGui.QLabel(OpenFromInfoDialog)
        self.label_2.setGeometry(QtCore.QRect(120, 360, 91, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.searchLineEdit = QtGui.QLineEdit(OpenFromInfoDialog)
        self.searchLineEdit.setGeometry(QtCore.QRect(225, 380, 101, 20))
        self.searchLineEdit.setText(_fromUtf8(""))
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.label_3 = QtGui.QLabel(OpenFromInfoDialog)
        self.label_3.setGeometry(QtCore.QRect(230, 360, 91, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ReadInfoPushButton = QtGui.QPushButton(OpenFromInfoDialog)
        self.ReadInfoPushButton.setGeometry(QtCore.QRect(330, 360, 71, 21))
        self.ReadInfoPushButton.setObjectName(_fromUtf8("ReadInfoPushButton"))
        self.SearchExpPushButton = QtGui.QPushButton(OpenFromInfoDialog)
        self.SearchExpPushButton.setGeometry(QtCore.QRect(400, 360, 61, 21))
        self.SearchExpPushButton.setObjectName(_fromUtf8("SearchExpPushButton"))
        self.SearchAnaPushButton = QtGui.QPushButton(OpenFromInfoDialog)
        self.SearchAnaPushButton.setGeometry(QtCore.QRect(460, 360, 71, 21))
        self.SearchAnaPushButton.setObjectName(_fromUtf8("SearchAnaPushButton"))

        self.retranslateUi(OpenFromInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OpenFromInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OpenFromInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenFromInfoDialog)

    def retranslateUi(self, OpenFromInfoDialog):
        OpenFromInfoDialog.setWindowTitle(QtGui.QApplication.translate("OpenFromInfoDialog", "Plate Info File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "plate_id:", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLineEdit.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "eche", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "run type contains:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "search string:", None, QtGui.QApplication.UnicodeUTF8))
        self.ReadInfoPushButton.setToolTip(QtGui.QApplication.translate("OpenFromInfoDialog", "Import multiple folders and/or .zip, each representing a RUN with a .rcp file", None, QtGui.QApplication.UnicodeUTF8))
        self.ReadInfoPushButton.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "get .info", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchExpPushButton.setToolTip(QtGui.QApplication.translate("OpenFromInfoDialog", "find any exp .zip or folders\n"
"that have the search string but\n"
" only exps in the first folderwith a hit", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchExpPushButton.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "search EXP", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchAnaPushButton.setToolTip(QtGui.QApplication.translate("OpenFromInfoDialog", "find any exp .zip or folders\n"
"that have the search string but\n"
" only exps in the first folderwith a hit", None, QtGui.QApplication.UnicodeUTF8))
        self.SearchAnaPushButton.setText(QtGui.QApplication.translate("OpenFromInfoDialog", "search ANA", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OpenFromInfoDialog = QtGui.QDialog()
    ui = Ui_OpenFromInfoDialog()
    ui.setupUi(OpenFromInfoDialog)
    OpenFromInfoDialog.show()
    sys.exit(app.exec_())

