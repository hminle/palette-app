import copy
import numpy as np
from PIL import Image
from core.palette import *
from core.transfer import *
from core.util import *

class ImageModel:

    def __init__(self):
        self.original_image = None # RGB
        self.current_image = None # RGB
        self.original_color_samples_RGB = None
        self.color_samples_RGB = None 

    def load_image(self, input_path):
        self.original_image = Image.open(input_path)
        self.current_image = copy.deepcopy(self.original_image)
        self.original_color_samples_RGB = self.__get_simple_hist()
        self.color_samples_RGB = self.__get_simple_hist()
        return self.original_image

    def get_current_image(self):
        return copy.deepcopy(self.current_image)

    def get_original_image(self):
        return copy.deepcopy(self.original_image)

    def update_image(self, modified_image):
        self.current_image = modified_image
        self.color_samples_RGB = self.__get_simple_hist()

    def reset(self):
        self.current_image = copy.deepcopy(self.original_image)
        self.color_samples_RGB = self.__get_simple_hist()

    def __get_simple_hist(self):
        #get colors
        image = self.current_image
        colors = image.getcolors(image.width * image.height)

        #build bins
        bins = {}
        for count, color in colors:
            bins[color] = count
        bins = simple_bins(bins)
        temp = []
        for color in bins.keys():
            # color = RegularRGB(LABtoRGB(RegularLAB(color)))
            temp.append(color)
        color_samples_RGB = np.array(temp).astype(np.float32)
        color_samples_RGB = color_samples_RGB/255
        return color_samples_RGB


    def image_transfer(self, image, original_p, modified_p, sample_level=16, luminance_flag=False):
        t = time.time()
        #init
        original_p = [RegularLAB(c) for c in original_p]
        modified_p = [RegularLAB(c) for c in modified_p]
        level = 255 / (sample_level - 1)
        levels = [i * (255/(sample_level-1)) for i in range(sample_level)]

        #build sample color map
        print('Build sample color map')
        t2 = time.time()
        sample_color_map = {}
        sample_colors = RGB_sample_color(sample_level)

        args = []
        for color in sample_colors:
            args.append((RegularLAB(color), original_p, modified_p))

        if luminance_flag:
            with Pool(cpu_count()-1) as pool:
                l = pool.map(luminance_transfer_mt, args)
                lab = pool.map(multiple_color_transfer_mt, args)

            for i in range(len(sample_colors)):
                sample_color_map[sample_colors[i]] = ByteLAB((l[i], *lab[i][-2:]))
        else:
            with Pool(cpu_count()-1) as pool:
                lab = pool.map(multiple_color_transfer_mt, args)

            for i in range(len(sample_colors)):
                sample_color_map[sample_colors[i]] = ByteLAB(lab[i])

        print('Build sample color map time', time.time() - t2)
        t2 = time.time()

        #build color map
        print('Build color map')
        color_map = {}
        colors = image.getcolors(image.width * image.height)

        args = []
        for _, color in colors:
            nc = nearest_color(color, level, levels)
            args.append((color, nc, sample_color_map))
        with Pool(cpu_count()-1) as pool:
            inter_result = pool.map(trilinear_interpolation_mt, args)

        for i in range(len(colors)):
            color_map[colors[i][1]] = tuple([int(x) for x in inter_result[i]])
        print('Build color map time', time.time() - t2)
        t2 = time.time()

        #transfer image
        print('Transfer image')
        result = Image.new('LAB', image.size)
        result_pixels = result.load()
        image_pixels = image.load()
        for i in range(image.width):
            for j in range(image.height):
                result_pixels[i, j] = color_map[image_pixels[i, j]]
        print('Transfer image time', time.time() - t2)

        print('Total time', time.time() - t)
        return result