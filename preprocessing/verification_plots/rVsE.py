#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 14:25:18 2018

@author: anandan
"""

import numpy as np
import pandas as pd
from pyntcloud import PyntCloud
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import warnings
warnings.filterwarnings("ignore")

path = "/media/anandan/3474068674064B56/CERN/Program/atlas_sim_gan/"
filename = "NTUP_FCS.13289379._000001.pool.root.1"

def get_hits(event_range=range(0,10), layer=0):

    xyzE = []

    with open(path+"data/layer_wise/"+filename+"_Layer_"+str(layer)+".csv", 'r') as f:
        for i,event in enumerate(f):

            if i in event_range:

                event = event.split(';')

                xyzE_temp = np.array([[], [], [], [], []]).T


                for hit in event[:-1]:
                    hit = hit.split(',')

                    xyzE_temp = np.vstack((xyzE_temp, np.array([float(hit[0]),
                                                                float(hit[1]),
                                                                float(hit[2]),
                                                                float(hit[4]),
                                                                layer])))
                xyzE.append(xyzE_temp)

            if i == event_range[-1]:
                break

    return xyzE

def get_events(event_range=range(0,10)):

    xyzE_layer = []

    for layer in [0,1,2,3,12]:
        hits = get_hits(event_range=event_range, layer=layer)
        xyzE_layer.append(hits)

    xyzE = []

    for i in range(len(event_range)):

        xyzE_temp = np.concatenate((xyzE_layer[0][i],
                                    xyzE_layer[1][i],
                                    xyzE_layer[2][i],
                                    xyzE_layer[3][i],
                                    xyzE_layer[4][i]))

        xyzE.append(xyzE_temp)

    return xyzE

def filter_hits_by_dynamic_angle(event_spherical, layer, multiplier=2):

    layer_bool_array = event_spherical.colors == layer

    if layer != 'r':
        event_spherical_layer = event_spherical.loc[layer_bool_array]
    else:
        event_spherical_layer = event_spherical.loc[event_spherical.colors == 'b']

    if event_spherical_layer.shape[0] < 3:
        return event_spherical

    eta_upper = event_spherical_layer.eta.mean() + multiplier*event_spherical_layer.eta.std()
    eta_lower = event_spherical_layer.eta.mean() - multiplier*event_spherical_layer.eta.std()
    phi_upper = event_spherical_layer.phi.mean() + multiplier*event_spherical_layer.phi.std()
    phi_lower = event_spherical_layer.phi.mean() - multiplier*event_spherical_layer.phi.std()

    eta_bool_array = np.logical_and(event_spherical.eta.values<eta_upper, event_spherical.eta>eta_lower)
    phi_bool_array = np.logical_and(event_spherical.phi.values<phi_upper, event_spherical.phi>phi_lower)
    event_bool_array = np.logical_or(np.logical_and(eta_bool_array, phi_bool_array),
                                     np.logical_not(layer_bool_array))

    event_spherical = event_spherical[event_bool_array]

    return event_spherical

def filter_hits_by_angle(event_spherical, r_angles, alpha_angles, layer):

    r_lower, r_upper = r_angles[0], r_angles[1]
    alpha_lower, alpha_upper = alpha_angles[0], alpha_angles[1]

    r_bool_array = np.logical_and(event_spherical.r.values<r_upper, event_spherical.r>r_lower)
    alpha_bool_array = np.logical_and(event_spherical.alpha.values<alpha_upper, event_spherical.alpha>alpha_lower)
    event_bool_array = np.logical_and(r_bool_array, alpha_bool_array)

    event_spherical = event_spherical[event_bool_array]

    return event_spherical

def voxalize_by_layer(event_cylindrical, layer, segments):

    event_cylindrical_layer_wise = event_cylindrical.loc[event_cylindrical.colors==layer, :]

    if event_cylindrical_layer_wise.shape[0] == 0:
        return np.zeros(shape=((len(segments[0])-1) *
                               (len(segments[1])-1) *
                               (len(segments[2])) ))

    ref_cloud = PyntCloud(event_cylindrical_layer_wise)
    voxelgrid_id = ref_cloud.add_structure("voxelgrid", segments=segments)
    feature_vector = ref_cloud.structures[voxelgrid_id].query_voxels(event_cylindrical_layer_wise.loc[:,['r','alpha','z']].values,
                                                                     event_cylindrical_layer_wise.loc[:,'E'].values)

    return feature_vector.reshape((-1,))

events_r = []
events_E = []


for n in range(0,1):

    s = n*100
    e = s+200

    event_range = range(s,e)
    xyzE = get_events(event_range)

    print("Percentage complted: %10.2f" %(n))

    batch = np.empty((0,400), float)

    for i, event in enumerate(event_range):

        event_cartisian = xyzE[i]

        event_cartisian = pd.DataFrame(event_cartisian, columns=['x','y','z','E','colors'])

        event_cartisian.colors[event_cartisian.colors==0] = 'r'
        event_cartisian.colors[event_cartisian.colors==1] = 'b'
        event_cartisian.colors[event_cartisian.colors==2] = 'g'
        event_cartisian.colors[event_cartisian.colors==3] = 'c'
        event_cartisian.colors[event_cartisian.colors==12] = 'm'

        event_cartisian = event_cartisian[event_cartisian.E > 0]

        eta = pd.read_csv(path+"data/truth_angles/"+filename+"_eta.csv", header=None, usecols=[0, 1, 2, 3])
        phi = pd.read_csv(path+"data/truth_angles/"+filename+"_phi.csv", header=None, usecols=[0, 1, 2, 3])
        r = pd.read_csv(path+"data/truth_angles/"+filename+"_r.csv", header=None, usecols=[0, 1, 2, 3])

        event_r = np.linalg.norm(event_cartisian.loc[:,['x','y']], axis=1)
        event_phi = np.arctan2(event_cartisian.loc[:,'y'], event_cartisian.loc[:,'x'])
        event_eta = np.arcsinh(event_cartisian.loc[:,'z']/event_r)

        event_delta_phi = event_phi - phi.iloc[event, 0]
        event_delta_eta = event_eta - eta.iloc[event, 0]

        events_r.extend(event_r)
        events_E.extend(event_cartisian.E)

events_r = np.array(events_r)
events_E = np.array(events_E)

plt.hist(events_r, weights=events_E, bins=500, histtype=u'step')
plt.show()