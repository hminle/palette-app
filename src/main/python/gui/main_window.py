# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import math
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from typing import List, Optional
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLabel, QScrollArea, QPushButton
from PyQt5.QtGui import QImage
from skimage import io, util, transform
import numpy as np
from utils import limit_scale, generateGlobalPalettes, generateLocalPalettes
from PIL import Image, ImageQt
from gui.palette_label import PaletteLabel
from gui.palette_controller import PaletteController
from gui.image_label import ImageLabel

# import matplotlib
# matplotlib.use('Qt5Agg')
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure

# class MplCanvas(FigureCanvas):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super(MplCanvas, self).__init__(fig)

GLOBAL_COLOR_PALETTE_SIZE = 60
LOCAL_COLOR_PALETTE_SIZE = 20

class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()

        self.ctx: ApplicationContext = ctx 
        self.palette_num: int = 5
        self.window_size: int = 5
        self.overlap_size: int = 0
        self.overlap_size_interval: int = 100
        self.setupUi()

    def setupUi(self) -> None:
        print("Setup UI")
        self.setObjectName("MainWindow")
        self.resize(826, 597)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageLabel = ImageLabel(self.centralwidget)
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
        
        # self.globalColorPalette = QtWidgets.QLabel(self.centralwidget)
        # self.globalColorPalette.setEnabled(True)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(1)
        # sizePolicy.setHeightForWidth(self.globalColorPalette.sizePolicy().hasHeightForWidth())
        # self.globalColorPalette.setSizePolicy(sizePolicy)
        # self.globalColorPalette.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # self.globalColorPalette.setText("")
        # self.globalColorPalette.setObjectName("globalColorPalette")

        self.globalPalettes: List[PaletteLabel] = []
        for i in range(self.palette_num):
            self.globalPalettes.append(PaletteLabel(self, palette_index=i))
            self.globalPalettes[-1].setAlignment(Qt.AlignCenter)
            #self.globalPalettes[-1].setColor(np.array((0, 0, 0)).astype(np.float32))
        self.globalPalettesLayout = QtWidgets.QHBoxLayout()
        for label in self.globalPalettes:
            self.globalPalettesLayout.addWidget(label)

        # self.verticalLayout.addWitget(self.globalColorPalette)
        self.verticalLayout.addLayout(self.globalPalettesLayout)

        self.localColorPalettes = QtWidgets.QWidget(self.centralwidget) #Fix here
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.localColorPalettes.sizePolicy().hasHeightForWidth())
        self.localColorPalettes.setSizePolicy(sizePolicy)
        # self.localColorPalettes.setText("")
        self.localColorPalettes.setObjectName("localColorPalettes")
        # self.verticalLayout.addWidget(self.localColorPalettes)


        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.gridLayout.addWidget(self.openButton, 0, 0, 1, 2)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.gridLayout.addWidget(self.resetButton, 0, 2, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(588, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        
        self.numWindowLabel = QtWidgets.QLabel(self.centralwidget)
        self.numWindowLabel.setObjectName("numWindowLabel")
        self.gridLayout.addWidget(self.numWindowLabel, 1, 0, 1, 1)

        self.numWindowSlider = QtWidgets.QSlider(self.centralwidget)
        self.numWindowSlider.setMinimum(1)
        self.numWindowSlider.setMaximum(10)
        self.numWindowSlider.setSingleStep(1)
        self.numWindowSlider.setValue(self.window_size)
        self.numWindowSlider.setSliderPosition(self.window_size)
        self.numWindowSlider.setOrientation(QtCore.Qt.Horizontal)
        self.numWindowSlider.setObjectName("numWindowSlider")
        self.gridLayout.addWidget(self.numWindowSlider, 1, 1, 1, 2)

        self.numWindowDisplay = QtWidgets.QLabel(self.centralwidget)
        self.numWindowDisplay.setObjectName("numWindowDisplay")
        self.gridLayout.addWidget(self.numWindowDisplay, 1, 3, 1, 1)

        self.overlapSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeLabel.setObjectName("overlapSizeLabel")
        self.gridLayout.addWidget(self.overlapSizeLabel, 2, 0, 1, 1)

        self.overlapSizeSlider = QtWidgets.QSlider(self.centralwidget)
        self.overlapSizeSlider.setMinimum(0)
        self.overlapSizeSlider.setMaximum(1000)
        self.overlapSizeSlider.setTickInterval(self.overlap_size_interval)
        self.overlapSizeSlider.setSingleStep(self.overlap_size_interval)
        self.overlapSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.overlapSizeSlider.setObjectName("overlapSizeSlider")
        self.gridLayout.addWidget(self.overlapSizeSlider, 2, 1, 1, 2)

        self.overlapSizeDisplay = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeDisplay.setObjectName("overlapSizeDisplay")
        self.gridLayout.addWidget(self.overlapSizeDisplay, 2, 3, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Add code
        self.palette_controller = None
        self.openButton.clicked.connect(self.handleOpenButtonClicked)
        self.resetButton.clicked.connect(self.handleResetButtonClicked)
        self.numWindowSlider.valueChanged['int'].connect(self.handleNumWindowChange)
        self.overlapSizeSlider.valueChanged['int'].connect(self.handleOverlapSizeChange)
        self.imageLabelWidth: int = 800
        self.imageLabelHeight: int = 600

        self.localPalettesLayout = QtWidgets.QVBoxLayout()
        self.localPalettesLayout.setObjectName("localPalettesLayout")
        self.localPalettes: List[PaletteLabel] = []

        self.localColorPalettes.setLayout(self.localPalettesLayout)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.localColorPalettes)

        self.verticalLayout.addWidget(self.scroll)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Palette App"))
        self.overlapSizeDisplay.setText(_translate("MainWindow", "0"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.numWindowDisplay.setText(_translate("MainWindow", f"{self.window_size}x{self.window_size}"))
        self.numWindowLabel.setText(_translate("MainWindow", "Num Window"))
        self.overlapSizeLabel.setText(_translate("MainWindow", "Overlap Size"))
    
    def handleNumWindowChange(self, value: int):
        self.window_size = value
        self.numWindowDisplay.setText(f"{value}x{value}")
        # if self.palette_controller is not None:
        #     self.clearLayout(self.localPalettesLayout)
        #     self.setAllLocalColorPalettes()

    def handleOverlapSizeChange(self, value: int):
        real_value = round(value / self.overlap_size_interval)*self.overlap_size_interval
        self.overlap_size = real_value
        self.overlapSizeSlider.setTickPosition(real_value)
        self.overlapSizeDisplay.setText(str(real_value))
        if self.palette_controller is not None:
            self.clearLayout(self.localPalettesLayout)
            # self.setAllLocalColorPalettes()

    def handleOpenButtonClicked(self):
        input_path = QFileDialog.getOpenFileName()[0]
        print(input_path)
        if self.palette_controller is None:
            self.palette_controller = PaletteController(self)
        self.palette_controller.load_image(input_path)
        global_palette_Lab = self.palette_controller.generate_global_palettes()
        self.__setGlobalPalettes(global_palette_Lab)
        input_image = self.palette_controller.get_current_image()
        self.setPhoto(input_image)

        self.clearLayout(self.localPalettesLayout)
        local_color_palettes = self.palette_controller.generate_local_palettes(self.overlap_size, 
                                                                               self.window_size)
        self.__setLocalColorPalettes(local_color_palettes)
        # self.setAllLocalColorPalettes()

    def handleResetButtonClicked(self):
        original_image = self.palette_controller.get_original_image()
        self.setPhoto(original_image)

    def handlePaletteLabelClicked(self, chosen_color_Lab, is_global, palette_index):
        if is_global:
            self.globalPalettes[palette_index].setColor(chosen_color_Lab, 
                                                        size=GLOBAL_COLOR_PALETTE_SIZE)
            self.palette_controller.handleGlobalPaletteChanged(chosen_color_Lab, palette_index)

    def setPhoto(self, image):
        print("SET NEW IMAGE")
        self.imageLabel.setImage(limit_scale(image, self.imageLabelWidth, self.imageLabelHeight))

    def __setGlobalPalettes(self, global_palette_Lab):
        for i in range(len(global_palette_Lab)):
            self.globalPalettes[i].setColor(global_palette_Lab[i], 
                                            size=GLOBAL_COLOR_PALETTE_SIZE)
    
    def __setLocalColorPalettes(self, local_color_palettes):
        count_palette_index = 0
        for i in range(len(local_color_palettes)):
            count_palette_index += 1
            hLayout = QtWidgets.QHBoxLayout()
            for color in local_color_palettes[i]:
                paletteLabel = PaletteLabel(self, is_global=False, palette_index=count_palette_index)
                paletteLabel.setAlignment(Qt.AlignCenter)
                paletteLabel.setColor(color, size=30)
                self.localPalettes.append(paletteLabel)
                hLayout.addWidget(paletteLabel)
            self.localPalettesLayout.addLayout(hLayout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())