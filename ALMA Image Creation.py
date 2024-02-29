import casatasks
import multiprocessing

from casatasks import importfits
from casatasks import simobserve
from casatasks import concat
from casatasks import simanalyze
from casatasks import simalma
from casatasks import exportfits
from casatasks import tclean
#import casaviewer
import os
import shutil

def multiprocessing_func(y):
    x=y[1]
    idn=y[0]
    freq=y[2]
    rarr=["done"]
    importfits(fitsimage="almatest/"+x,imagename=idn+".casa",whichrep=0,
        whichhdu=-1,zeroblanks=True,overwrite=True,defaultaxes=False,defaultaxesvalues=[],beam=[])

    #Simulate compact observations
    simobserve(project=idn,skymodel=idn+".casa/",inbright="",indirection="J2000 19h00m00 -40d00m00",incell="0.02arcsec"
        ,incenter=freq,inwidth="7.5GHz",complist="",compwidth="8GHz",setpointings=True,ptgfile="$project.ptg.txt",
        integration="10s",direction="",mapsize=['', ''],maptype="ALMA",pointingspacing="",caldirection="",
        calflux="1Jy",obsmode="int",refdate="2014/05/21",hourangle="transit",totaltime="216s",
        antennalist="alma.cycle10.8.cfg",sdantlist="aca.tp.cfg",sdant=0,thermalnoise="tsys-atm",
        user_pwv=5,t_ground=269.0,t_sky=260.0,tau0=0.1,seed=11111,leakage=0.0,graphics="both",verbose=False,overwrite=True)
    
    #Cleaning
    tclean(vis="./"+idn+"/"+idn+".alma.cycle10.8.ms", imagename=idn+"_tclean", imsize=400, cell='0.02arcsec', specmode='mfs',deconvolver='hogbom', gridder='standard', weighting='natural', niter=10000 )

    #Write out the cleaned image as a FITS file
    exportfits(idn+"_tclean.image",fitsimage="almaimages/"+idn+"_alma.fits",
                   velocity=False,optical=False,bitpix=-32,minpix=0,maxpix=-1,overwrite=True,
                   dropstokes=False,stokeslast=True,history=True,dropdeg=False)
    
    shutil.rmtree(idn, ignore_errors=True)
    shutil.rmtree(idn+".casa", ignore_errors=True)
    shutil.rmtree(idn+".casa", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.image", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.mask", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.model", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.pb", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.psf", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.residual", ignore_errors=True)
    shutil.rmtree(idn+"_tclean.sumwt", ignore_errors=True)
    return rarr
    
if __name__ == '__main__':
    sendtotal=[]
    donecount=0
    for num,x in enumerate(os.listdir("almatest")):
        idn=x[:-5]
        zint=int(x[:-23][2:])
        lamda=1.58e-4*(zint+1)
        c=299792458.00
        f=(c/lamda)/1e9
        freq=str(round(f,2))+"GHz"
        #print(idn,zint,freq,num)
        donelist=os.listdir("almaimages")

        if (idn+"_alma.fits") in donelist :
            donecount+=1
            #print("done")
        else :
            abc=[idn,x,freq]
            sendtotal.append(abc)
    print(donecount)
    pool = multiprocessing.Pool()
    #print(sendtotal)
    print(pool.map(multiprocessing_func,sendtotal))
    
