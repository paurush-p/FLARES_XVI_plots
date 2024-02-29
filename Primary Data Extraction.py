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
            file_hlr=save_path+edited+"/Half_light_R_scipy_uv.txt"
            file_hlr_dust=save_path+edited+"/Half_light_R_scipy_dust.txt"
            file_sed_uv=final+"/flares_cube_UV_sed.dat"
            file_sed_dust=final+"/flares_cube_dust_sed.dat"
            h=h5py.File(file_hdf5)
            hlr_arr_uv=numpy.loadtxt(file_hlr)
            hlr_arr_dust=numpy.loadtxt(file_hlr_dust)
            hlr_1500uv=numpy.interp(0.15,[0.1498307077,0.1587401052],[hlr_arr_uv[7],hlr_arr_uv[8]])
            hlr_50um=numpy.interp(50,[48.61649310,51.04633161],[hlr_arr_dust[37],hlr_arr_dust[38]])
            hlr_250um=numpy.interp(250,[243.0824655,255.2316581e+02 ],[hlr_arr_dust[70],hlr_arr_dust[71]])
            lum_arr_uv=numpy.loadtxt(file_sed_uv,usecols=1)
            lum_arr_dust=numpy.loadtxt(file_sed_dust,usecols=1)
            lum_1500uv=(numpy.interp(0.15,[0.1498307077,0.1587401052],[lum_arr_uv[7],lum_arr_uv[8]]))*4*math.pi*1*1*(10**12)*3.0856*(10**18)*3.0856*(10**18)*(10**-23) ###in egs/sec/Hz
            lum_50um=(numpy.interp(50,[48.61649310,51.04633161],[lum_arr_dust[37],lum_arr_dust[38]]))*4*math.pi*1*1*(10**12)*3.0856*(10**18)*3.0856*(10**18)*(10**-23)
            lum_250um=(numpy.interp(250,[243.0824655,255.2316581e+02 ],[lum_arr_dust[70],lum_arr_dust[71]]))*4*math.pi*1*1*(10**12)*3.0856*(10**18)*3.0856*(10**18)*(10**-23)
            regionnumber=y[7:]
            #print(regionnumber)
            special=15-int(redshift)
            redshiftcode=f"{special:03}"+"_z"+f"{int(redshift):03}"+"p000"
            #print(regionnumber+"/"+redshiftcode+"/Galaxy/Mstar")
            data=h[regionnumber+"/"+redshiftcode+"/Galaxy/Mstar"]
            data1=h[regionnumber+"/"+redshiftcode+"/Galaxy/SFR"]
            mass_arr=numpy.array(data)
            SFR_arr=numpy.array(data1)
            galaxynum=int(z[4:])
            SFR=SFR_arr[galaxynum]
            Mstellar=mass_arr[galaxynum]
            ids.append(idn)
            zs.append(redshift)
            ms.append(Mstellar)
            sfrs.append(SFR)
            lumuv.append(lum_1500uv)
            lumir1.append(lum_50um)
            lumir2.append(lum_250um)
            hlruv.append(hlr_1500uv)
            hlrir1.append(hlr_50um)
            hlrir2.append(hlr_250um)
            t+=1
            print("Galaxies Done :",t)
#bigarr=[ids,zs,ms,sfrs,lumuv,lumir1,lumir2,hlruv,hlrir1,hlrir2]
#table_data=numpy.array(bigarr)
#numpy.savetxt("/home/projects/dtu_00026/people/paupun/table.txt",table_data)
df=pd.DataFrame({'ID':ids,'Redshift':zs,'Stellar Mass':ms,'Star Formation Rate':sfrs,'UV Luminosity 1500A':lumuv,'Luminosity 50um IR':lumir1,'Luminosity 250um IR':lumir2,'UV HLR 1500A':hlruv,'HLR 50um IR':hlrir1,'HLR 250um IR':hlrir2})
df['Mass_bin'] = pd.cut(df['Stellar Mass'], [0, 0.1, 0.31622776601683794,1,3.162277660168379,10,31.622776601683796,100],labels=['0-10^9', '10^9-10^9.5', '10^9.5-10^10','10^10-10^10.5','10^10.5-10^11','10^11-10^11.5','10^11.5-10^12'])
print(df)
df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/table1.csv")
print("Done in :",round((time.time()-start)/60,2),"Min")


