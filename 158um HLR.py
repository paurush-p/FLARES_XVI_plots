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
    #print(x[0])
    ident=x[0][57:-10]
    size1=int(x[1])
    image=fits.getdata(x[0], ext=0)[0][0]
    center=(199.5,199.5)
    std=np.std(image)
    for i,x1 in enumerate(image):
        for j,y1 in enumerate(x1):
            if y1<(5*std):
                image[i][j]=0

    r=[0]
    sum_r=[0]
    sum=0
    radius=1
    sumhf=0
    k=math.ceil(center[0])
    l=math.ceil(center[1])
    size_x=0
    size_y=0
    for x2 in image:
        size_x+=1
        for y2 in x2:
            size_y+=1
            sum+=y2
    while sumhf<(0.6*sum) :
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
    nr=numpy.array(r)
    nsum_r=numpy.array(sum_r)
    numpy_interpolated_radius=numpy.interp((sum/2),nsum_r,nr)
    rarr=[ident,str(numpy_interpolated_radius)]
    #print(nr,nsum_r,rarr)
    print(rarr)
    return rarr
    
if __name__ == '__main__':
    start=time.time()
    sendtotal=[]
    results=[]
    for x in os.listdir("/home/projects/dtu_00026/people/paupun/cleanedalmaimages") :
                filename="/home/projects/dtu_00026/people/paupun/cleanedalmaimages/"+x
                abc=[filename,str(400)]
                sendtotal.append(abc)
    pool = multiprocessing.Pool()
    print(sendtotal)
    results.append(pool.map(multiprocessing_func,sendtotal))
    ids=[]
    rad=[]
    for tortilla in results[0]:
        ids.append(tortilla[0])
        rad.append(tortilla[1])
    df=pd.DataFrame({'ID':ids,'HLR':rad})
    print(df)
    df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/AlmaTrad.csv")
    print('That took {} seconds'.format(time.time() - start))