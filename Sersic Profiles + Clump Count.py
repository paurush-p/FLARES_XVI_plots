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
from photutils.segmentation import SourceFinder
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
    image1=(fits.getdata(x[1], ext=0)[7])
    imarr=Image.fromarray(image1)
    image=np.array(imarr.resize((size1,size1)))
    clearimage=image
    psf1=fits.getdata(x[2], ext=0)
    newpsf=Image.fromarray(psf1)
    psfsizeby2=1288/2
    sby2=math.ceil(size1/2)
    box = (psfsizeby2-sby2,psfsizeby2-sby2,psfsizeby2+sby2,psfsizeby2+sby2)
    newpsf1 = newpsf.crop(box)
    if ((size1%2)==0) :
        psf=np.array(newpsf1.resize((size1-1,size1-1)))
    else :
        psf=np.array(newpsf1.resize((size1,size1)))

    image = convolve(image, psf)

    np.random.seed(3)
    gain = 1e5
    image = np.random.poisson(image * gain) / gain

    snp = 5.0
    sky_sigma = 1.0 / snp
    image += sky_sigma * np.random.standard_normal(size=(size1, size1))

    threshold = detect_threshold(image, 1.5)
    npixels = 5  # minimum number of connected pixels
    convolved_image = convolve(image, psf)
    segmap = detect_sources(convolved_image, threshold, npixels)
    #plt.imshow(segmap, origin='lower', cmap='gray')
    rarr=[ident,"","","","","","","","","","",""]
    try:
        source_morphs = statmorph.source_morphology(image, segmap, gain=gain, psf=psf)
        maxnum=0
        maxsize=0
        objcount=0
        for numobj,objs in enumerate(source_morphs) :
            objcount=objcount+1
            #if objs.rhalf_ellip>maxsize:
            if objs.sn_per_pixel>maxsize:
                    #maxsize=objs.rhalf_ellip
                    maxsize=objs.sn_per_pixel
                    maxnum=numobj
        morph = source_morphs[maxnum]
        print(maxnum,numobj,source_morphs[0].flag_sersic)
       
        y, x = np.mgrid[0:size1, 0:size1]
        sersic_model = morph._sersic_model(x, y)
        im2=image-sersic_model
        im3=numpy.zeros((size1,size1))
        for i,x in enumerate(im2):
                for j,y in enumerate(x):
                    if y<(3*sky_sigma):
                        im2[i][j]=0
                    if y>(5*sky_sigma):
                        im3[i][j]=y
                        
        threshold = detect_threshold(image, 1.5)
        finder = SourceFinder(npixels=5, progress_bar=False)
        segment_map = finder(im2, threshold)
        segment_map1 = finder(im3, threshold)
        sigma3=str(segment_map.nlabels)
        sigma5=str(segment_map1.nlabels)

        print(ident,str(morph.flag_sersic),sigma3,sigma5,str(morph.sersic_amplitude),str(morph.sersic_rhalf),str(morph.sersic_n),str(morph.sersic_xc),str(morph.sersic_yc),str(morph.sersic_ellip),str(morph.sersic_theta),str(morph.sersic_chi2_dof))
        rarr=[ident,str(morph.flag_sersic),sigma3,sigma5,str(morph.sersic_amplitude),str(morph.sersic_rhalf),str(morph.sersic_n),str(morph.sersic_xc),str(morph.sersic_yc),str(morph.sersic_ellip),str(morph.sersic_theta),str(morph.sersic_chi2_dof)]
    except: 
    #except Exception as e: print(e)
        pass
    return rarr
    
if __name__ == '__main__':
    starttime = time.time()
    path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
    save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
    ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
    #ini_fold=["z_11"]
    rerez=[302,332,363,393,425,456,456]
    psfnamelist=["nircampsf090.fits","nircampsf115.fits","nircampsf115.fits","nircampsf140.fits","nircampsf150.fits","nircampsf162.fits","nircampsf162.fits"]
    names=[]
    sendtotal=[]
    results=[]
    for x in ini_fold :
        current=path+"/"+x
        if x=="z_11":
            current=path+"/"+"z_10"
        #print(current)
        regions=[]
        dir_list = os.listdir(current)
        regions=dir_list
        regions=[f for f in regions if os.path.isdir(current+'/'+f)]
        if x=="z_11":
            current=path+"/"+"z_10"
            regions=["flares_10"]
        for y in regions :
            latest=current+"/"+y
            galaxies = os.listdir(latest)
            galaxies=[f for f in galaxies if os.path.isdir(latest+'/'+f)]
            for z in galaxies:
                final=latest+"/"+z
                edited="/"+x+"/"+y+"/"+z
                if x=="z_11":
                    edited="/"+"z_10"+"/"+y+"/"+z
                idn=x+"/"+y+"/"+z
                redshift=x[2:]
                zint=int(redshift)
                ######### Your are in the folder where the SKIRT files
                filename=path+edited+"/flares_cube_UV_total.fits"
                psffile="/home/projects/dtu_00026/people/paupun/PSF/"+ psfnamelist[zint-5]
                abc=[idn,filename,psffile,str(rerez[zint-5])]
                sendtotal.append(abc)
    pool = multiprocessing.Pool()
    print(len(sendtotal))
    #print(pool.map(multiprocessing_func,sendtotal))
    results.append(pool.map(multiprocessing_func,sendtotal))
    ids=[]
    sersicflag=[]
    sigma3sources=[]
    sigma5sources=[]
    sersic_amplitude=[]
    sersic_rhalf=[]
    sersic_n=[]
    sersic_xc=[]
    sersic_yc=[]
    sersic_ellip=[]
    sersic_theta=[]
    sersic_chi2_dof=[]
    for tortilla in results[0]:
        ids.append(tortilla[0])
        sersicflag.append(tortilla[1])
        sigma3sources.append(tortilla[2])
        sigma5sources.append(tortilla[3])
        sersic_amplitude.append(tortilla[4])
        sersic_rhalf.append(tortilla[5])
        sersic_n.append(tortilla[6])
        sersic_xc.append(tortilla[7])
        sersic_yc.append(tortilla[8])
        sersic_ellip.append(tortilla[9])
        sersic_theta.append(tortilla[10])
        sersic_chi2_dof.append(tortilla[11])
    df=pd.DataFrame({'ID':ids,'Sersic Flag':sersicflag,'sigma3res':sigma3sources,'sigma5res':sigma5sources,'sersic_amplitude':sersic_amplitude,'sersic_rhalf':sersic_rhalf,'sersic_n':sersic_n,'sersic_xc':sersic_xc,'sersic_yc':sersic_yc,'sersic_ellip':sersic_ellip,'sersic_theta':sersic_theta,'sersic_chi2_dof':sersic_chi2_dof})
    print(df)
    df.to_csv("/home/projects/dtu_00026/people/paupun/dust_continuum/output/SersicProfile.csv")
    print('That took {} seconds'.format(time.time() - starttime))
