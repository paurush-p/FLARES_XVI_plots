from astropy.io import fits
import numpy
import os
abc=numpy.genfromtxt('highoffset.txt',dtype='str')
path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
done=0
#ini_fold=["z_10"]
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
                filename=path+edited+"/flares_cube_dust_total.fits"
                image1=(fits.getdata(filename, ext=0)[61])
                header01 = fits.getheader(filename)
                hdu=fits.PrimaryHDU(image1,header=header01)
                #print("/home/projects/dtu_00026/people/paupun/highoffsetimages/"+x.replace("/","_")+".fits")
                hdu.writeto("/home/projects/dtu_00026/people/paupun/almatest/"+idn.replace("/","_")+".fits",overwrite=False)
                #print(num)
                done+=1
                print("galaxies done: ",done)
