import os
import matplotlib.pyplot as plt
import numpy
import time
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
import pandas as pd
import math
path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
#ini_fold=["z_10"]
start=time.time()
t=0
mxs=[]
mns=[]
meds=[]
ids=[]
zs=[]
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
            redshift=x[2:]
            ######### Your are in the folder where the SKIRT files are
            file_name_fits=final+"/flares_cube_UV_total.fits"
            image_data = fits.getdata(file_name_fits, ext=0)
            image=image_data[7]
            image=numpy.reshape(image,(len(image)**2,))
            mx=numpy.max(image)
            mn=numpy.min(image)
            med=numpy.mean(image)
            ids.append(idn)
            zs.append(redshift)
            mxs.append(mx)
            mns.append(mn)
            meds.append(med)
            t+=1
            print("Galaxies done :",t)
mxmn=pd.DataFrame({'ID':ids,'Redshift':zs, 'Max Pixel':mxs, 'Min Pixel': mns, 'Mean Pixel':meds})
print(mxmn)
mxmn.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/imagedata.csv")
print("Done.Total execute time :", round((time.time()-start)/60.0,2))
