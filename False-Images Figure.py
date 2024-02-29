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
from mpl_toolkits.axes_grid1.anchored_artists import (AnchoredSizeBar)
import matplotlib.font_manager as fm


def imagecreation(filename,wavelengths,redshift,filterR,filterG,filterB,psfR,psfG,psfB,aperturesize):
    #filename is the full location of fits file
    #wavelengths is a numpy array of wavelengths corresponding to each slide in fits cube
    #filterR/G/B are the names of NIRCAM filters
    #psfR/G/B are the psf fits file locations
    #aperture size is the total length of 1 axis in image in pkpc
    wavs=wavelengths


    psfreshapesize=60 #psfs are, takes these amounts of pixles around the point source
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


fig, ax = plt.subplots(6,5, figsize=(15,18))
fig.subplots_adjust(hspace=0,wspace=0)
z5=["z_5/flares_15/gal_100","z_5/flares_13/gal_166","z_5/flares_10/gal_087","z_5/flares_05/gal_038","z_5/flares_00/gal_124"]
for i,x in enumerate(z5):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=5
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #print(arr.shape[2])
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[0,i].imshow(load_original_arr,origin='lower')


    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[0]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
z6=["z_6/flares_08/gal_054","z_6/flares_16/gal_007","z_6/flares_07/gal_001","z_6/flares_01/gal_022","z_6/flares_00/gal_000"]    
for i,x in enumerate(z6):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=6
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[1,i].imshow(load_original_arr,origin='lower')


    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[1]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
z7=["z_7/flares_17/gal_019","z_7/flares_10/gal_008","z_7/flares_03/gal_001","z_7/flares_02/gal_007","z_7/flares_04/gal_000"]    
for i,x in enumerate(z7):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=7
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[2,i].imshow(load_original_arr,origin='lower')


    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[2]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
z8=["z_8/flares_05/gal_001","z_8/flares_14/gal_000","z_8/flares_10/gal_004","z_8/flares_04/gal_002","z_8/flares_04/gal_000"]    
for i,x in enumerate(z8):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=8
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[3,i].imshow(load_original_arr,origin='lower')



    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[3]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
z9=["z_9/flares_08/gal_010","z_9/flares_12/gal_003","z_9/flares_10/gal_002","z_9/flares_04/gal_002"]    
for i,x in enumerate(z9):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=9
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[4,i].imshow(load_original_arr,origin='lower')

    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[4]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
z10=["z_10/flares_00/gal_002","z_10/flares_08/gal_000","z_10/flares_17/gal_001","z_10/flares_04/gal_000"]    
for i,x in enumerate(z10):
    imagename="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits"
    wavelengths=numpy.loadtxt("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/z_5/flares_00/gal_000/flares_cube_UV_sed.dat",usecols=0)
    z=10
    fr="F200W"
    fg="F150W"
    fb="F115W"

    psfb="/home/projects/dtu_00026/people/paupun/PSF/nircampsf115.fits"
    psfg="/home/projects/dtu_00026/people/paupun/PSF/nircampsf150.fits"
    psfr="/home/projects/dtu_00026/people/paupun/PSF/nircampsf200.fits"

    asize=60
    #arr=imagecreation(imagename,wavelengths,z,fr,fg,fb,psfr,psfg,psfb,asize)
    #numpy.savetxt(x.replace("/","_")+".txt",arr.reshape(arr.shape[0], -1)) 

    loaded_arr = numpy.loadtxt(x.replace("/","_")+".txt")
    load_original_arr = loaded_arr.reshape(loaded_arr.shape[0], loaded_arr.shape[1] // 3, 3)
    ax[5,i].imshow(load_original_arr,origin='lower')


    zint=z
    distperpx=cosmo.angular_diameter_distance(zint).value*1.502922e-7*1e3
    size1=(math.ceil(asize/distperpx))
    for b in ax[5]:
        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(b.transData, (size1/20), '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)
        b.set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
        b.set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
blank=numpy.zeros((400,400))
size1=400
ax[4,4].imshow(blank,origin='lower',cmap='gray_r')
ax[4,4].set_xlim((size1/2)-(size1/4),(size1/2)+(size1/4))
ax[4,4].set_ylim((size1/2)-(size1/4),(size1/2)+(size1/4))
for x in ax:
    for y in x:
        y.get_xaxis().set_ticks([])
        y.get_yaxis().set_ticks([])

        #fontprops = fm.FontProperties(size=10, family='monospace')
        #bar = AnchoredSizeBar(y.transData, 20, '', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='white',fontproperties=fontprops)


        #y.add_artist(bar)
fontprops = fm.FontProperties(size=10, family='monospace')
bar = AnchoredSizeBar(ax[4,4].transData, 400/6, '10 pkpc', 4, pad=0.5,sep=5, borderpad=0.5, frameon=False,size_vertical=0.5, color='red',fontproperties=fontprops)


ax[4,4].add_artist(bar)
for i,x in enumerate(["5","6","7","8","9","10"]):
    ax[i,0].set_ylabel("z = "+x,fontsize = 20)

ax[0,0].set_title("$10^{9}$<(M*)/($M_\u2609$)<$10^{9.4}$",fontsize = 14)
ax[0,1].set_title("$10^{9.4}$<(M*)/($M_\u2609$)<$10^{9.8}$",fontsize = 14)
ax[0,2].set_title("$10^{9.8}$<(M*)/($M_\u2609$)<$10^{10.2}$",fontsize = 14)
ax[0,3].set_title("$10^{10.2}$<(M*)/($M_\u2609$)<$10^{10.6}$",fontsize = 14)
ax[0,4].set_title("$10^{10.6}$<(M*)/($M_\u2609$)",fontsize = 14)


fig.delaxes(ax[5,4])
#fig.delaxes(ax[4,4])
fig.savefig("PostStamp.pdf")
fig.savefig("PostStamp.png")
plt.close()
#plt.show()