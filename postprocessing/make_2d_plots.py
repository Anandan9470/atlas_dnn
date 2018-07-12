#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:52:17 2018

@author: anandan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors

path = '/media/anandan/3474068674064B56/CERN/Program/cern_gan/'

def get_data():

    #data = np.loadtxt(path+"data/vectorized_cylindrical_positive/batch_0.csv", delimiter=',')
    data = np.loadtxt("batch_0.csv", delimiter=',')

    while(True):

        batch = data[np.random.choice(data.shape[0], 50, replace=False)]
        #batch = np.tanh(0.1*np.log(batch+10e-5))
        yield batch

data_gen = get_data()
batch_transformed = data_gen.__next__()

for i,b in enumerate(batch_transformed):

    b = np.reshape(b, newshape=(10,40), order='F')
    b = np.log(b+10e-5)

    b[b<=0] = np.log(10e-5)
    num_levels = 200
    vmin, vmax = b.min(), b.max()
    midpoint = 0
    levels = np.linspace(vmin, vmax, num_levels)
    midp = np.mean(np.c_[levels[:-1], levels[1:]], axis=1)
    vals = np.interp(midp, [vmin, midpoint, vmax], [0, 0.5, 1])
    colors = plt.cm.seismic(vals)
    cmap, norm = from_levels_and_colors(levels, colors)

    fig, ax = plt.subplots()
    im = ax.imshow(b, cmap=cmap, norm=norm, interpolation='none')
    fig.colorbar(im)
    plt.savefig('a%d.png' %i)
    plt.close()