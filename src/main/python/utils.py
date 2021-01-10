from PIL import Image, ImageCms
from palette.io_util.image import loadRGB
from palette.core.hist_3d import Hist3D
from palette.core.palette_selection import PaletteSelection

def limit_scale(image, width, height):
    if image.width > width or image.height > height:
        if image.width/image.height > width/height:
            scale_size = (width, width * image.height//image.width)
        else:
            scale_size = (height * image.width//image.height, height)

        return image.resize(scale_size)
    else:
        return image

def generateGlobalPalettes(input_img, palette_num=5):
    hist3D = Hist3D(input_img, num_bins=16, color_space='Lab')
    color_coordinates = hist3D.colorCoordinates()
    color_densities = hist3D.colorDensities()
    rgb_colors = hist3D.rgbColors()
    palette_selection = PaletteSelection(color_coordinates,
                                        color_densities, rgb_colors,
                                        num_colors=palette_num, sigma=70.0)
    return palette_selection.paletteColors()

def generateLocalPalettes(input_img, row_step, col_step, overlap_size, total_slides):
    count = 0
    localPalettesList = []
    height = input_img.shape[0]
    width = input_img.shape[1]
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
                        sample_img = input_img[i : i + row_step_final, j : j + col_step_final, :]

                        hist3D = Hist3D(sample_img, num_bins=16, color_space='Lab')
                        color_coordinates = hist3D.colorCoordinates()
                        color_densities = hist3D.colorDensities()
                        rgb_colors = hist3D.rgbColors()
                        palette_selection = PaletteSelection(color_coordinates,
                                                             color_densities, rgb_colors,
                                                             num_colors=5, sigma=70.0)
                        localPalettesList.append(palette_selection.paletteColors())
                    else: 
                        break
    return localPalettesList