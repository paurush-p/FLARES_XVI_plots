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
import pandas as pd
path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
#ini_fold=["z_10"]
start=time.time()
t=0
ms=[]
lumuv=[]
sfrs=[]
hlruv=[]
hlrir1=[]
hlrir2=[]
ids=[]
zs=[]
lumir1=[]
lumir2=[]
obshlrs=[]
obshlrsuv=[]
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
            file_hdf5="/home/projects/dtu_00026/people/paupun/flares_skirt_outputs.hdf5"
            file_hlr_dust=save_path+edited+"/Half_light_R_scipy_dust.txt"
            file_sed_dust=final+"/flares_cube_dust_sed.dat"
            file_hlr_uv=save_path+edited+"/Half_light_R_scipy_uv.txt"
            file_sed_uv=final+"/flares_cube_UV_sed.dat"
            h=h5py.File(file_hdf5)
            hlr_arr_dust=numpy.loadtxt(file_hlr_dust)
            hlr_arr_uv=numpy.loadtxt(file_hlr_uv)
            regionnumber=y[7:]
            #print(regionnumber)
            redshiftint=int(redshift)
            restwav=850.0/(redshiftint+1)
            restwavuv=1.6/(redshiftint+1)
            wavs_arr=numpy.loadtxt(file_sed_dust,usecols=0)
            wavs_arr_uv=numpy.loadtxt(file_sed_uv,usecols=0)
            hlr_obs_850um=numpy.interp(restwav,wavs_arr,hlr_arr_dust)
            hlr_obs_uv=numpy.interp(restwavuv,wavs_arr_uv,hlr_arr_uv)
            special=15-redshiftint
            redshiftcode=f"{special:03}"+"_z"+f"{int(redshift):03}"+"p000"
            #print(regionnumber+"/"+redshiftcode+"/Galaxy/Mstar")
            data=h[regionnumber+"/"+redshiftcode+"/Galaxy/Mstar"]
            data1=h[regionnumber+"/"+redshiftcode+"/Galaxy/DTM"]
            mass_arr=numpy.array(data)
            SFR_arr=numpy.array(data1)
            galaxynum=int(z[4:])
            SFR=SFR_arr[galaxynum]
            Mstellar=mass_arr[galaxynum]
            ids.append(idn)
            zs.append(redshift)
            ms.append(Mstellar)
            sfrs.append(SFR)
            obshlrs.append(hlr_obs_850um)
            obshlrsuv.append(hlr_obs_uv)
            t+=1
            print("Galaxies Done :",t)
#bigarr=[ids,zs,ms,sfrs,lumuv,lumir1,lumir2,hlruv,hlrir1,hlrir2]
#table_data=numpy.array(bigarr)
#numpy.savetxt("/home/projects/dtu_00026/people/paupun/table.txt",table_data)
df=pd.DataFrame({'ID':ids,'Redshift':zs,'Stellar Mass':ms,'DTM':sfrs,"850um observed HLR":obshlrs,"1.6um observed HLR":obshlrsuv})
df['Mass_bin'] = pd.cut(df['Stellar Mass'], [0, 0.1, 0.31622776601683794,1,3.162277660168379,10,31.622776601683796,100],labels=['0-10^9', '10^9-10^9.5', '10^9.5-10^10','10^10-10^10.5','10^10.5-10^11','10^11-10^11.5','10^11.5-10^12'])
print(df)
df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/ObservedSizeRatio.csv")
print("Done in :",round((time.time()-start)/60,2),"Min")

