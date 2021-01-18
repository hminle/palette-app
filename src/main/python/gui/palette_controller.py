import math
import copy
import numpy as np
from PIL import Image, ImageQt
from gui.global_palette_model import GlobalPaletteModel
from gui.local_palette_model import LocalPaletteModel
from core.util import rgb2lab, lab2rgb
from core.palette import build_palette
from core.transfer import image_transfer
from gui.image_model import ImageModel

class PaletteController:

    def __init__(self, main_window):
        self.main_window = main_window
        self.global_palette_model = GlobalPaletteModel()
        self.local_palette_model = LocalPaletteModel()
        self.image_model = ImageModel()

    def load_image(self, input_path):
        self.image_model.load_image(input_path)

    def get_current_image(self):
        return self.image_model.get_current_image()

    def get_original_image(self):
        return self.image_model.get_original_image()

    def generate_global_palettes(self):
        input_image = self.image_model.get_current_image()
        input_image_Lab = rgb2lab(input_image)
        global_palette_Lab = build_palette(input_image_Lab)
        self.global_palette_model.set_palette(global_palette_Lab)
        return global_palette_Lab

    def generate_local_palettes(self, overlap_size, window_size):
        input_image = self.image_model.get_current_image()
        local_color_palettes = []
        num_col_slides = window_size
        num_row_slides = window_size
        height = input_image.height
        width = input_image.width
        total_slides = num_col_slides*num_row_slides
        row_step = math.floor((height)/num_col_slides)
        col_step = math.floor((width)/num_row_slides)
        count = 0

        for i in range(0, height, row_step):
            if i + row_step > height:
                continue
            else:
                for j in range(0, width, col_step):
                    if j + col_step > width:
                        continue
                    else:
                        count += 1
                        if count <= total_slides:
                            row_step_final = row_step if ((i + row_step + overlap_size) > height) else (row_step + overlap_size)
                            col_step_final = col_step if ((j + col_step + overlap_size) > width) else (col_step + overlap_size) 
                            # left upper right lower
                            sample_img = input_image.crop((j, i, j+col_step_final, i+row_step_final))
                            sample_Lab = rgb2lab(sample_img)

                            #build palette
                            sample_palette_Lab = build_palette(sample_Lab)
                            local_color_palettes.append(sample_palette_Lab)
                        else: 
                            break
        return local_color_palettes

    def handleGlobalPaletteChanged(self, chosen_color_Lab, palette_index):
        source_palette = copy.deepcopy(self.global_palette_model.get_current_palette())
        self.global_palette_model.update_palette(chosen_color_Lab, palette_index)
        target_palette = self.global_palette_model.get_current_palette()
        target_image_RGB = self.__transfer_image(source_palette, target_palette)
        self.image_model.update_image(target_image_RGB)
        self.main_window.setPhoto(target_image_RGB)

    def __transfer_image(self, source_palette, target_palette):
        source_image = self.image_model.get_current_image()
        print(f"SOURCE {source_palette}")
        print(f"TARGETT {target_palette}")
        source_image_Lab = rgb2lab(source_image)
        target_image_Lab = image_transfer(source_image_Lab, 
                                     source_palette, 
                                     target_palette, 
                                     sample_level=10, 
                                     luminance_flag=False)
        target_image_RGB = lab2rgb(target_image_Lab)
        return target_image_RGB

        
