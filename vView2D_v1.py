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

Description1 = "This function is vView_v0(file, Tracer, Auxiallaryfield, bool vector)"
Description2 = "file is compulsory. Default Auxiallaryfield is tracer f"
Description3 = "bool vector decides between vector field or streamplot\n"

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
scaleQ=50.0
widthQ=0.0075
print(Description1)
print(Description2)
print(Description3)
if (len(sys.argv) == 1):
    print("Please enter the location of gfs file!")
    sys.exit(1)
else:
    place = sys.argv[1]
    if (len(sys.argv) == 2):
        print('Making f as default VOF tracer')
        fieldName1 = 'f'
        print('Making f as default tracer')
        fieldName2 = 'f'
        print("streamplot it is!")
        vector = False
    else:
        fieldName1 = sys.argv[2]
        if (len(sys.argv) == 3):
            print('Making f as default tracer')
            fieldName2 = 'f'
            print("streamplot it is!")
            vector = False
        else:
            fieldName2 = sys.argv[3]
            if (len(sys.argv) == 4):
                print("streamplot it is!")
                vector = False
            else:
                vectors = sys.argv[4]
if not os.path.exists(place):
    print("File not found!\n")
    sys.exit(1)
R = 1.0
Ldomain = 20*R
xmin = -0.495*Ldomain
xmax = 0.495*Ldomain
ymin = -0.495*Ldomain
ymax = 0.495*Ldomain
nx = 512
ny = 512
nd = 16
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
field = gettingfield(fieldName1)
U = gettingfield('u_x')
V = gettingfield('u_y')
Theta = gettingfield(fieldName2)
xp = -y/Ldomain
yp = x/Ldomain
Xp = -Y.transpose()/Ldomain
Yp = X.transpose()/Ldomain
Up = -V.transpose()
Vp = U.transpose()
fp = field.transpose()
Thetap = Theta.transpose()
plt.close()
fig, ax = plt.subplots()
fig.set_size_inches(28.80, 18.00)
rc('axes', linewidth=2)
ax.contour(Xp, Yp, fp, levels=0.5, colors='black')
ax.pcolormesh(Xp, Yp, Thetap, alpha=0.80, cmap='jet', edgecolors='face')
speed = np.sqrt(Up**2 + Vp**2)
for row in range(len(speed)):
    for col in range(len(speed[0])):
        if (abs(speed[row,col]) > 0):
            Up[row,col] /= speed[row,col]
            Vp[row,col] /= speed[row,col]
if (vectors):
    ax.quiver(xp[::nd], yp[::nd], Up[::nd,::nd], Vp[::nd,::nd], color='white', scale_units="xy", scale=scaleQ, width=widthQ, pivot="mid")
else:
    ax.streamplot(xp, yp, Up, Vp, density = 5, color='gray', linewidth=1, cmap='Greys')
ax.set_xlabel(r'$X/L_0$', fontsize=30)
ax.set_ylabel(r'$Y/L_0$', fontsize=30)
ax.xaxis.set_tick_params(labelsize=30)
ax.yaxis.set_tick_params(labelsize=30)
ax.set_xlim(x.min()/Ldomain, x.max()/Ldomain)
ax.set_ylim(y.min()/Ldomain, y.max()/Ldomain)
ax.grid(False)
ax.set_aspect('equal')
ax.set_title(r'file: %s' % (place), fontsize=30)
plt.show()
plt.close()
