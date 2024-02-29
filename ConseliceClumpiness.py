import os
import time
import multiprocessing 
import numpy as np
import numpy
import matplotlib.pyplot as plt
from astropy.visualization import simple_norm
from astropy.modeling.models import Sersic2D
from astropy.convolution import convolve, Gaussian2DKernel
from photutils.segmentation import detect_threshold, detect_sources
import statmorph
from astropy.io import fits
from scipy import interpolate
import cv2
from PIL import Image
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import scipy.ndimage as ndimage
import pandas as pd

def multiprocessing_func(x):
    ident=x[0]
    hlr=float(x[2])
    #sigma=math.ceil(hlr*0.3)
    sigma=math.ceil(60)
    image=fits.getdata(x[1], ext=0)[7]
    blur = ndimage.uniform_filter(image, size=sigma)
    image2=image-blur
    sval=10*numpy.sum(image2)/numpy.sum(image)
    rarr=[ident,str(sval)]
    return rarr
    
if __name__ == '__main__':
    starttime = time.time()
    path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
    save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
    #ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
    ini_fold=["z_10"]
    names=[]
    sendtotal=[]
    results=[]
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
                zint=int(redshift)
                ######### Your are in the folder where the SKIRT files
                file_hlr=save_path+edited+"/Half_light_R_scipy_uv.txt"
                hlr_arr_uv=numpy.loadtxt(file_hlr)
                hlr=hlr_arr_uv[7]
                filename=path+edited+"/flares_cube_UV_total.fits"
                abc=[idn,filename,str(hlr)]
                sendtotal.append(abc)
    pool = multiprocessing.Pool()
    #print(sendtotal)
    #print(pool.map(multiprocessing_func,sendtotal))
    results.append(pool.map(multiprocessing_func,sendtotal))
    ids=[]
    svalues=[]
    for tortilla in results[0]:
        ids.append(tortilla[0])
        svalues.append(tortilla[1])
    df=pd.DataFrame({'ID':ids,'S':svalues})
    print(df)
    df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/Clumpiness.csv")
    print('That took {} seconds'.format(time.time() - starttime))
