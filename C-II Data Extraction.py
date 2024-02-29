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
start=time.time()
t=0
ids=[]
zs=[]
lum156um=[]
hlr156um=[]
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
            #print(redshift)
            ######### Your are in the folder where the SKIRT files are
            file_hlr=save_path+edited+"/Half_light_R_scipy_uv.txt"
            file_hlr_dust=save_path+edited+"/Half_light_R_scipy_dust.txt"
            file_sed_uv=final+"/flares_cube_UV_sed.dat"
            file_sed_dust=final+"/flares_cube_dust_sed.dat"

            
            hlr_arr_uv=numpy.loadtxt(file_hlr)
            lum_arr_uv=numpy.loadtxt(file_sed_uv,usecols=1)
            hlr_arr_dust=numpy.loadtxt(file_hlr_dust)
            lum_arr_dust=numpy.loadtxt(file_sed_dust,usecols=1)
            
            
            hlr156umi=hlr_arr_dust[61]
            
            lum156umi=lum_arr_dust[61]*4*math.pi*1*1*(10**12)*3.0856*(10**18)*3.0856*(10**18)*(10**-23)
            
            special=15-int(redshift)
            redshiftcode=f"{special:03}"+"_z"+f"{int(redshift):03}"+"p000"
            
            ids.append(idn)
            zs.append(redshift)
            
         
            hlr156um.append(hlr156umi)
            lum156um.append(lum156umi)
            t+=1
            print("Galaxies Done :",t)
df=pd.DataFrame({'ID':ids,'Redshift':zs,'Lum 156um':lum156um,'HLR 156um':hlr156um})
print(df)
df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/almacomparision.csv")
print("Done in :",round((time.time()-start)/60,2),"Min")


