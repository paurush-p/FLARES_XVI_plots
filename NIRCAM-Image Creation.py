from astropy.io import fits
import numpy
import cv2
import numpy as np
import matplotlib.pyplot as plt
from astropy.convolution import convolve, Gaussian2DKernel
from PIL import Image
from PIL import Image, ImageOps
from astropy.cosmology import Planck15 as cosmo
import math

def imagecreation(filename,wavelengths,redshift,filterR,filterG,filterB,psfR,psfG,psfB,aperturesize):
    #filename is the full location of fits file
    #wavelengths is a numpy array of wavelengths corresponding to each slide in fits cube
    #filterR/G/B are the names of NIRCAM filters
    #psfR/G/B are the psf fits file locations
    #aperture size is the total length of 1 axis in image in pkpc
    wavs=wavelengths


    psfreshapesize=60 #psfs are huge, takes these amounts of pixles around the point source
    psfrs=psfreshapesize/2

    filtername=["F070W","F090W","F115W","F140M","F150W","F162M","F164N","F150W2","F182M","F187N","F200W","F210M","F212N"]
    wavmin=[0.624,0.795,1.013,1.331,1.331,1.542,1.635,1.007,1.722,1.863,1.755,1.992,2.109]
    wavmax=[0.781,1.005,1.282,1.479,1.668,1.713,1.653,2.38,1.968,1.885,2.227,2.201,2.134]
    efferes=[0.237,0.318,0.333,0.434,0.476,0.469,0.385,0.489,0.505,0.434,0.525,0.522,0.42]

    rf=filtername.index(filterR)
    bf=filtername.index(filterB)
    gf=filtername.index(filterG)

    bmin=wavmin[bf]	
    bmax=wavmax[bf]
    rmin=wavmin[rf]
    rmax=wavmax[rf]	
    gmin=wavmin[gf]	
    gmax=wavmax[gf]
    ger=efferes[gf]
    rer=efferes[rf]
    ber=efferes[bf]

    image=(fits.getdata(filename, ext=0))
    psfb=(fits.getdata(psfB, ext=0))
    psfg=(fits.getdata(psfG, ext=0))
    psfr=(fits.getdata(psfR, ext=0))

    box=((psfb.shape[0]/2)-psfrs,(psfb.shape[0]/2)-psfrs,(psfb.shape[0]/2)+psfrs,(psfb.shape[0]/2)+psfrs)

    newpsf=Image.fromarray(psfb)
    newpsf1 = newpsf.crop(box)
    psfb=np.array(newpsf1)

    newpsf=Image.fromarray(psfr)
    newpsf1 = newpsf.crop(box)
    psfr=np.array(newpsf1)

    newpsf=Image.fromarray(psfg)
    newpsf1 = newpsf.crop(box)
    psfg=np.array(newpsf1)

    if ((psfb.shape[0]%2) == 0):
        newpsf=Image.fromarray(psfb)
        psfb=np.array(newpsf.resize((psfb.shape[0]-1,psfb.shape[1]-1)))


    if ((psfr.shape[0]%2) == 0):
        newpsf=Image.fromarray(psfr)
        psfr=np.array(newpsf.resize((psfr.shape[0]-1,psfr.shape[1]-1)))


    if ((psfg.shape[0]%2) == 0):
        newpsf=Image.fromarray(psfg)
        psfg=np.array(newpsf.resize((psfg.shape[0]-1,psfg.shape[1]-1)))


    #print(psfr.shape,psfb.shape,psfg.shape)

    snp =20.0
    sky_sigma = 0.333 / snp

    zint=redshift
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(aperturesize/distperpx))


    for wavi,x in enumerate(wavs):
        if x>(bmin/(zint+1)):
            bmi=wavi
            break
    for wavi,x in enumerate(wavs):
        if x>(bmax/(zint+1)):
            bma=wavi
            break
    for wavi,x in enumerate(wavs):
        if x>(rmin/(zint+1)):
            rmi=wavi
            break
    for wavi,x in enumerate(wavs):
        if x>(rmax/(zint+1)):
            rma=wavi
            break
    for wavi,x in enumerate(wavs):
        if x>(gmin/(zint+1)):
            gmi=wavi
            break
    for wavi,x in enumerate(wavs):
        if x>(gmax/(zint+1)):
            gma=wavi
            break
    #print(gmi,gma,bmi,bma,rmi,rma)

    green=numpy.zeros((400,400))
    i=gmi
    green1=np.zeros((size1,size1))
    while i<gma:
        green=green+(ger*image[i])
        green *= 1.0/green.max()
        imarr=Image.fromarray(green)
        green1=np.array(imarr.resize((size1,size1)))
        green1 = convolve(green1,psfg)
        green1 += sky_sigma * np.random.standard_normal(size=(size1, size1))
        green1 *= 1.0/green1.max() 
        i+=1
    red=numpy.zeros((400,400))
    i=rmi
    red1=np.zeros((size1,size1))
    while i<rma:
        red=red+(rer*image[i])
        red *= 1.0/red.max()

        imarr=Image.fromarray(red)
        red1=np.array(imarr.resize((size1,size1)))
        red1 = convolve(red1,psfr)
        red1 += sky_sigma * np.random.standard_normal(size=(size1, size1))
        red1 *= 1.0/red1.max()
        i+=1
    blue=numpy.zeros((400,400))
    i=bmi
    blue1=np.zeros((size1,size1))
    while i<bma:
        blue=blue+(ber*image[i])
        blue *= 1.0/blue.max() 

        imarr=Image.fromarray(blue)
        blue1=np.array(imarr.resize((size1,size1)))
        
        blue1 = convolve(blue1,psfb)
        blue1 += sky_sigma * np.random.standard_normal(size=(size1, size1))
        blue1 *= 1.0/blue1.max() 
        i+=1

    image_merge = cv2.merge([red1, green1, blue1]) 
    return image_merge



abc=numpy.genfromtxt('/home/projects/dtu_00026/people/paupun/Imaging.txt',dtype='str')
imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+abc[1]+"/flares_cube_UV_total.fits"
wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
z=5
fr="F200W"
fg="F150W"
fb="F115W"

psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

asize=60

plt.imshow(imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize),origin='lower')
plt.show()
