# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_reduce_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 512)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/General/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.exportSpecular = QtWidgets.QCheckBox(self.groupBox_2)
        self.exportSpecular.setChecked(True)
        self.exportSpecular.setObjectName("exportSpecular")
        self.verticalLayout.addWidget(self.exportSpecular)
        self.export_SA = QtWidgets.QCheckBox(self.groupBox_2)
        self.export_SA.setEnabled(True)
        self.export_SA.setObjectName("export_SA")
        self.verticalLayout.addWidget(self.export_SA)
        self.exportOffSpecular = QtWidgets.QCheckBox(self.groupBox_2)
        self.exportOffSpecular.setObjectName("exportOffSpecular")
        self.verticalLayout.addWidget(self.exportOffSpecular)
        self.exportOffSpecularCorr = QtWidgets.QCheckBox(self.groupBox_2)
        self.exportOffSpecularCorr.setObjectName("exportOffSpecularCorr")
        self.verticalLayout.addWidget(self.exportOffSpecularCorr)
        self.exportOffSpecularSmoothed = QtWidgets.QCheckBox(self.groupBox_2)
        self.exportOffSpecularSmoothed.setObjectName("exportOffSpecularSmoothed")
        self.verticalLayout.addWidget(self.exportOffSpecularSmoothed)
        self.exportGISANS = QtWidgets.QCheckBox(self.groupBox_2)
        self.exportGISANS.setObjectName("exportGISANS")
        self.verticalLayout.addWidget(self.exportGISANS)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.multiAscii = QtWidgets.QCheckBox(self.groupBox_3)
        self.multiAscii.setChecked(True)
        self.multiAscii.setObjectName("multiAscii")
        self.gridLayout.addWidget(self.multiAscii, 0, 0, 1, 1)
        self.combinedAscii = QtWidgets.QCheckBox(self.groupBox_3)
        self.combinedAscii.setObjectName("combinedAscii")
        self.gridLayout.addWidget(self.combinedAscii, 0, 1, 1, 1)
        self.matlab = QtWidgets.QCheckBox(self.groupBox_3)
        self.matlab.setObjectName("matlab")
        self.gridLayout.addWidget(self.matlab, 1, 0, 1, 1)
        self.numpy = QtWidgets.QCheckBox(self.groupBox_3)
        self.numpy.setObjectName("numpy")
        self.gridLayout.addWidget(self.numpy, 1, 1, 1, 1)
        self.plot = QtWidgets.QCheckBox(self.groupBox_3)
        self.plot.setChecked(True)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 2, 1, 1, 1)
        self.genx = QtWidgets.QCheckBox(self.groupBox_3)
        self.genx.setObjectName("genx")
        self.gridLayout.addWidget(self.genx, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_7 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.sampleSize = QtWidgets.QDoubleSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleSize.sizePolicy().hasHeightForWidth())
        self.sampleSize.setSizePolicy(sizePolicy)
        self.sampleSize.setDecimals(1)
        self.sampleSize.setProperty("value", 10.0)
        self.sampleSize.setObjectName("sampleSize")
        self.horizontalLayout_4.addWidget(self.sampleSize)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.directoryEntry = QtWidgets.QLineEdit(self.tab)
        self.directoryEntry.setObjectName("directoryEntry")
        self.horizontalLayout_2.addWidget(self.directoryEntry)
        self.toolButton = QtWidgets.QToolButton(self.tab)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.toolButton.setIcon(icon)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.fileNameEntry = QtWidgets.QLineEdit(self.tab)
        self.fileNameEntry.setObjectName("fileNameEntry")
        self.horizontalLayout_3.addWidget(self.fileNameEntry)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.toolButton.clicked.connect(Dialog.change_directory)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.directoryEntry, self.fileNameEntry)
        Dialog.setTabOrder(self.fileNameEntry, self.buttonBox)
        Dialog.setTabOrder(self.buttonBox, self.exportSpecular)
        Dialog.setTabOrder(self.exportSpecular, self.exportOffSpecular)
        Dialog.setTabOrder(self.exportOffSpecular, self.exportOffSpecularCorr)
        Dialog.setTabOrder(self.exportOffSpecularCorr, self.exportOffSpecularSmoothed)
        Dialog.setTabOrder(self.exportOffSpecularSmoothed, self.exportGISANS)
        Dialog.setTabOrder(self.exportGISANS, self.multiAscii)
        Dialog.setTabOrder(self.multiAscii, self.combinedAscii)
        Dialog.setTabOrder(self.combinedAscii, self.matlab)
        Dialog.setTabOrder(self.matlab, self.numpy)
        Dialog.setTabOrder(self.numpy, self.plot)
        Dialog.setTabOrder(self.plot, self.toolButton)
        Dialog.setTabOrder(self.toolButton, self.tabWidget)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Reduction Options"))
        self.groupBox_2.setTitle(_translate("Dialog", "Items"))
        self.exportSpecular.setText(_translate("Dialog", "Specular"))
        self.export_SA.setText(_translate("Dialog", "Spin-Asymmetry"))
        self.exportOffSpecular.setText(_translate("Dialog", "Off-Specular Raw"))
        self.exportOffSpecularCorr.setText(_translate("Dialog", "Off-Specular Corrected"))
        self.exportOffSpecularSmoothed.setText(_translate("Dialog", "Off-Specular Smoothed"))
        self.exportGISANS.setText(_translate("Dialog", "GISANS"))
        self.groupBox_3.setTitle(_translate("Dialog", "Output Formats"))
        self.multiAscii.setText(_translate("Dialog", "ASCII for each channel"))
        self.combinedAscii.setText(_translate("Dialog", "Combined ASCII"))
        self.matlab.setText(_translate("Dialog", "Matlab"))
        self.numpy.setText(_translate("Dialog", "Numpy .npz"))
        self.plot.setText(_translate("Dialog", "Show Plot"))
        self.genx.setText(_translate("Dialog", "GenX"))
        self.label_7.setText(_translate("Dialog", "Sample Size"))
        self.sampleSize.setSuffix(_translate("Dialog", " mm"))
        self.label.setText(_translate("Dialog", "Directory"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "File Naming"))
        self.fileNameEntry.setText(_translate("Dialog", "REF_M_{numbers}_{item}_{state}.{type}"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Output Options"))

import icons_rc
