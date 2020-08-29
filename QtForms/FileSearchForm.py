# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\FileSearchForm.ui'
#
# Created: Sat Nov 14 00:41:08 2015
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_filesearchDialog(object):
    def setupUi(self, filesearchDialog):
        filesearchDialog.setObjectName("filesearchDialog")
        filesearchDialog.resize(560, 397)
        self.treeWidget = QtWidgets.QTreeWidget(filesearchDialog)
        self.treeWidget.setGeometry(QtCore.QRect(0, 80, 551, 311))
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setStretchLastSection(True)
        self.findfoldersButton = QtWidgets.QPushButton(filesearchDialog)
        self.findfoldersButton.setGeometry(QtCore.QRect(0, 10, 71, 23))
        self.findfoldersButton.setObjectName("findfoldersButton")
        self.withinfileLineEdit = QtWidgets.QLineEdit(filesearchDialog)
        self.withinfileLineEdit.setGeometry(QtCore.QRect(440, 10, 113, 20))
        self.withinfileLineEdit.setText("")
        self.withinfileLineEdit.setObjectName("withinfileLineEdit")
        self.label = QtWidgets.QLabel(filesearchDialog)
        self.label.setGeometry(QtCore.QRect(370, 10, 71, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(filesearchDialog)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 71, 31))
        self.label_2.setObjectName("label_2")
        self.foldernameLineEdit = QtWidgets.QLineEdit(filesearchDialog)
        self.foldernameLineEdit.setGeometry(QtCore.QRect(250, 10, 113, 20))
        self.foldernameLineEdit.setText("")
        self.foldernameLineEdit.setObjectName("foldernameLineEdit")
        self.exp_k_checkBox = QtWidgets.QCheckBox(filesearchDialog)
        self.exp_k_checkBox.setGeometry(QtCore.QRect(130, 20, 16, 17))
        self.exp_k_checkBox.setText("")
        self.exp_k_checkBox.setChecked(True)
        self.exp_k_checkBox.setObjectName("exp_k_checkBox")
        self.exp_j_checkBox = QtWidgets.QCheckBox(filesearchDialog)
        self.exp_j_checkBox.setGeometry(QtCore.QRect(150, 20, 16, 17))
        self.exp_j_checkBox.setText("")
        self.exp_j_checkBox.setObjectName("exp_j_checkBox")
        self.ana_k_checkBox = QtWidgets.QCheckBox(filesearchDialog)
        self.ana_k_checkBox.setGeometry(QtCore.QRect(130, 40, 16, 17))
        self.ana_k_checkBox.setText("")
        self.ana_k_checkBox.setChecked(True)
        self.ana_k_checkBox.setObjectName("ana_k_checkBox")
        self.ana_j_checkBox = QtWidgets.QCheckBox(filesearchDialog)
        self.ana_j_checkBox.setGeometry(QtCore.QRect(150, 40, 16, 17))
        self.ana_j_checkBox.setText("")
        self.ana_j_checkBox.setObjectName("ana_j_checkBox")
        self.label_3 = QtWidgets.QLabel(filesearchDialog)
        self.label_3.setGeometry(QtCore.QRect(100, 20, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(filesearchDialog)
        self.label_4.setGeometry(QtCore.QRect(100, 40, 21, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(filesearchDialog)
        self.label_5.setGeometry(QtCore.QRect(130, 6, 20, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(filesearchDialog)
        self.label_6.setGeometry(QtCore.QRect(150, 9, 20, 16))
        self.label_6.setObjectName("label_6")
        self.retranslateUi(filesearchDialog)
        QtCore.QMetaObject.connectSlotsByName(filesearchDialog)

    def retranslateUi(self, filesearchDialog):
        filesearchDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "filesearchDialog", "EXP+ANA file management", None
            )
        )
        self.findfoldersButton.setText(
            QtCore.QCoreApplication.translate("filesearchDialog", "find folders", None)
        )
        self.label.setText(
            QtCore.QCoreApplication.translate(
                "filesearchDialog", "Search within\n" "exp/ana file", None
            )
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate(
                "filesearchDialog", "Search within\n" "folder name", None
            )
        )
        self.label_3.setText(
            QtCore.QCoreApplication.translate("filesearchDialog", "exp", None)
        )
        self.label_4.setText(
            QtCore.QCoreApplication.translate("filesearchDialog", "ana", None)
        )
        self.label_5.setText(
            QtCore.QCoreApplication.translate("filesearchDialog", " K", None)
        )
        self.label_6.setText(
            QtCore.QCoreApplication.translate("filesearchDialog", " J", None)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    filesearchDialog = QtWidgets.QDialog()
    ui = Ui_filesearchDialog()
    ui.setupUi(filesearchDialog)
    filesearchDialog.show()
    sys.exit(app.exec_())
