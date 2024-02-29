from astropy.io import fits
from PIL import Image
import numpy
abc=numpy.genfromtxt('highoffset.txt',dtype='str')
for num,x in enumerate(abc):
    image1=(fits.getdata("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits", ext=0)[7])
    header01 = fits.getheader("/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output/"+x+"/flares_cube_UV_total.fits")
    hdu=fits.PrimaryHDU(image1,header=header01)
    #print("/home/projects/dtu_00026/people/paupun/highoffsetimages/"+x.replace("/","_")+".fits")
    hdu.writeto("/home/projects/dtu_00026/people/paupun/sameobjhighoff/"+x.replace("/","_")+".fits")
    print(num)
