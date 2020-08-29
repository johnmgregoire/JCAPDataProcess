# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Z:\Documents\PythonCode\JCAP\JCAPDataProcess\QtDesign\CreateExpForm.ui'
#
# Created: Fri Mar 11 13:28:29 2016
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateExpDialog(object):
    def setupUi(self, CreateExpDialog):
        CreateExpDialog.setObjectName("CreateExpDialog")
        CreateExpDialog.resize(1054, 818)
        self.AddMeasPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.AddMeasPushButton.setGeometry(QtCore.QRect(520, 10, 151, 21))
        self.AddMeasPushButton.setObjectName("AddMeasPushButton")
        self.FilterMeasPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.FilterMeasPushButton.setGeometry(QtCore.QRect(520, 40, 151, 21))
        self.FilterMeasPushButton.setObjectName("FilterMeasPushButton")
        self.ImportRunsPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ImportRunsPushButton.setGeometry(QtCore.QRect(110, 40, 81, 21))
        self.ImportRunsPushButton.setObjectName("ImportRunsPushButton")
        self.FilterRunComboBox = QtWidgets.QComboBox(CreateExpDialog)
        self.FilterRunComboBox.setGeometry(QtCore.QRect(510, 90, 161, 22))
        self.FilterRunComboBox.setObjectName("FilterRunComboBox")
        self.PlateAttrEqualComboBox = QtWidgets.QComboBox(CreateExpDialog)
        self.PlateAttrEqualComboBox.setGeometry(QtCore.QRect(860, 20, 81, 22))
        self.PlateAttrEqualComboBox.setObjectName("PlateAttrEqualComboBox")
        self.label = QtWidgets.QLabel(CreateExpDialog)
        self.label.setGeometry(QtCore.QRect(950, 20, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.PlateAttrEqualSpinBox = QtWidgets.QDoubleSpinBox(CreateExpDialog)
        self.PlateAttrEqualSpinBox.setGeometry(QtCore.QRect(970, 20, 62, 22))
        self.PlateAttrEqualSpinBox.setFrame(True)
        self.PlateAttrEqualSpinBox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.PlateAttrEqualSpinBox.setDecimals(3)
        self.PlateAttrEqualSpinBox.setMinimum(-999999.0)
        self.PlateAttrEqualSpinBox.setMaximum(999999.0)
        self.PlateAttrEqualSpinBox.setObjectName("PlateAttrEqualSpinBox")
        self.PlateAttrLessSpinBox = QtWidgets.QDoubleSpinBox(CreateExpDialog)
        self.PlateAttrLessSpinBox.setGeometry(QtCore.QRect(970, 40, 62, 22))
        self.PlateAttrLessSpinBox.setFrame(True)
        self.PlateAttrLessSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.PlateAttrLessSpinBox.setDecimals(3)
        self.PlateAttrLessSpinBox.setMinimum(-999999.0)
        self.PlateAttrLessSpinBox.setMaximum(999999.0)
        self.PlateAttrLessSpinBox.setObjectName("PlateAttrLessSpinBox")
        self.PlateAttrLessComboBox = QtWidgets.QComboBox(CreateExpDialog)
        self.PlateAttrLessComboBox.setGeometry(QtCore.QRect(860, 40, 81, 22))
        self.PlateAttrLessComboBox.setObjectName("PlateAttrLessComboBox")
        self.label_2 = QtWidgets.QLabel(CreateExpDialog)
        self.label_2.setGeometry(QtCore.QRect(950, 40, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.PlateAttrMoreSpinBox = QtWidgets.QDoubleSpinBox(CreateExpDialog)
        self.PlateAttrMoreSpinBox.setGeometry(QtCore.QRect(970, 60, 62, 22))
        self.PlateAttrMoreSpinBox.setFrame(True)
        self.PlateAttrMoreSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.PlateAttrMoreSpinBox.setDecimals(3)
        self.PlateAttrMoreSpinBox.setMinimum(-999999.0)
        self.PlateAttrMoreSpinBox.setMaximum(999999.0)
        self.PlateAttrMoreSpinBox.setObjectName("PlateAttrMoreSpinBox")
        self.label_3 = QtWidgets.QLabel(CreateExpDialog)
        self.label_3.setGeometry(QtCore.QRect(950, 60, 21, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.PlateAttrMoreComboBox = QtWidgets.QComboBox(CreateExpDialog)
        self.PlateAttrMoreComboBox.setGeometry(QtCore.QRect(860, 60, 81, 22))
        self.PlateAttrMoreComboBox.setObjectName("PlateAttrMoreComboBox")
        self.label_6 = QtWidgets.QLabel(CreateExpDialog)
        self.label_6.setGeometry(QtCore.QRect(860, 0, 181, 20))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(CreateExpDialog)
        self.label_7.setGeometry(QtCore.QRect(520, 70, 141, 16))
        self.label_7.setObjectName("label_7")
        self.ExpTextBrowser = QtWidgets.QTextBrowser(CreateExpDialog)
        self.ExpTextBrowser.setGeometry(QtCore.QRect(510, 430, 531, 381))
        self.ExpTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ExpTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ExpTextBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.ExpTextBrowser.setObjectName("ExpTextBrowser")
        self.SaveExpPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.SaveExpPushButton.setGeometry(QtCore.QRect(80, 430, 61, 21))
        self.SaveExpPushButton.setObjectName("SaveExpPushButton")
        self.ImportExpPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ImportExpPushButton.setGeometry(QtCore.QRect(400, 420, 51, 31))
        self.ImportExpPushButton.setObjectName("ImportExpPushButton")
        self.FileSearchLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.FileSearchLineEdit.setGeometry(QtCore.QRect(860, 180, 171, 20))
        self.FileSearchLineEdit.setObjectName("FileSearchLineEdit")
        self.label_8 = QtWidgets.QLabel(CreateExpDialog)
        self.label_8.setGeometry(QtCore.QRect(860, 160, 171, 21))
        self.label_8.setObjectName("label_8")
        self.SampleListLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.SampleListLineEdit.setGeometry(QtCore.QRect(860, 100, 171, 20))
        self.SampleListLineEdit.setText("")
        self.SampleListLineEdit.setObjectName("SampleListLineEdit")
        self.label_9 = QtWidgets.QLabel(CreateExpDialog)
        self.label_9.setGeometry(QtCore.QRect(860, 80, 171, 21))
        self.label_9.setObjectName("label_9")
        self.ExpDescLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.ExpDescLineEdit.setGeometry(QtCore.QRect(650, 400, 341, 20))
        self.ExpDescLineEdit.setObjectName("ExpDescLineEdit")
        self.label_11 = QtWidgets.QLabel(CreateExpDialog)
        self.label_11.setGeometry(QtCore.QRect(550, 400, 91, 16))
        self.label_11.setObjectName("label_11")
        self.RunPriorityLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.RunPriorityLineEdit.setGeometry(QtCore.QRect(510, 260, 161, 20))
        self.RunPriorityLineEdit.setObjectName("RunPriorityLineEdit")
        self.label_12 = QtWidgets.QLabel(CreateExpDialog)
        self.label_12.setGeometry(QtCore.QRect(510, 240, 171, 21))
        self.label_12.setObjectName("label_12")
        self.RunTypeLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.RunTypeLineEdit.setGeometry(QtCore.QRect(560, 120, 91, 20))
        self.RunTypeLineEdit.setObjectName("RunTypeLineEdit")
        self.label_13 = QtWidgets.QLabel(CreateExpDialog)
        self.label_13.setGeometry(QtCore.QRect(510, 120, 51, 16))
        self.label_13.setObjectName("label_13")
        self.RemoveRunsPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.RemoveRunsPushButton.setGeometry(QtCore.QRect(390, 40, 91, 21))
        self.RemoveRunsPushButton.setObjectName("RemoveRunsPushButton")
        self.LastActionLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.LastActionLineEdit.setGeometry(QtCore.QRect(60, 10, 361, 20))
        self.LastActionLineEdit.setObjectName("LastActionLineEdit")
        self.label_15 = QtWidgets.QLabel(CreateExpDialog)
        self.label_15.setGeometry(QtCore.QRect(0, 10, 71, 20))
        self.label_15.setObjectName("label_15")
        self.ExpTypeLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.ExpTypeLineEdit.setGeometry(QtCore.QRect(620, 340, 51, 20))
        self.ExpTypeLineEdit.setObjectName("ExpTypeLineEdit")
        self.label_16 = QtWidgets.QLabel(CreateExpDialog)
        self.label_16.setGeometry(QtCore.QRect(550, 340, 91, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(CreateExpDialog)
        self.label_17.setGeometry(QtCore.QRect(690, 340, 91, 16))
        self.label_17.setObjectName("label_17")
        self.ExpNameLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.ExpNameLineEdit.setEnabled(False)
        self.ExpNameLineEdit.setGeometry(QtCore.QRect(760, 340, 221, 20))
        self.ExpNameLineEdit.setObjectName("ExpNameLineEdit")
        self.label_18 = QtWidgets.QLabel(CreateExpDialog)
        self.label_18.setGeometry(QtCore.QRect(550, 370, 91, 16))
        self.label_18.setObjectName("label_18")
        self.UserNameLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.UserNameLineEdit.setGeometry(QtCore.QRect(620, 370, 121, 20))
        self.UserNameLineEdit.setObjectName("UserNameLineEdit")
        self.line = QtWidgets.QFrame(CreateExpDialog)
        self.line.setGeometry(QtCore.QRect(510, 320, 531, 16))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.AccessLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.AccessLineEdit.setGeometry(QtCore.QRect(830, 370, 121, 20))
        self.AccessLineEdit.setObjectName("AccessLineEdit")
        self.label_19 = QtWidgets.QLabel(CreateExpDialog)
        self.label_19.setGeometry(QtCore.QRect(760, 370, 91, 16))
        self.label_19.setObjectName("label_19")
        self.ClearExpPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ClearExpPushButton.setGeometry(QtCore.QRect(360, 420, 41, 31))
        self.ClearExpPushButton.setObjectName("ClearExpPushButton")
        self.BatchComboBox = QtWidgets.QComboBox(CreateExpDialog)
        self.BatchComboBox.setGeometry(QtCore.QRect(650, 300, 391, 22))
        self.BatchComboBox.setObjectName("BatchComboBox")
        self.BatchPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.BatchPushButton.setGeometry(QtCore.QRect(510, 300, 131, 21))
        self.BatchPushButton.setObjectName("BatchPushButton")
        self.line_2 = QtWidgets.QFrame(CreateExpDialog)
        self.line_2.setGeometry(QtCore.QRect(510, 280, 531, 16))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.ImportExpParamsPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ImportExpParamsPushButton.setGeometry(QtCore.QRect(450, 420, 61, 31))
        self.ImportExpParamsPushButton.setObjectName("ImportExpParamsPushButton")
        self.SearchRunsPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.SearchRunsPushButton.setGeometry(QtCore.QRect(290, 40, 91, 21))
        self.SearchRunsPushButton.setObjectName("SearchRunsPushButton")
        self.RunTreeWidget = QtWidgets.QTreeWidget(CreateExpDialog)
        self.RunTreeWidget.setGeometry(QtCore.QRect(10, 70, 491, 351))
        self.RunTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.RunTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.RunTreeWidget.setHeaderHidden(True)
        self.RunTreeWidget.setExpandsOnDoubleClick(False)
        self.RunTreeWidget.setObjectName("RunTreeWidget")
        self.RunTreeWidget.headerItem().setText(0, "1")
        self.RunTreeWidget.header().setVisible(False)
        self.RunTreeWidget.header().setCascadingSectionResizes(False)
        self.RunTreeWidget.header().setStretchLastSection(True)
        self.ExpTreeWidget = QtWidgets.QTreeWidget(CreateExpDialog)
        self.ExpTreeWidget.setGeometry(QtCore.QRect(10, 460, 491, 351))
        self.ExpTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ExpTreeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.ExpTreeWidget.setHeaderHidden(True)
        self.ExpTreeWidget.setExpandsOnDoubleClick(False)
        self.ExpTreeWidget.setObjectName("ExpTreeWidget")
        self.ExpTreeWidget.headerItem().setText(0, "1")
        self.ExpTreeWidget.header().setVisible(False)
        self.ExpTreeWidget.header().setCascadingSectionResizes(False)
        self.ExpTreeWidget.header().setStretchLastSection(True)
        self.label_20 = QtWidgets.QLabel(CreateExpDialog)
        self.label_20.setGeometry(QtCore.QRect(860, 120, 171, 21))
        self.label_20.setObjectName("label_20")
        self.FileStartLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.FileStartLineEdit.setGeometry(QtCore.QRect(860, 140, 171, 20))
        self.FileStartLineEdit.setObjectName("FileStartLineEdit")
        self.SaveExpGoAnaPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.SaveExpGoAnaPushButton.setGeometry(QtCore.QRect(150, 430, 91, 21))
        self.SaveExpGoAnaPushButton.setObjectName("SaveExpGoAnaPushButton")
        self.getplatemapCheckBox = QtWidgets.QCheckBox(CreateExpDialog)
        self.getplatemapCheckBox.setGeometry(QtCore.QRect(430, 10, 91, 31))
        self.getplatemapCheckBox.setChecked(True)
        self.getplatemapCheckBox.setObjectName("getplatemapCheckBox")
        self.UserFOMLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.UserFOMLineEdit.setGeometry(QtCore.QRect(510, 190, 151, 20))
        self.UserFOMLineEdit.setObjectName("UserFOMLineEdit")
        self.label_21 = QtWidgets.QLabel(CreateExpDialog)
        self.label_21.setGeometry(QtCore.QRect(510, 170, 141, 16))
        self.label_21.setObjectName("label_21")
        self.TechTypeTreeWidget = QtWidgets.QTreeWidget(CreateExpDialog)
        self.TechTypeTreeWidget.setGeometry(QtCore.QRect(680, 30, 171, 251))
        self.TechTypeTreeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.TechTypeTreeWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded
        )
        self.TechTypeTreeWidget.setHeaderHidden(True)
        self.TechTypeTreeWidget.setExpandsOnDoubleClick(False)
        self.TechTypeTreeWidget.setObjectName("TechTypeTreeWidget")
        self.TechTypeTreeWidget.headerItem().setText(0, "1")
        self.TechTypeTreeWidget.header().setVisible(False)
        self.TechTypeTreeWidget.header().setCascadingSectionResizes(False)
        self.TechTypeTreeWidget.header().setStretchLastSection(True)
        self.label_10 = QtWidgets.QLabel(CreateExpDialog)
        self.label_10.setGeometry(QtCore.QRect(680, 10, 171, 16))
        self.label_10.setObjectName("label_10")
        self.savebinaryCheckBox = QtWidgets.QCheckBox(CreateExpDialog)
        self.savebinaryCheckBox.setGeometry(QtCore.QRect(10, 420, 71, 31))
        self.savebinaryCheckBox.setChecked(True)
        self.savebinaryCheckBox.setObjectName("savebinaryCheckBox")
        self.FileNotStartLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.FileNotStartLineEdit.setGeometry(QtCore.QRect(860, 220, 171, 20))
        self.FileNotStartLineEdit.setText("")
        self.FileNotStartLineEdit.setObjectName("FileNotStartLineEdit")
        self.label_14 = QtWidgets.QLabel(CreateExpDialog)
        self.label_14.setGeometry(QtCore.QRect(860, 200, 171, 21))
        self.label_14.setObjectName("label_14")
        self.RaiseErrorPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.RaiseErrorPushButton.setGeometry(QtCore.QRect(1030, 0, 31, 23))
        self.RaiseErrorPushButton.setObjectName("RaiseErrorPushButton")
        self.label_22 = QtWidgets.QLabel(CreateExpDialog)
        self.label_22.setGeometry(QtCore.QRect(860, 240, 171, 21))
        self.label_22.setObjectName("label_22")
        self.FileNotSearchLineEdit = QtWidgets.QLineEdit(CreateExpDialog)
        self.FileNotSearchLineEdit.setGeometry(QtCore.QRect(860, 260, 171, 20))
        self.FileNotSearchLineEdit.setText("")
        self.FileNotSearchLineEdit.setObjectName("FileNotSearchLineEdit")
        self.ImportRunInfoPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ImportRunInfoPushButton.setGeometry(QtCore.QRect(10, 40, 91, 21))
        self.ImportRunInfoPushButton.setObjectName("ImportRunInfoPushButton")
        self.ImportRunFolderPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.ImportRunFolderPushButton.setGeometry(QtCore.QRect(200, 40, 81, 21))
        self.ImportRunFolderPushButton.setObjectName("ImportRunFolderPushButton")
        self.SaveExpGoVisPushButton = QtWidgets.QPushButton(CreateExpDialog)
        self.SaveExpGoVisPushButton.setGeometry(QtCore.QRect(250, 430, 91, 21))
        self.SaveExpGoVisPushButton.setObjectName("SaveExpGoVisPushButton")
        self.retranslateUi(CreateExpDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateExpDialog)

    def retranslateUi(self, CreateExpDialog):
        CreateExpDialog.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Create EXP from RUN", None
            )
        )
        self.AddMeasPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Considering all the imported RUNs, apply the below filters and add files to EXP",
                None,
            )
        )
        self.AddMeasPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Add Measurements to EXP", None
            )
        )
        self.FilterMeasPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.FilterMeasPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Filter Measurments in EXP", None
            )
        )
        self.ImportRunsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.ImportRunsPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Import RUN(s)", None)
        )
        self.FilterRunComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.PlateAttrEqualComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "These are attributes from the platemap file and select values or ranges can be filtered with these 3 (in)equalities",
                None,
            )
        )
        self.label.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "=", None)
        )
        self.label_2.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "<", None)
        )
        self.label_3.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", ">", None)
        )
        self.label_6.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Require the Sample properties:", None
            )
        )
        self.label_7.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Only consider this RUN", None
            )
        )
        self.SaveExpPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "save .exp text file", None
            )
        )
        self.SaveExpPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Save EXP", None)
        )
        self.ImportExpPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import a .exp file, which will clear any existing EXP and RUNs and create new RUNs from the EXP",
                None,
            )
        )
        self.ImportExpPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Import\n" "EXP", None)
        )
        self.FileSearchLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "All raw data filenames regardless of type will be searched for this string.\n"
                " comma-deliminated strings will be searched separately with OR logic",
                None,
            )
        )
        self.label_8.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Require filename to contain:", None
            )
        )
        self.SampleListLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "This should be a single sample number of comma-deliminated list of numbers from the platemap file",
                None,
            )
        )
        self.label_9.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Sample list, e.g. 3,77,111", None
            )
        )
        self.ExpDescLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.label_11.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "EXP description:", None
            )
        )
        self.RunPriorityLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "comma-deliminated list of RUN indeces in tree view.\n"
                "If the same filename appears in multiple runs, this sets the priorty for which is used.",
                None,
            )
        )
        self.label_12.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "RUN priority (high to low):", None
            )
        )
        self.RunTypeLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                'When "Add" to EXP the files within a RUN will be marked with this type',
                None,
            )
        )
        self.RunTypeLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "data", None)
        )
        self.label_13.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "RUN use:", None)
        )
        self.RemoveRunsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.RemoveRunsPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Remove all RUNs", None
            )
        )
        self.LastActionLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.LastActionLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Start", None)
        )
        self.label_15.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Last Action:", None)
        )
        self.ExpTypeLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.ExpTypeLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "eche", None)
        )
        self.label_16.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "EXP type:", None)
        )
        self.label_17.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "EXP name:", None)
        )
        self.ExpNameLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.ExpNameLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "eche", None)
        )
        self.label_18.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "created by:", None)
        )
        self.UserNameLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.UserNameLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "eche", None)
        )
        self.AccessLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Comment string to be included in EXP", None
            )
        )
        self.AccessLineEdit.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "hte", None)
        )
        self.label_19.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "EXP access:", None)
        )
        self.ClearExpPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "save .exp text file", None
            )
        )
        self.ClearExpPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Clear\n" "EXP", None)
        )
        self.BatchComboBox.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Apply all other filteres in this section to only this run",
                None,
            )
        )
        self.BatchPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Considering the files already in the EXP, keep the files that meet all criteria",
                None,
            )
        )
        self.BatchPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Run Batch Process:", None
            )
        )
        self.ImportExpParamsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Open a .exp file and use only the top-level params",
                None,
            )
        )
        self.ImportExpParamsPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Import EXP\n" "Params", None
            )
        )
        self.SearchRunsPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.SearchRunsPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Search for RUNs", None
            )
        )
        self.label_20.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Require filename start with:", None
            )
        )
        self.FileStartLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "All raw data filenames regardless of type will be searched for this string.\n"
                " comma-deliminated strings will be searched separately with OR logic",
                None,
            )
        )
        self.SaveExpGoAnaPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "save .exp text file", None
            )
        )
        self.SaveExpGoAnaPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Save+GoToAna", None)
        )
        self.getplatemapCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Get platemaps\n" "on RUN import", None
            )
        )
        self.UserFOMLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "enter comma-delimited list of string or\n"
                'number FOMS that will become a constant column in the .csv generated by "Analyze Data".\n'
                "After entry complete, you will be prompted for fom names",
                None,
            )
        )
        self.label_21.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "User-defined FOMs", None
            )
        )
        self.label_10.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Select tech+type to add/keep:", None
            )
        )
        self.savebinaryCheckBox.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Save raw\n" "binary", None
            )
        )
        self.FileNotStartLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "This should be a single sample number of comma-deliminated list of numbers from the platemap file",
                None,
            )
        )
        self.label_14.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Require filename to NOT startwith:", None
            )
        )
        self.RaiseErrorPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "err", None)
        )
        self.label_22.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Require filename to NOT contaih:", None
            )
        )
        self.FileNotSearchLineEdit.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "This should be a single sample number of comma-deliminated list of numbers from the platemap file",
                None,
            )
        )
        self.ImportRunInfoPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.ImportRunInfoPushButton.setText(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "Import from .info", None
            )
        )
        self.ImportRunFolderPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog",
                "Import multiple folders and/or .zip, each representing a RUN with a .rcp file",
                None,
            )
        )
        self.ImportRunFolderPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Import Folder", None)
        )
        self.SaveExpGoVisPushButton.setToolTip(
            QtCore.QCoreApplication.translate(
                "CreateExpDialog", "save .exp text file", None
            )
        )
        self.SaveExpGoVisPushButton.setText(
            QtCore.QCoreApplication.translate("CreateExpDialog", "Save+GoToVis", None)
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    CreateExpDialog = QtWidgets.QDialog()
    ui = Ui_CreateExpDialog()
    ui.setupUi(CreateExpDialog)
    CreateExpDialog.show()
    sys.exit(app.exec_())
