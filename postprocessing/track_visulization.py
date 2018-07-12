import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

filename = "NTUP_FCS.13289379._000001.pool.root.1"
path="/media/anandan/3474068674064B56/CERN/Program/atlas_sim_gan/"

def get_one_event(layer=1, requireEnergy = False):

    x, y, z, E = [], [], [], []

    with open(path +"data/layer_wise/"+filename+"_Layer_"+str(layer)+".csv", 'r') as f:
        for i,event in enumerate(f):
            event = event.split(';')

            for hit in event[:-1]:
                hit = hit.split(',')

                x.append(float(hit[0]))
                y.append(float(hit[1]))
                z.append(float(hit[2]))

                if requireEnergy:
                    E.append(float(hit[4]))

            if i == 0:
                break

    return np.array(x), np.array(y), np.array(z), np.array(E)

def get_all_events(layer=1, requireEnergy = False):

    x, y, z, E = [], [], [], []

    with open(path +"data/layer_wise/"+filename+"_Layer_"+str(layer)+".csv", 'r') as f:
        for i,event in enumerate(f):

            if event != '\n':

                event = event.split(';')

                hit = np.random.choice(event[:-1])
                hit = hit.split(',')

                x.append(float(hit[0]))
                y.append(float(hit[1]))
                z.append(float(hit[2]))

                if requireEnergy:
                    E.append(float(hit[4]))

            if i == 500:
                break

#    x, y, z = convert_to_cylindrical(np.array(x), np.array(y), np.array(z))

    return x, y, z, E

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#x, y, z, _ = get_one_event(layer=0)
#ax.scatter(x, y, z, s=1, c='r', marker='.', label='Layer0')

x, y, z, _ = get_one_event(layer=1)
ax.scatter(x, y, z, s=1, c='g', marker='o', label='Layer1')

#x, y, z, _ = get_one_event(layer=2)
#ax.scatter(x, y, z, s=1, c='b', marker='.', label='Layer2')
#
#x, y, z, _ = get_one_event(layer=3)
#ax.scatter(x, y, z, s=1, c='k', marker='.', label='Layer3')
#
#x, y, z, _ = get_one_event(layer=12)
#ax.scatter(x, y, z, s=1, c='c', marker='.', label='Layer12')

eta = pd.read_csv("../data/"+filename+"_eta.csv", header=None, usecols=[0, 1, 2, 3])
phi = pd.read_csv("../data/"+filename+"_phi.csv", header=None, usecols=[0, 1, 2, 3])
r = pd.read_csv("../data/"+filename+"_r.csv", header=None, usecols=[0, 1, 2, 3])

X = r*phi.apply(np.cos)
Y = r*phi.apply(np.sin)
Z = r*eta.apply(np.sinh)

ax.plot(X.iloc[0,:], Y.iloc[0,:], Z.iloc[0,:])
#ax.plot(X.iloc[1,:], Y.iloc[1,:], Z.iloc[1,:])
#ax.plot(X.iloc[2,:], Y.iloc[2,:], Z.iloc[2,:])

ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

ax.set_xlim([1350,1800])
ax.set_ylim([-800,-400])
ax.set_zlim([300,600])

ax.legend()
plt.show()














