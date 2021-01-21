import numpy as np
from typing import Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor
from PIL import Image, ImageQt
from gui.image_label import ImageLabel
from core.palette import draw_color
from core.util import *


class PaletteLabel(ImageLabel):
    
    def __init__(self, parent, is_global=True, palette_index = -1,flags=Qt.WindowFlags()) -> None:
        super(PaletteLabel, self).__init__(parent, flags)
        self.palette_index = palette_index
        self.bind_color = None #Lab
        self.parent = parent
        self.is_global = is_global

    def setColor(self, color_Lab, size=100):
        self.bind_color = color_Lab
        self.setImage(draw_color(color_Lab, size=size))
        self.repaint()

    def mousePressEvent(self, event):
        #get color
        current_color = QColor(*RegularRGB(LABtoRGB(RegularLAB(self.bind_color))))
        chosen_color = QColorDialog.getColor(initial=current_color, options=QColorDialog.DontUseNativeDialog)
        if not chosen_color.isValid():
            return

        chosen_color_RGB = chosen_color.red(), chosen_color.green(), chosen_color.blue()
        chosen_color_Lab = ByteLAB(RGBtoLAB(chosen_color_RGB))
        self.parent.handlePaletteLabelClicked(chosen_color_Lab, self.is_global, self.palette_index)