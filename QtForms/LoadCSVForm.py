# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\LoadCSVForm.ui'
#
# Created: Thu Feb 18 10:30:25 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadCSVDialog(object):
    def setupUi(self, LoadCSVDialog):
        LoadCSVDialog.setObjectName("LoadCSVDialog")
        LoadCSVDialog.resize(325, 344)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoadCSVDialog)
        self.buttonBox.setGeometry(QtCore.QRect(120, 310, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.ellabelsLineEdit = QtWidgets.QLineEdit(LoadCSVDialog)
        self.ellabelsLineEdit.setGeometry(QtCore.QRect(210, 30, 101, 20))
        self.ellabelsLineEdit.setReadOnly(False)
        self.ellabelsLineEdit.setObjectName("ellabelsLineEdit")
        self.label = QtWidgets.QLabel(LoadCSVDialog)
        self.label.setGeometry(QtCore.QRect(170, 20, 41, 31))
        self.label.setObjectName("label")
        self.label_15 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_15.setGeometry(QtCore.QRect(10, 110, 61, 21))
        self.label_15.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_15.setObjectName("label_15")
        self.sampleComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.sampleComboBox.setGeometry(QtCore.QRect(80, 110, 121, 22))
        self.sampleComboBox.setObjectName("sampleComboBox")
        self.xComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.xComboBox.setGeometry(QtCore.QRect(80, 160, 191, 22))
        self.xComboBox.setObjectName("xComboBox")
        self.label_16 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_16.setGeometry(QtCore.QRect(10, 160, 61, 21))
        self.label_16.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_16.setObjectName("label_16")
        self.yComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.yComboBox.setGeometry(QtCore.QRect(80, 180, 191, 22))
        self.yComboBox.setObjectName("yComboBox")
        self.label_17 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_17.setGeometry(QtCore.QRect(10, 180, 61, 21))
        self.label_17.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_17.setObjectName("label_17")
        self.aComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.aComboBox.setGeometry(QtCore.QRect(80, 200, 191, 22))
        self.aComboBox.setObjectName("aComboBox")
        self.label_18 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_18.setGeometry(QtCore.QRect(10, 200, 61, 21))
        self.label_18.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_18.setObjectName("label_18")
        self.bComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.bComboBox.setGeometry(QtCore.QRect(80, 220, 191, 22))
        self.bComboBox.setObjectName("bComboBox")
        self.label_19 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_19.setGeometry(QtCore.QRect(10, 220, 61, 21))
        self.label_19.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_19.setObjectName("label_19")
        self.cComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.cComboBox.setGeometry(QtCore.QRect(80, 240, 191, 22))
        self.cComboBox.setObjectName("cComboBox")
        self.label_20 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_20.setGeometry(QtCore.QRect(10, 240, 61, 21))
        self.label_20.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_20.setObjectName("label_20")
        self.dComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.dComboBox.setGeometry(QtCore.QRect(80, 260, 191, 22))
        self.dComboBox.setObjectName("dComboBox")
        self.label_21 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_21.setGeometry(QtCore.QRect(10, 260, 61, 21))
        self.label_21.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_21.setObjectName("label_21")
        self.codeComboBox = QtWidgets.QComboBox(LoadCSVDialog)
        self.codeComboBox.setGeometry(QtCore.QRect(80, 280, 191, 22))
        self.codeComboBox.setObjectName("codeComboBox")
        self.label_22 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_22.setGeometry(QtCore.QRect(10, 280, 61, 21))
        self.label_22.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_22.setObjectName("label_22")
        self.plateidLineEdit = QtWidgets.QLineEdit(LoadCSVDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(80, 30, 71, 20))
        self.plateidLineEdit.setText("")
        self.plateidLineEdit.setObjectName("plateidLineEdit")
        self.plateidPushButton = QtWidgets.QPushButton(LoadCSVDialog)
        self.plateidPushButton.setGeometry(QtCore.QRect(10, 20, 61, 31))
        self.plateidPushButton.setObjectName("plateidPushButton")
        self.label_2 = QtWidgets.QLabel(LoadCSVDialog)
        self.label_2.setGeometry(QtCore.QRect(80, 60, 91, 16))
        self.label_2.setObjectName("label_2")
        self.platemapLineEdit = QtWidgets.QLineEdit(LoadCSVDialog)
        self.platemapLineEdit.setGeometry(QtCore.QRect(80, 80, 231, 20))
        self.platemapLineEdit.setText("")
        self.platemapLineEdit.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.platemapLineEdit.setObjectName("platemapLineEdit")
        self.platemapPushButton = QtWidgets.QPushButton(LoadCSVDialog)
        self.platemapPushButton.setGeometry(QtCore.QRect(10, 70, 61, 31))
        self.platemapPushButton.setObjectName("platemapPushButton")
        self.useplatemapCheckBox = QtWidgets.QCheckBox(LoadCSVDialog)
        self.useplatemapCheckBox.setGeometry(QtCore.QRect(70, 140, 141, 17))
        self.useplatemapCheckBox.setObjectName("useplatemapCheckBox")
        self.retranslateUi(LoadCSVDialog)
        self.buttonBox.accepted.connect(LoadCSVDialog.accept)
        self.buttonBox.rejected.connect(LoadCSVDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoadCSVDialog)

    def retranslateUi(self, LoadCSVDialog):
        LoadCSVDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog", "ChooseImagesToSave", None
            )
        )
        self.ellabelsLineEdit.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "A,B,C,D", None)
        )
        self.label.setText(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog", "Element\n" "labels", None
            )
        )
        self.label_15.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "sample_no", None)
        )
        self.sampleComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.xComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_16.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "x", None)
        )
        self.yComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_17.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "y", None)
        )
        self.aComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_18.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "A", None)
        )
        self.bComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_19.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "B", None)
        )
        self.cComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_20.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "C", None)
        )
        self.dComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_21.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "D", None)
        )
        self.codeComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.label_22.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "code", None)
        )
        self.plateidPushButton.setText(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog", "Load from\n" "plateid", None
            )
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate("LoadCSVDialog", "platemap path", None)
        )
        self.platemapPushButton.setText(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog", "Load\n" "platemap", None
            )
        )
        self.useplatemapCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "LoadCSVDialog", "Use platemap for these:", None
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoadCSVDialog = QtWidgets.QDialog()
    ui = Ui_LoadCSVDialog()
    ui.setupUi(LoadCSVDialog)
    LoadCSVDialog.show()
    sys.exit(app.exec_())
