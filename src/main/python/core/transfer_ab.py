import math
import itertools
import time
import numpy.linalg
from core.util import *
from multiprocessing import Pool, cpu_count
from core.transfer import *

class Vec3AB:
    def __init__(self, data):
        self.l_channel = data[0]
        self.ab = (data[1], data[2])
        self.data = [self.l_channel] + list(self.ab)

    def __add__(self, other):
        return Vec3AB([self.l_channel] + [x + y for x, y in zip(self.ab, other.ab)])

    def __sub__(self, other):
        return Vec3AB([self.l_channel] + [x - y for x, y in zip(self.ab, other.ab)])

    def __mul__(self, other):
        return Vec3AB([self.l_channel] + [x * other for x in self.ab])

    def __truediv__(self, other):
        return Vec3AB([self.l_channel] + [x / other for x in self.ab])

    def len(self):
        return (sum([x**2 for x in self.ab]))**0.5

def single_color_transfer_ab(color, original_c, modified_c):
    def get_boundary(origin, direction, k_min, k_max, iters=20):
        start = origin + direction * k_min
        end = origin + direction * k_max
        for _ in range(iters):
            mid = (start + end) / 2
            if ValidAB(mid.ab):
                start = mid
            else:
                end = mid
        return (start + end) / 2

    #init
    color = Vec3AB(color)
    original_c = Vec3AB(original_c)
    modified_c = Vec3AB(modified_c)
    offset = modified_c - original_c

    #get boundary
    c_boundary = get_boundary(original_c, offset, 1, 255)
    naive = (color + offset)
    if ValidAB(naive.ab) and ValidLAB(naive.data) and ValidRGB(LABtoRGB(naive.data)):
        boundary = get_boundary(color, offset, 1, 255)
    else:
        boundary = get_boundary(modified_c, color - original_c, 0, 1)

    #transfer
    if (boundary - color).len() == 0:
        result = color
    elif (boundary - color).len() < (c_boundary - original_c).len():
        result = color + (boundary - color) * (offset.len() / (c_boundary - original_c).len())
    else:
        result = color + (boundary - color) * (offset.len() / (boundary - color).len())

    return result

def multiple_color_transfer_ab(color, original_p, modified_p):
    #single color transfer
    color_st = []
    for i in range(len(original_p)):
        color_st.append(single_color_transfer_ab(color, original_p[i], modified_p[i]))

    #get weights
    weights = calc_weights(color, original_p)

    #calc result
    color_mt = Vec3AB([0, 0, 0])
    for i in range(len(original_p)):
        color_mt = color_mt + color_st[i] * weights[i]

    return color_mt.data

def multiple_color_transfer_ab_mt(args):
    return multiple_color_transfer_ab(*args)

def image_transfer_ab(image, original_p, modified_p, sample_level=16, luminance_flag=False):
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
            lab = pool.map(multiple_color_transfer_ab_mt, args)

        for i in range(len(sample_colors)):
            sample_color_map[sample_colors[i]] = ByteLAB((l[i], *lab[i][-2:]))
    else:
        with Pool(cpu_count()-1) as pool:
            lab = pool.map(multiple_color_transfer_ab_mt, args)

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
