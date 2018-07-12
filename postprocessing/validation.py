#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 10:52:53 2018

@author: anandan
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors

filename = "NTUP_FCS.13289379._000001.pool.root.1"
path="/media/anandan/3474068674064B56/CERN/Program/atlas_sim_gan/"

def get_energy(layer):

    with open(path +"data/layer_wise/"+filename+"_Layer_"+str(layer)+".csv", 'r') as f:

        E_l = []
        for i,event in enumerate(f):
            event = event.split(';')[:-1]

            s = 0
            for e in event:
                e = float(e.split(',')[-1])
                if e > 0:
                    s = s + e

            E_l.append(s)

            if i%1000 == 0:
                print("Layer:%d, Event:%d" %(layer,i))

    return np.array(E_l)


E_l0 = get_energy(layer=0)[:2000]
E_l1 = get_energy(layer=1)[:2000]
E_l2 = get_energy(layer=2)[:2000]
E_l3 = get_energy(layer=3)[:2000]
E_l12 = get_energy(layer=12)[:2000]
E_tot = E_l0 + E_l1 + E_l2 + E_l3+ E_l12

#l0, l1, l2, l3, l12, ltot = [], [], [], [], [], []
#
#for i in range(20):
#
#    batch = np.loadtxt("../data/vectorized_cylindrical_positive/batch_%d.csv" %i, delimiter=',')
#
#    layer0_sum = batch[:,:100].sum(axis=1)
#    layer1_sum = batch[:,100:200].sum(axis=1)
#    layer2_sum = batch[:,200:300].sum(axis=1)
#    layer3_sum = batch[:,300:400].sum(axis=1)
#    layer12_sum = batch[:,400:500].sum(axis=1)
#    ltot_sum = batch.sum(axis=1)
#
#    l0.extend(layer0_sum.tolist())
#    l1.extend(layer1_sum.tolist())
#    l2.extend(layer2_sum.tolist())
#    l3.extend(layer3_sum.tolist())
#    l12.extend(layer12_sum.tolist())
#    ltot.extend(ltot_sum.tolist())

batch = np.loadtxt(path+"data/samples/samples_tanh.csv", delimiter=',')
batch[batch<=0] = 0

l0 = batch[:,:100].sum(axis=1)
l1 = batch[:,100:200].sum(axis=1)
l2 = batch[:,200:300].sum(axis=1)
l3 = batch[:,300:400].sum(axis=1)
l12 = batch[:,400:500].sum(axis=1)
ltot = batch.sum(axis=1)

fig = plt.figure()
ax1 = fig.add_subplot(231)
#ax1.hist(E_l0, bins=50, histtype=u'step', density=True, label='Truth')
ax1.hist(l0, bins=50, histtype=u'step', density=True, label='Processed')
ax1.set_title('Layer 0')
ax1.legend()

ax2 = fig.add_subplot(232)
#ax2.hist(E_l1, bins=50, histtype=u'step', density=True, label='Truth')
ax2.hist(l1, bins=50, histtype=u'step', density=True, label='Processed')
ax2.set_title('Layer 1')
ax2.legend()

ax3 = fig.add_subplot(233)
#ax3.hist(E_l2, bins=50, histtype=u'step', density=True, label='Truth')
ax3.hist(l2, bins=50, histtype=u'step', density=True, label='Processed')
ax3.set_title('Layer 2')
ax3.legend()

ax4 = fig.add_subplot(234)
#ax4.hist(E_l3, bins=50, histtype=u'step', density=True, label='Truth')
ax4.hist(l3, bins=50, histtype=u'step', density=True, label='Processed')
ax4.set_title('Layer 3')
ax4.legend()

ax5 = fig.add_subplot(235)
#ax5.hist(E_l12, bins=50, histtype=u'step', density=True, label='Truth')
ax5.hist(l12, bins=50, histtype=u'step', density=True, label='Processed')
ax5.set_title('Layer 12')
ax5.legend()

ax6 = fig.add_subplot(236)
#ax6.hist(E_tot, bins=50, histtype=u'step', density=True, label='Truth')
ax6.hist(ltot, bins=50, histtype=u'step', density=True, label='Processed')
ax6.set_title('All layers')
ax6.legend()
plt.show()
