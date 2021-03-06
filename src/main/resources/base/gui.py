# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.horizontalLayout.addWidget(self.imageLabel)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.globalColorPalette = QtWidgets.QLabel(self.centralwidget)
        self.globalColorPalette.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.globalColorPalette.sizePolicy().hasHeightForWidth())
        self.globalColorPalette.setSizePolicy(sizePolicy)
        self.globalColorPalette.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.globalColorPalette.setText("")
        self.globalColorPalette.setObjectName("globalColorPalette")
        self.verticalLayout.addWidget(self.globalColorPalette)
        self.localColorPalettes = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.localColorPalettes.sizePolicy().hasHeightForWidth())
        self.localColorPalettes.setSizePolicy(sizePolicy)
        self.localColorPalettes.setText("")
        self.localColorPalettes.setObjectName("localColorPalettes")
        self.verticalLayout.addWidget(self.localColorPalettes)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.overlapSizeNumLabel = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeNumLabel.setObjectName("overlapSizeNumLabel")
        self.gridLayout.addWidget(self.overlapSizeNumLabel, 2, 3, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 2, 1, 1)
        self.numPaletteSlider = QtWidgets.QSlider(self.centralwidget)
        self.numPaletteSlider.setMinimum(0)
        self.numPaletteSlider.setMaximum(30)
        self.numPaletteSlider.setSingleStep(2)
        self.numPaletteSlider.setOrientation(QtCore.Qt.Horizontal)
        self.numPaletteSlider.setObjectName("numPaletteSlider")
        self.gridLayout.addWidget(self.numPaletteSlider, 1, 1, 1, 2)
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(588, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.paletteNumLabel = QtWidgets.QLabel(self.centralwidget)
        self.paletteNumLabel.setObjectName("paletteNumLabel")
        self.gridLayout.addWidget(self.paletteNumLabel, 1, 3, 1, 1)
        self.numPaletteLabel = QtWidgets.QLabel(self.centralwidget)
        self.numPaletteLabel.setObjectName("numPaletteLabel")
        self.gridLayout.addWidget(self.numPaletteLabel, 1, 0, 1, 1)
        self.overlapSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeLabel.setObjectName("overlapSizeLabel")
        self.gridLayout.addWidget(self.overlapSizeLabel, 2, 0, 1, 1)
        self.overlapSizeSlider = QtWidgets.QSlider(self.centralwidget)
        self.overlapSizeSlider.setMinimum(0)
        self.overlapSizeSlider.setMaximum(1000)
        self.overlapSizeSlider.setSingleStep(100)
        self.overlapSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.overlapSizeSlider.setObjectName("overlapSizeSlider")
        self.gridLayout.addWidget(self.overlapSizeSlider, 2, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.overlapSizeNumLabel.setText(_translate("MainWindow", "0"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.paletteNumLabel.setText(_translate("MainWindow", "0"))
        self.numPaletteLabel.setText(_translate("MainWindow", "Num Palettes"))
        self.overlapSizeLabel.setText(_translate("MainWindow", "Overlap Size"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
