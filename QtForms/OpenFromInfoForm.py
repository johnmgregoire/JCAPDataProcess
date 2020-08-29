# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\OpenFromInfoForm.ui'
#
# Created: Fri Mar 11 22:03:21 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenFromInfoDialog(object):
    def setupUi(self, OpenFromInfoDialog):
        OpenFromInfoDialog.setObjectName("OpenFromInfoDialog")
        OpenFromInfoDialog.resize(579, 427)
        self.buttonBox = QtWidgets.QDialogButtonBox(OpenFromInfoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.FilesTreeWidget = QtWidgets.QTreeWidget(OpenFromInfoDialog)
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
        self.plateidLineEdit = QtWidgets.QLineEdit(OpenFromInfoDialog)
        self.plateidLineEdit.setGeometry(QtCore.QRect(5, 380, 101, 20))
        self.plateidLineEdit.setObjectName("plateidLineEdit")
        self.label = QtWidgets.QLabel(OpenFromInfoDialog)
        self.label.setGeometry(QtCore.QRect(10, 360, 91, 20))
        self.label.setObjectName("label")
        self.typeLineEdit = QtWidgets.QLineEdit(OpenFromInfoDialog)
        self.typeLineEdit.setGeometry(QtCore.QRect(115, 380, 101, 20))
        self.typeLineEdit.setObjectName("typeLineEdit")
        self.label_2 = QtWidgets.QLabel(OpenFromInfoDialog)
        self.label_2.setGeometry(QtCore.QRect(120, 360, 91, 20))
        self.label_2.setObjectName("label_2")
        self.searchLineEdit = QtWidgets.QLineEdit(OpenFromInfoDialog)
        self.searchLineEdit.setGeometry(QtCore.QRect(225, 380, 101, 20))
        self.searchLineEdit.setText("")
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.label_3 = QtWidgets.QLabel(OpenFromInfoDialog)
        self.label_3.setGeometry(QtCore.QRect(230, 360, 91, 20))
        self.label_3.setObjectName("label_3")
        self.ReadInfoPushButton = QtWidgets.QPushButton(OpenFromInfoDialog)
        self.ReadInfoPushButton.setGeometry(QtCore.QRect(330, 360, 71, 21))
        self.ReadInfoPushButton.setObjectName("ReadInfoPushButton")
        self.SearchExpPushButton = QtWidgets.QPushButton(OpenFromInfoDialog)
        self.SearchExpPushButton.setGeometry(QtCore.QRect(400, 360, 61, 21))
        self.SearchExpPushButton.setObjectName("SearchExpPushButton")
        self.SearchAnaPushButton = QtWidgets.QPushButton(OpenFromInfoDialog)
        self.SearchAnaPushButton.setGeometry(QtCore.QRect(460, 360, 71, 21))
        self.SearchAnaPushButton.setObjectName("SearchAnaPushButton")
        self.retranslateUi(OpenFromInfoDialog)
        self.buttonBox.accepted.connect(OpenFromInfoDialog.accept)
        self.buttonBox.rejected.connect(OpenFromInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenFromInfoDialog)

    def retranslateUi(self, OpenFromInfoDialog):
        OpenFromInfoDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog", "Plate Info File", None
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate("OpenFromInfoDialog", "plate_id:", None)
        )
        self.typeLineEdit.setText(
            QtCore.QCoreApplication.translate("OpenFromInfoDialog", "eche", None)
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog", "run type contains:", None
            )
        )
        self.label_3.setText(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog", "search string:", None
            )
        )
        self.ReadInfoPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.ReadInfoPushButton.setText(
            QtCore.QCoreApplication.translate("OpenFromInfoDialog", "get .info", None)
        )
        self.SearchExpPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog",
                "find any exp .zip or folders\n"
                "that have the search string but\n"
                " only exps in the first folderwith a hit",
                None,
            )
        )
        self.SearchExpPushButton.setText(
            QtCore.QCoreApplication.translate("OpenFromInfoDialog", "search EXP", None)
        )
        self.SearchAnaPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "OpenFromInfoDialog",
                "find any exp .zip or folders\n"
                "that have the search string but\n"
                " only exps in the first folderwith a hit",
                None,
            )
        )
        self.SearchAnaPushButton.setText(
            QtCore.QCoreApplication.translate("OpenFromInfoDialog", "search ANA", None)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    OpenFromInfoDialog = QtWidgets.QDialog()
    ui = Ui_OpenFromInfoDialog()
    ui.setupUi(OpenFromInfoDialog)
    OpenFromInfoDialog.show()
    sys.exit(app.exec_())
