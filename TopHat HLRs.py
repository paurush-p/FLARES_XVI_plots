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
import pandas as pd

def multiprocessing_func(x):
    ident=x[0]
    filename=x[1]
    file_name_fits=x[2]
    amount_of_layers=0
    extracted_wav=[]
    with open(filename) as f:
        lines_after_2 = f.readlines()[2:]
        column1 = [x.split() for x in lines_after_2]
        extracted = [float(y[0]) for y in column1]
        amount_of_layers= len(extracted)
        extracted_wav.append(extracted)
    image_data = fits.getdata(file_name_fits, ext=0)
    loopcontrol=0
    image=image_data[6]+image_data[7]+image_data[8]
    center=(199.5,199.5)
    r=[0]
    sum_r=[0]
    sum=0
    sumhf=0
    radius=1
    k=math.ceil(center[0])
    l=math.ceil(center[1])
    size_x=0
    size_y=0
    for x2 in image:
    	size_x+=1
    	for y2 in x2:
    		size_y+=1
    		sum+=y2
    while sumhf<(0.75*sum) :
    	sumhf=0
    	m=max(0,k-radius)
    	while m<min(k+radius+1,size_x):
    		n=max(0,l-radius)
    		while n<min(l+radius+1,size_y):
    			current_point=(m,n)
    			if(abs(math.dist(current_point,center))<=radius) :
    				sumhf+=image[m][n]
    			n+=1
    		m+=1
    	sum_r.append(sumhf)
    	r.append(radius)
    	radius+=1
    	hlr1500=numpy.interp((sum/2),sum_r,r)
    
    rarr=[ident,str(hlr1500)]
    
    return rarr
    
if __name__ == '__main__':
    starttime = time.time()
    path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
    save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
    ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
    #ini_fold=["z_10"]
    names=[]
    sendtotal=[]
    results=[]
    hlrtophat=[]
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
                filename=path+edited+"/flares_cube_UV_sed.dat"
                fitsfile=path+edited+"/flares_cube_UV_total.fits"
                abc=[idn,filename,fitsfile]
                sendtotal.append(abc)
    pool = multiprocessing.Pool()
    results.append(pool.map(multiprocessing_func,sendtotal))
    for x in results[0]:
    	hlrtophat.append(float(x[1]))
    print(hlrtophat)
    numpy.savetxt("/home/projects/dtu_00026/people/paupun/"+"TopHat.txt",hlrtophat)
    print('That took {} seconds'.format(time.time() - starttime))

