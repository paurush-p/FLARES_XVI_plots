import os
import matplotlib.pyplot as plt
import numpy
import time
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
from scipy import interpolate
import math
import h5py
import numpy as np
import pandas as pd
path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
start=time.time()
t=0
ids=[]
zs=[]
bm=[]
for x in ini_fold :
    current=path+"/"+x
    regions=[]
    dir_list = os.listdir(current)
    regions=dir_list
    regions=[f for f in regions if os.path.isdir(current+'/'+f)]
    for y in regions :
        latest=current+"/"+y
        galaxies = os.listdir(latest)
        galaxies=[f for f in galaxies if os.path.isdir(latest+'/'+f)]
        for z in galaxies:
            final=latest+"/"+z
            edited="/"+x+"/"+y+"/"+z
            idn=x+"/"+y+"/"+z
            ids.append(idn)
            redshift=x[2:]
            #print(redshift)
            ######### Your are in the folder where the SKIRT files are
            regionnumber=y[7:]
            file_hdf5="/home/projects/dtu_00026/people/paupun/flares_skirt_outputs.hdf5"
            h=h5py.File(file_hdf5)
            special=15-int(redshift)
            redshiftcode=f"{special:03}"+"_z"+f"{int(redshift):03}"+"p000"
            #print(regionnumber+"/"+redshiftcode+"/Galaxy/Mstar")
            data=h[regionnumber+"/"+redshiftcode+"/Galaxy/Index"]
            index_arr=numpy.array(data)
            galaxynum=int(z[4:])
            ind=index_arr[galaxynum]
            #print(ind,y)
            fname = "/home/projects/dtu_00026/people/aswvij/FLARES_data/flares.hdf5"
            with h5py.File(fname, 'r') as hf:
                #print(list(hf[regionnumber+'/'+redshiftcode+'/Galaxy/Mgas_aperture'].keys()))
                #print(list(hf[regionnumber+'/'+redshiftcode+'/Particle'].keys()))
                BH_Mass = np.array(hf[regionnumber+'/'+redshiftcode+'/Galaxy/Mgas_aperture'].get('30'), dtype = np.float64)
                bm.append(BH_Mass[ind])
            t+=1
            print("Galaxies Done :",t,BH_Mass[ind])
df=pd.DataFrame({'ID':ids,'Gass Mass':bm})
print(df)
df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/GassMass.csv")
print("Done in :",round((time.time()-start)/60,2),"Min")


