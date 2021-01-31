# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import math
import numpy as np
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

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas, 
                                                NavigationToolbar2QT as NavigationToolbar)           
from matplotlib.figure import Figure

GLOBAL_COLOR_PALETTE_SIZE = 60
LOCAL_COLOR_PALETTE_SIZE = 20

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.ion()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, projection='3d')
        # self.axes = Axes3D(self.fig)
        super(MplCanvas, self).__init__(self.fig)

class PushButton(QPushButton):

    def __init__(self, index):
        super(PushButton, self).__init__()
        self.index = index

class MainWindow(QMainWindow):

    def __init__(self, ctx):
        super(MainWindow, self).__init__()

        self.ctx: ApplicationContext = ctx 
        self.palette_num: int = 5
        self.window_size: int = 5
        self.overlap_size: int = 0
        self.overlap_size_interval: int = 5
        self.setupUi()

    def setupUi(self) -> None:
        print("Setup UI")
        self.setObjectName("MainWindow")
        self.resize(1100, 700)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralGridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.centralGridLayout.setObjectName("centralGridLayout")
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
        #self.horizontalLayout.addWidget(self.imageLabel)

        self.leftVerticalLayout = QtWidgets.QVBoxLayout()
        self.leftVerticalLayout.setObjectName("leftVerticalLayout")
        self.leftVerticalLayout.addWidget(self.imageLabel)

        self.globalPalettes: List[PaletteLabel] = []
        for i in range(self.palette_num):
            self.globalPalettes.append(PaletteLabel(self, palette_index=i))
            self.globalPalettes[-1].setAlignment(Qt.AlignCenter)
        self.globalPalettesLayout = QtWidgets.QHBoxLayout()
        for i in range(len(self.globalPalettes)):
            showWeightsPushButton = PushButton(i)
            showWeightsPushButton.setText('Show Weights')
            showWeightsPushButton.setObjectName(f"Show Weights {i} th")
            showWeightsPushButton.resize(30, 20)
            showWeightsPushButton.setCheckable(True)
            showWeightsPushButton.clicked.connect(self.handleShowWeightsButtonPressed)
            self.globalPalettesLayout.addWidget(showWeightsPushButton)
            self.globalPalettesLayout.addWidget(self.globalPalettes[i])
        self.leftVerticalLayout.addLayout(self.globalPalettesLayout)
        self.horizontalLayout.addLayout(self.leftVerticalLayout)

        self.rightVerticalLayout = QtWidgets.QVBoxLayout()
        self.rightVerticalLayout.setContentsMargins(0, -1, -1, -1)
        self.rightVerticalLayout.setObjectName("rightVerticalLayout")

        self.localColorPalettes = QtWidgets.QWidget() #Fix here
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.localColorPalettes.sizePolicy().hasHeightForWidth())
        self.localColorPalettes.setSizePolicy(sizePolicy)
        # self.localColorPalettes.setText("")
        self.localColorPalettes.setObjectName("localColorPalettes")

        self.horizontalLayout.addLayout(self.rightVerticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.bottomGridLayout = QtWidgets.QGridLayout()
        self.bottomGridLayout.setObjectName("bottomGridLayout")

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setObjectName("openButton")
        self.bottomGridLayout.addWidget(self.openButton, 0, 0, 1, 1)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setObjectName("resetButton")
        self.bottomGridLayout.addWidget(self.resetButton, 0, 1, 1, 1)

        self.showOriginalButton = QtWidgets.QPushButton(self.centralwidget)
        self.showOriginalButton.setObjectName("showOriginal")
        self.showOriginalButton.setCheckable(True)
        self.showOriginalButton.clicked.connect(self.handleShowOriginalClicked)
        self.bottomGridLayout.addWidget(self.showOriginalButton, 0, 2, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(588, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottomGridLayout.addItem(spacerItem, 0, 3, 1, 1)
        
        self.numWindowLabel = QtWidgets.QLabel(self.centralwidget)
        self.numWindowLabel.setObjectName("numWindowLabel")
        self.bottomGridLayout.addWidget(self.numWindowLabel, 1, 0, 1, 1)

        self.numWindowSlider = QtWidgets.QSlider(self.centralwidget)
        self.numWindowSlider.setMinimum(1)
        self.numWindowSlider.setMaximum(10)
        self.numWindowSlider.setSingleStep(1)
        self.numWindowSlider.setValue(self.window_size)
        self.numWindowSlider.setSliderPosition(self.window_size)
        self.numWindowSlider.setOrientation(QtCore.Qt.Horizontal)
        self.numWindowSlider.setObjectName("numWindowSlider")
        self.bottomGridLayout.addWidget(self.numWindowSlider, 1, 1, 1, 2)

        self.numWindowDisplay = QtWidgets.QLabel(self.centralwidget)
        self.numWindowDisplay.setObjectName("numWindowDisplay")
        self.bottomGridLayout.addWidget(self.numWindowDisplay, 1, 3, 1, 1)

        self.overlapSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeLabel.setObjectName("overlapSizeLabel")
        self.bottomGridLayout.addWidget(self.overlapSizeLabel, 2, 0, 1, 1)

        self.overlapSizeSlider = QtWidgets.QSlider(self.centralwidget)
        self.overlapSizeSlider.setMinimum(0)
        self.overlapSizeSlider.setMaximum(100)
        self.overlapSizeSlider.setTickInterval(self.overlap_size_interval)
        self.overlapSizeSlider.setSingleStep(self.overlap_size_interval)
        self.overlapSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.overlapSizeSlider.setObjectName("overlapSizeSlider")
        self.bottomGridLayout.addWidget(self.overlapSizeSlider, 2, 1, 1, 2)

        self.overlapSizeDisplay = QtWidgets.QLabel(self.centralwidget)
        self.overlapSizeDisplay.setObjectName("overlapSizeDisplay")
        self.bottomGridLayout.addWidget(self.overlapSizeDisplay, 2, 3, 1, 1)

        self.leftVerticalLayout.addLayout(self.bottomGridLayout)
        # self.gridLayout_2.addLayout(self.bottomGridLayout, 1, 0, 1, 1)
        self.centralGridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
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

        self.rightVerticalLayout.addWidget(self.scroll)


        self.matplotlibCanvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        self.toolbar = NavigationToolbar(self.matplotlibCanvas, self)

        self.matplotlibLayout = QtWidgets.QVBoxLayout()
        self.matplotlibLayout.addWidget(self.toolbar)
        self.matplotlibLayout.addWidget(self.matplotlibCanvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        self.matplotlibWidget = QtWidgets.QWidget()
        self.matplotlibWidget.setLayout(self.matplotlibLayout)
        self.rightVerticalLayout.addWidget(self.matplotlibWidget)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Palette App"))
        self.overlapSizeDisplay.setText(_translate("MainWindow", "0"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.showOriginalButton.setText(_translate("MainWindow", "Show Original"))
        self.numWindowDisplay.setText(_translate("MainWindow", f"{self.window_size}x{self.window_size}"))
        self.numWindowLabel.setText(_translate("MainWindow", "Num Window"))
        self.overlapSizeLabel.setText(_translate("MainWindow", "Overlap Size"))
    
    def handleNumWindowChange(self, value: int):
        self.window_size = value
        self.numWindowDisplay.setText(f"{value}x{value}")
        if self.palette_controller is not None:
            self.clearLayout(self.localPalettesLayout)
            image = self.palette_controller.get_image()
            local_color_palettes = self.palette_controller.generate_local_palettes(image,
                                                                                   self.overlap_size, 
                                                                                   self.window_size)
            self.__setLocalColorPalettes(local_color_palettes)

    def handleOverlapSizeChange(self, value: int):
        real_value = round(value / self.overlap_size_interval)*self.overlap_size_interval
        self.overlap_size = real_value
        self.overlapSizeSlider.setTickPosition(real_value)
        self.overlapSizeDisplay.setText(str(real_value))
        if self.palette_controller is not None:
            self.clearLayout(self.localPalettesLayout)
            image = self.palette_controller.get_image()
            local_color_palettes = self.palette_controller.generate_local_palettes(image,
                                                                                   self.overlap_size, 
                                                                                   self.window_size)
            self.__setLocalColorPalettes(local_color_palettes)

    def handleOpenButtonClicked(self):
        input_path = QFileDialog.getOpenFileName()[0]
        print(input_path)
        if self.palette_controller is None:
            self.palette_controller = PaletteController(self)
        self.palette_controller.load_image(input_path)
        global_palette_Lab = self.palette_controller.generate_global_palettes()
        self.__setGlobalPalettes(global_palette_Lab)
        input_image = self.palette_controller.get_image()
        self.setPhoto(input_image)

        self.clearLayout(self.localPalettesLayout)
        local_color_palettes = self.palette_controller.generate_local_palettes(input_image,
                                                                               self.overlap_size, 
                                                                               self.window_size)
        self.__setLocalColorPalettes(local_color_palettes)

        color_samples_RGB = self.palette_controller.image_model.color_samples_RGB
        self.plot(color_samples_RGB)

    def handleResetButtonClicked(self):
        self.palette_controller.reset()
        original_image = self.palette_controller.get_image()
        self.setPhoto(original_image)
        original_global_palette_Lab = self.palette_controller.get_global_palette()
        self.__setGlobalPalettes(original_global_palette_Lab)

        self.clearLayout(self.localPalettesLayout)

        local_color_palettes = self.palette_controller.generate_local_palettes(original_image,
                                                                               self.overlap_size,
                                                                               self.window_size)
        self.__setLocalColorPalettes(local_color_palettes)
        # TODO: remove this matplotlib test
        self.clear_plot()
        color_samples_RGB = self.palette_controller.image_model.color_samples_RGB
        self.plot(color_samples_RGB)

    def handleShowOriginalClicked(self):
        if self.showOriginalButton.isChecked():
            original = self.palette_controller.get_original()
            original_image = original.get('image')
            original_global_palette_Lab = original.get('global_palette')
            self.setPhoto(original_image)
            self.__setGlobalPalettes(original_global_palette_Lab)
            self.clear_plot()
            original_color_samples_RGB = self.palette_controller.image_model.original_color_samples_RGB
            self.plot(original_color_samples_RGB)
        else:
            current = self.palette_controller.get_current()
            current_image = current.get('image')
            current_global_palette_Lab = current.get('global_palette')
            self.setPhoto(current_image)
            self.__setGlobalPalettes(current_global_palette_Lab)
            self.clear_plot()
            color_samples_RGB = self.palette_controller.image_model.color_samples_RGB
            self.plot(color_samples_RGB)
        
    def handlePaletteLabelClicked(self, chosen_color_Lab, is_global, palette_index):
        if is_global:
            self.globalPalettes[palette_index].setColor(chosen_color_Lab, 
                                                        size=GLOBAL_COLOR_PALETTE_SIZE)
            self.palette_controller.handleGlobalPaletteChanged(chosen_color_Lab, palette_index)
            self.clear_plot()
            color_samples_RGB = self.palette_controller.image_model.color_samples_RGB
            self.plot(color_samples_RGB)
            # update local palettes
            self.clearLayout(self.localPalettesLayout)
            image = self.palette_controller.get_image()
            local_color_palettes = self.palette_controller.generate_local_palettes(image,
                                                                                   self.overlap_size,
                                                                                   self.window_size)
            self.__setLocalColorPalettes(local_color_palettes)


    def handleShowWindowButtonPressed(self):
        button_sender = self.sender()
        print(f"Button {button_sender.index} th clicked:")
        palette_index = button_sender.index
        local_palette_info = self.palette_controller.get_single_local_palette(palette_index)
        window_position = local_palette_info.get('window_position')
        self.palette_controller.draw_rectangle(window_position)

    def handleShowWeightsButtonPressed(self):
        button_sender = self.sender()
        if button_sender.isChecked():
            index = button_sender.index
            weights_map = self.palette_controller.image_model.weights_map
            single_map = weights_map[:, :, index]
            map_image = Image.fromarray(single_map)
            map_image = map_image.convert("L")
            self.setPhoto(map_image)
        else:
            image = self.palette_controller.get_image()
            self.setPhoto(image)


        
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
            pushButton = PushButton(i)
            pushButton.setText('Show')
            pushButton.setObjectName(f"Show Button {i} th")
            pushButton.resize(30, 20)
            pushButton.pressed.connect(self.handleShowWindowButtonPressed)
            hLayout.addWidget(pushButton)
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

    def plot(self, color_samples_RGB):
        # color_samples_RGB = self.palette_controller.image_model.color_samples_RGB
        self.matplotlibCanvas.axes.scatter(color_samples_RGB[:, 0], 
                                           color_samples_RGB[:, 1], 
                                           color_samples_RGB[:, 2],
                                           c=np.reshape(color_samples_RGB, (-1, 3)))
        self.matplotlibCanvas.draw()

    def clear_plot(self):
        print('Clear Plot')
        self.matplotlibCanvas.axes.cla()
        self.matplotlibCanvas.draw()