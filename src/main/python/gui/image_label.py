import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt

class ImageLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(ImageLabel, self).__init__(parent, flags)
        self.bind_image = None

    def setImage(self, image: np.array):
        self.bind_image = ImageQt.ImageQt(image)
        self.setPixmap(QtGui.QPixmap.fromImage(self.bind_image))