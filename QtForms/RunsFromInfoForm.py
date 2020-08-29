# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\RunsFromInfoForm.ui'
#
# Created: Mon Feb 22 14:31:00 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RunsFromInfoDialog(object):
    def setupUi(self, RunsFromInfoDialog):
        RunsFromInfoDialog.setObjectName("RunsFromInfoDialog")
        RunsFromInfoDialog.resize(579, 408)
        self.buttonBox = QtWidgets.QDialogButtonBox(RunsFromInfoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 360, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.FilesTreeWidget = QtWidgets.QTreeWidget(RunsFromInfoDialog)
        self.FilesTreeWidget.setGeometry(QtCore.QRect(10, 10, 561, 341))
        self.FilesTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.FilesTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.FilesTreeWidget.setHeaderHidden(True)
        self.FilesTreeWidget.setExpandsOnDoubleClick(False)
        self.FilesTreeWidget.setObjectName("FilesTreeWidget")
        self.FilesTreeWidget.headerItem().setText(0, "1")
        self.FilesTreeWidget.header().setVisible(False)
        self.FilesTreeWidget.header().setCascadingSectionResizes(False)
        self.FilesTreeWidget.header().setStretchLastSection(True)
        self.plateidLineEdit = QtWidgets.QLineEdit(RunsFromInfoDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(5, 380, 101, 20))
        self.plateidLineEdit.setObjectName("plateidLineEdit")
        self.label = QtWidgets.QLabel(RunsFromInfoDialog)
        self.label.setGeometry(QtCore.QRect(10, 360, 91, 20))
        self.label.setObjectName("label")
        self.typeLineEdit = QtWidgets.QLineEdit(RunsFromInfoDialog)
        self.typeLineEdit.setGeometry(QtCore.QRect(115, 380, 101, 20))
        self.typeLineEdit.setObjectName("typeLineEdit")
        self.label_2 = QtWidgets.QLabel(RunsFromInfoDialog)
        self.label_2.setGeometry(QtCore.QRect(120, 360, 91, 20))
        self.label_2.setObjectName("label_2")
        self.qualityLineEdit = QtWidgets.QLineEdit(RunsFromInfoDialog)
        self.qualityLineEdit.setGeometry(QtCore.QRect(225, 380, 101, 20))
        self.qualityLineEdit.setObjectName("qualityLineEdit")
        self.label_3 = QtWidgets.QLabel(RunsFromInfoDialog)
        self.label_3.setGeometry(QtCore.QRect(230, 360, 91, 20))
        self.label_3.setObjectName("label_3")
        self.ReadInfoPushButton = QtWidgets.QPushButton(RunsFromInfoDialog)
        self.ReadInfoPushButton.setGeometry(QtCore.QRect(340, 370, 51, 31))
        self.ReadInfoPushButton.setObjectName("ReadInfoPushButton")
        self.retranslateUi(RunsFromInfoDialog)
        self.buttonBox.accepted.connect(RunsFromInfoDialog.accept)
        self.buttonBox.rejected.connect(RunsFromInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RunsFromInfoDialog)

    def retranslateUi(self, RunsFromInfoDialog):
        RunsFromInfoDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "RunsFromInfoDialog", "Plate Info File", None
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate("RunsFromInfoDialog", "plate_id:", None)
        )
        self.typeLineEdit.setText(
            QtCore.QCoreApplication.translate("RunsFromInfoDialog", "eche", None)
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate(
                "RunsFromInfoDialog", "run type contains:", None
            )
        )
        self.qualityLineEdit.setText(
            QtCore.QCoreApplication.translate("RunsFromInfoDialog", "Usable", None)
        )
        self.label_3.setText(
            QtCore.QCoreApplication.translate(
                "RunsFromInfoDialog", '"Quality" contains:', None
            )
        )
        self.ReadInfoPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "RunsFromInfoDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.ReadInfoPushButton.setText(
            QtCore.QCoreApplication.translate("RunsFromInfoDialog", "get .info", None)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    RunsFromInfoDialog = QtWidgets.QDialog()
    ui = Ui_RunsFromInfoDialog()
    ui.setupUi(RunsFromInfoDialog)
    RunsFromInfoDialog.show()
    sys.exit(app.exec_())
