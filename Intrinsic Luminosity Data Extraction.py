import os
import matplotlib.pyplot as plt
import numpy
import time
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
from scipy import interpolate
import scipy
import math
import h5py
import pandas as pd
f = h5py.File("/home/projects/dtu_00026/people/aswvij/FLARES_data/flares.hdf5",'r')
df=pd.read_csv("dust_continuum/output/table1.csv")
IDS=numpy.array(df["ID"])
intlum=[]
t=0
for x in IDS:
	idtag=x[:-18]
	z=int(idtag[2:])
	zfl="{0:03}".format(15-z)+"_z"+"{0:03}".format(z)+"p000"
	rgtag=(x[:-8])[-2:]
	acname=rgtag+"/"+zfl+"/Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/Intrinsic/FUV"
	data=f[acname]
	alllum=numpy.array(data)
	gal=int(x[-3:])
	lum=alllum[gal]
	intlum.append(lum)
	t+=1
	print("Galaxies Done: ",t)
numpy.savetxt("intrinsiclum.txt",numpy.array(intlum))
print("Done")
