# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\FileSearchForm.ui'
#
# Created: Sat Nov 14 00:41:08 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_filesearchDialog(object):
    def setupUi(self, filesearchDialog):
        filesearchDialog.setObjectName(_fromUtf8("filesearchDialog"))
        filesearchDialog.resize(560, 397)
        self.treeWidget = QtGui.QTreeWidget(filesearchDialog)
        self.treeWidget.setGeometry(QtCore.QRect(0, 80, 551, 311))
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setStretchLastSection(True)
        self.findfoldersButton = QtGui.QPushButton(filesearchDialog)
        self.findfoldersButton.setGeometry(QtCore.QRect(0, 10, 71, 23))
        self.findfoldersButton.setObjectName(_fromUtf8("findfoldersButton"))
        self.withinfileLineEdit = QtGui.QLineEdit(filesearchDialog)
        self.withinfileLineEdit.setGeometry(QtCore.QRect(440, 10, 113, 20))
        self.withinfileLineEdit.setText(_fromUtf8(""))
        self.withinfileLineEdit.setObjectName(_fromUtf8("withinfileLineEdit"))
        self.label = QtGui.QLabel(filesearchDialog)
        self.label.setGeometry(QtCore.QRect(370, 10, 71, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(filesearchDialog)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 71, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.foldernameLineEdit = QtGui.QLineEdit(filesearchDialog)
        self.foldernameLineEdit.setGeometry(QtCore.QRect(250, 10, 113, 20))
        self.foldernameLineEdit.setText(_fromUtf8(""))
        self.foldernameLineEdit.setObjectName(_fromUtf8("foldernameLineEdit"))
        self.exp_k_checkBox = QtGui.QCheckBox(filesearchDialog)
        self.exp_k_checkBox.setGeometry(QtCore.QRect(130, 20, 16, 17))
        self.exp_k_checkBox.setText(_fromUtf8(""))
        self.exp_k_checkBox.setChecked(True)
        self.exp_k_checkBox.setObjectName(_fromUtf8("exp_k_checkBox"))
        self.exp_j_checkBox = QtGui.QCheckBox(filesearchDialog)
        self.exp_j_checkBox.setGeometry(QtCore.QRect(150, 20, 16, 17))
        self.exp_j_checkBox.setText(_fromUtf8(""))
        self.exp_j_checkBox.setObjectName(_fromUtf8("exp_j_checkBox"))
        self.ana_k_checkBox = QtGui.QCheckBox(filesearchDialog)
        self.ana_k_checkBox.setGeometry(QtCore.QRect(130, 40, 16, 17))
        self.ana_k_checkBox.setText(_fromUtf8(""))
        self.ana_k_checkBox.setChecked(True)
        self.ana_k_checkBox.setObjectName(_fromUtf8("ana_k_checkBox"))
        self.ana_j_checkBox = QtGui.QCheckBox(filesearchDialog)
        self.ana_j_checkBox.setGeometry(QtCore.QRect(150, 40, 16, 17))
        self.ana_j_checkBox.setText(_fromUtf8(""))
        self.ana_j_checkBox.setObjectName(_fromUtf8("ana_j_checkBox"))
        self.label_3 = QtGui.QLabel(filesearchDialog)
        self.label_3.setGeometry(QtCore.QRect(100, 20, 21, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(filesearchDialog)
        self.label_4.setGeometry(QtCore.QRect(100, 40, 21, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(filesearchDialog)
        self.label_5.setGeometry(QtCore.QRect(130, 6, 20, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(filesearchDialog)
        self.label_6.setGeometry(QtCore.QRect(150, 9, 20, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))

        self.retranslateUi(filesearchDialog)
        QtCore.QMetaObject.connectSlotsByName(filesearchDialog)

    def retranslateUi(self, filesearchDialog):
        filesearchDialog.setWindowTitle(QtGui.QApplication.translate("filesearchDialog", "EXP+ANA file management", None, QtGui.QApplication.UnicodeUTF8))
        self.findfoldersButton.setText(QtGui.QApplication.translate("filesearchDialog", "find folders", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("filesearchDialog", "Search within\n"
"exp/ana file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("filesearchDialog", "Search within\n"
"folder name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("filesearchDialog", "exp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("filesearchDialog", "ana", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("filesearchDialog", " K", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("filesearchDialog", " J", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    filesearchDialog = QtGui.QDialog()
    ui = Ui_filesearchDialog()
    ui.setupUi(filesearchDialog)
    filesearchDialog.show()
    sys.exit(app.exec_())

