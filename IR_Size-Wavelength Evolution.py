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

plt.rcParams.update({'font.size': 15})
plt.tick_params(axis="y",direction="in")
plt.tick_params(axis="x",direction="in")
paint=["blue","orange","green","red","purple","brown"]

path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
#ini_fold=["z_10"]
start=time.time()
t=0
rr=0
for x in ini_fold :
    current=path+"/"+x
    regions=[]
    dir_list = os.listdir(current)
    regions=dir_list
    regions=[f for f in regions if os.path.isdir(current+'/'+f)]
    redshiftratios=[]
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
            file_hlr_dust=save_path+edited+"/Half_light_R_scipy_dust.txt"
            file_sed_dust=final+"/flares_cube_dust_sed.dat"
            hlr_arr_dust=numpy.loadtxt(file_hlr_dust)
            regionnumber=y[7:]
            #print(regionnumber)
            redshiftint=int(redshift)
            #restwav=850.0/(redshiftint+1)
            restwav=500.0
            wavs_arr=numpy.loadtxt(file_sed_dust,usecols=0)
            wavlooptest=0
            while (wavs_arr[wavlooptest]<restwav):
                wavlooptest+=1
            hlr_obs_850um=numpy.interp(restwav,[wavs_arr[wavlooptest-1],wavs_arr[wavlooptest] ],[hlr_arr_dust[wavlooptest-1],hlr_arr_dust[wavlooptest]])
            hlr_ratios=[each/hlr_obs_850um for each in hlr_arr_dust]
            #obs_wav=[each*(redshiftint+1) for each in wavs_arr]
            #obs_wav=[each*(redshiftint+1) for each in wavs_arr]
            #combined=[obs_wav,hlr_ratios]
            redshiftratios.append(hlr_ratios)
            t+=1
            #print("Galaxies Done :",t)
    avg=[]
    y16=[]
    y84=[]
    for a in hlr_ratios:
        avg.append(0)
        y16.append(0)
        y84.append(0)
    lc=0
    while lc<len(avg):
        currarr=[]
        for numgal,g in enumerate(redshiftratios):
            currarr.append(g[lc])
        avg[lc]=numpy.median(currarr)
        y16[lc]=numpy.percentile(currarr,16)
        y84[lc]=numpy.percentile(currarr,84)
        lc+=1
    #print(avg)
    print("")
    print(y16)
    print(y84)
    print("")
    plt.plot(wavs_arr,avg,label="z="+redshift,color=paint[rr])
    plt.fill_between(wavs_arr, y16, y84,color=paint[rr],alpha = 0.1)
    rr+=1
plt.xlim(350,850)
plt.ylim(0.75,1.25)
plt.ylabel("$\mathdefault{R_{\u03bb}}$/$\mathdefault{R_{500um}}$")
plt.xlabel("$\u03bb$(um)")
plt.legend(loc="lower right",fontsize=11)
plt.yticks(fontsize=11)
plt.xticks(fontsize=11)
plt.grid(axis='both')
#plt.show()
plt.savefig("/home/projects/dtu_00026/people/paupun/sizewavevol.png")
print("Done in :",round((time.time()-start)/60,2),"Min")
