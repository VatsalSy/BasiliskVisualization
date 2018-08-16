# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids

import numpy as np
import os
import subprocess as sp
import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib
from matplotlib.collections import LineCollection

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
matplotlib.rcParams['text.latex.unicode'] = True

Description = 'This function is vView_v0(file, field)\nIt takes plots a pcolormesh for the given field!'

def gettingfield(fieldstr):
    print('Getting %s' % fieldstr)
    exe = "gfs2oogl2D -p %s -c %s < %s" % (gridfile,fieldstr, place)
    temp1 = sp.check_output(exe, shell=True)
    temp2 = temp1.decode("utf-8")
    temp3 = temp2.split("\n")
    fieldtemp = []
    for n1 in range(0, len(temp3) - 1):
        temp4 = temp3[n1].split(" ")
        fieldtemp.append(float(temp4[3]))
    field = np.asarray(fieldtemp)
    field.resize((ny, nx))
    return field

# ----------------------------------------------------------------------------------------------------------------------
## User Inputs
print(Description)
if (len(sys.argv) < 2):
    print("Please enter the location of gfs file!")
    sys.exit(1)
place = sys.argv[1]
if not os.path.exists(place):
    print("File not found!")
    sys.exit(1)
if (len(sys.argv) == 3):
    fieldName = sys.argv[2]
else:
    print('Taking default field as f')
    fieldName = 'f'
R = 1.0
Ldomain = 20*R
xmin = -0.495*Ldomain
xmax = 0.495*Ldomain
ymin = -0.495*Ldomain
ymax = 0.495*Ldomain
nx = 512
ny = 512
print('saving the grid')
x = np.linspace(xmin, xmax, num=nx)
y = np.linspace(ymin, ymax, num=ny)
gridfile = 'cartgrid.dat'
fg = open(gridfile, 'w+')
for i in range(ny):
 for j in range(nx):
     fg.write("%f %f %f\n" % (x[j], y[i], 0))
fg.close()
X, Y = np.meshgrid(x,y,indexing='xy')

field = gettingfield(fieldName)

Xp = -Y.transpose()/Ldomain
Yp = X.transpose()/Ldomain
fp = field.transpose()
fig, ax = plt.subplots()
fig.set_size_inches(28.80, 18.00)
rc('axes', linewidth=2)
ax.pcolormesh(Xp, Yp, fp, alpha=0.80, cmap='jet', edgecolors='face')
ax.set_xlabel(r'$X/L_0$', fontsize=30)
ax.set_ylabel(r'$Y/L_0$', fontsize=30)
ax.xaxis.set_tick_params(labelsize=30)
ax.yaxis.set_tick_params(labelsize=30)
ax.set_xlim(x.min()/Ldomain, x.max()/Ldomain)
ax.set_ylim(y.min()/Ldomain, y.max()/Ldomain)
ax.grid(False)
ax.set_aspect('equal')
ax.set_title(r'file: %s and field: %s' % (place, fieldName), fontsize=30)
plt.show()
plt.close()
