import 
import numpy as np
from hist_3d import Hist3D
from palette_selection import PaletteSelection
from global_palette import GlobalPalette
from palette.cv.image import rgb2Lab

## Implementation of PaletteManager
class PaletteManager:
    ## Constructor
    #  @param image          input image (numpy.array)
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    #  @param color_space    target color space. 'rgb' or 'Lab' or 'hsv'.

    def __init__(self, image: Optional[numpy.array],
                 num_bins=16, alpha=0.1, color_space='Lab', palette_num=5):
        self.input_img = image
        self.color_space = color_space
        self.num_bins= num_bins
        self.alpha = alpha
        self.palette_num = palette_num

        self.global_palette = GlobalPalette()
        init_palette = self.generate_global_palettes()
        self.global_palette.set_original_palette(init_palette)
        self.global_palette.set_current_palette(init_palette)


    def generate_global_palettes(self):
        hist3D = Hist3D(self.input_img, num_bins=self.num_bins, color_space=self.color_space)
        color_coordinates = hist3D.colorCoordinates()
        color_densities = hist3D.colorDensities()
        rgb_colors = hist3D.rgbColors()
        palette_selection = PaletteSelection(color_coordinates,
                                            color_densities, rgb_colors,
                                            num_colors=self.palette_num, sigma=70.0)
        return palette_selection.paletteColors()

    def lab_transfer(self):
        pass

    def __ab_transfer(self):
        