import os
import time
import multiprocessing 
import numpy as np
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
    size1=int(x[3])
    image1=(fits.getdata(x[1], ext=0)[38])
    imarr=Image.fromarray(image1)
    image=np.array(imarr.resize((size1,size1)))
    clearimage=image
    psf1=fits.getdata(x[2], ext=0)
    newpsf=Image.fromarray(psf1)
    psfsizeby2=1288/2
    sby2=size1/2
    box = (psfsizeby2-sby2,psfsizeby2-sby2,psfsizeby2+sby2,psfsizeby2+sby2)
    #newpsf1 = newpsf.crop(box)
    #psf=np.array(newpsf1.resize((size1-1,size1-1)))
    kernel=Gaussian2DKernel(2)
    kernel.normalize()
    psf=kernel.array

    image = convolve(image, psf)

    np.random.seed(3)
    gain = 1e4
    image = np.random.poisson(image * gain) / gain

    snp = 5.0
    sky_sigma = 1.0 / snp
    image += sky_sigma * np.random.standard_normal(size=(size1, size1))

    threshold = detect_threshold(image, 1.5)
    npixels = 5  # minimum number of connected pixels
    convolved_image = convolve(image, psf)
    segmap = detect_sources(convolved_image, threshold, npixels)
    #plt.imshow(segmap, origin='lower', cmap='gray')
    rarr=[ident,"","","",""]
    try:
    	source_morphs = statmorph.source_morphology(image, segmap, gain=gain, psf=psf)
    	maxnum=0
    	maxsize=0
    	mindist=504
    	for numobj,objs in enumerate(source_morphs) :
        	if abs(math.dist((sby2-0.5,sby2-0.5),(objs.xc_asymmetry,objs.yc_asymmetry)))<mindist :
            		mindist=abs(math.dist((sby2-0.5,sby2-0.5),(objs.xc_asymmetry,objs.yc_asymmetry)))
            		maxnum=numobj
    	morph = source_morphs[maxnum]
    	rarr=[ident,str(morph.xc_asymmetry),str(morph.yc_asymmetry),str((morph.rhalf_circ)*(60/size1)),str((morph.rhalf_ellip)*(60/size1))]
    except:
    	pass
    return rarr
    
if __name__ == '__main__':
    starttime = time.time()
    path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
    save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
    #ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
    ini_fold=["z_5"]
    rerez=[400,400,400,400,400,400]
    psfnamelist=["nircampsf090.fits","nircampsf115.fits","nircampsf115.fits","nircampsf140.fits","nircampsf150.fits","nircampsf162.fits"]
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
                filename=path+edited+"/flares_cube_dust_total.fits"
                psffile="/home/projects/dtu_00026/people/paupun/PSF/"+ psfnamelist[zint-5]
                abc=[idn,filename,psffile,str(rerez[zint-5])]
                sendtotal.append(abc)
    pool = multiprocessing.Pool()
    #print(pool.map(multiprocessing_func,sendtotal))
    results.append(pool.map(multiprocessing_func,sendtotal))
    ids=[]
    cenx=[]
    ceny=[]
    rcirc=[]
    rellip=[]
    for tortilla in results[0]:
    	ids.append(tortilla[0])
    	cenx.append(tortilla[1])
    	ceny.append(tortilla[2])
    	rcirc.append(tortilla[3])
    	rellip.append(tortilla[4])
    df=pd.DataFrame({'ID':ids,'Center x':cenx,'Center y':ceny,'HLR circ':rcirc,"HLR ellip":rellip})
    pool.close()
    df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/IRStatMorphResults50umZ5.csv")
    print('That took {} seconds'.format(time.time() - starttime))
