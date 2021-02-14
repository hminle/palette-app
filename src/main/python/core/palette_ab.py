import itertools
import math
from sklearn.cluster import KMeans
import numpy as np
from .util import *

def simple_bins_ab(bins, size=16):
    level = 256//size
    temp = {}
    for x in itertools.product(range(size), repeat=2):
        temp[x] = {'L':0, 'size': 0, 'sum': [0, 0]}

    for color, count in bins.items():
        index = (color[1]//level, color[2]//level) # only ab
        for i in range(2):
            temp[index]['sum'][i] += color[i+1] * count
        temp[index]['size'] += count
        temp[index]['L'] += color[0] * count

    result = {}
    for color in temp.values():
        if color['size'] != 0:
            result[(color['L']/color['size'], color['sum'][0]/color['size'], color['sum'][1]/color['size'])] = color['size']
    return result

def init_means_ab(bins, k):
    def attenuation(color, target):
        return 1 - math.exp(((distance(color, target)/80)**2) * -1)

    #init
    colors = []
    for color, count in bins.items():
        colors.append([count, (color[1], color[2])]) #only ab
    colors.sort(reverse=True)

    #select
    result = []
    for _ in range(k):
        for color in colors:
            if color[1] not in result:
                result.append(color[1])
                break

        for i in range(len(colors)):
            colors[i][0] *= attenuation(colors[i][1], result[-1])

        colors.sort(reverse=True)

    return result

def add_L_channel(kmeans, colors):
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    cluter_centers_L = np.zeros((cluster_centers.shape[0], 3))
    cluter_centers_L[:, 1:None] = cluster_centers
    for i in range(cluster_centers.shape[0]):
        cluter_centers_L[i, 0] = np.mean(colors[labels == i,0])
    return cluter_centers_L

def build_palette_ab(image, num_palettes=5, random_init=False, black=True, threshold=0):
    #get colors
    colors = image.getcolors(image.width * image.height)
    print('colors num:', len(colors))

    #build bins
    bins = {}
    for count, pixel in colors:
        bins[(pixel)] = count
    bins = simple_bins_ab(bins)

    #init means
    init_pixels = init_means_ab(bins, num_palettes)

    colors = []
    weights = []
    for color in bins.keys():
        colors.append(color)
        weights.append(bins[color])
    
    init_pixels = np.array(init_pixels)
    colors = np.array(colors)
    weights = np.array(weights)

    if threshold > 0:
        weights[weights > threshold] = threshold

    kmeans = KMeans(n_clusters=num_palettes, 
                    init=init_pixels).fit(colors[:,1:None], sample_weight=weights)
    cluster_centters_L = add_L_channel(kmeans, colors)
    palette = [tuple([int(x) for x in color]) for color in cluster_centters_L]
    return palette
                    