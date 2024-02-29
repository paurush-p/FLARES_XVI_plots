import os
import matplotlib.pyplot as plt
import numpy
import time
from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
from scipy import interpolate
import math
import pandas as pd


path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
#ini_fold=["z_10"]
start=time.time()
t=0
rs=[]
skr=[]
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
            ######### Your are in the folder where the SKIRT files are
            idn=x+"/"+y+"/"+z
            redshift=x[2:]
            #print(redshift)
            ######### Your are in the folder where the SKIRT files are
            file_hdf5="/home/projects/dtu_00026/people/paupun/flares_skirt_outputs.hdf5"
            file_hlr=save_path+edited+"/Half_light_R_scipy_uv.txt"
            hlr_arr_uv=numpy.loadtxt(file_hlr)

            hlr_1500uv=hlr_arr_uv[7]


            file_name_fits=final+"/flares_cube_UV_total.fits"
            image_data = fits.getdata(file_name_fits, ext=0)
            image=image_data[7]
            image=image.reshape((1,-1))
            image=image[0]
            image=numpy.sort(image)
            image=image[::-1]
            totallum=numpy.sum(image)
            currsum=0
            i=0
            lights=[]
            rad=[]
            while currsum<(0.75*totallum):
            	currsum=image[i]+currsum
            	lights.append(currsum)
            	r=((i+1)/math.pi)**0.5
            	rad.append(r)
            	i=i+1;
            radius1=numpy.interp((0.5*totallum),lights,rad)
            image=image_data[7]
            image=image.reshape((1,-1))
            image=image[0]
            image=numpy.sort(image)
            image=image[::-1]
            totallum=numpy.sum(image)
            currsum=0
            i=0
            lights=[]
            rad=[]
            while currsum<(0.75*totallum):
            	currsum=image[i]+currsum
            	lights.append(currsum)
            	r=((i+1)/math.pi)**0.5
            	rad.append(r)
            	i=i+1;
            radius=numpy.interp((0.5*totallum),lights,rad)
            rs.append(radius)
            skr.append(hlr_1500uv)
            t+=1
            print("Galaxies done :",t)
df=pd.DataFrame({'Roper Radius':rs,'SKIRT Radius':skr})
print(df)
df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/RoperRadius.csv")
print("Done.Total execute time :", round((time.time()-start)/60.0,2))
