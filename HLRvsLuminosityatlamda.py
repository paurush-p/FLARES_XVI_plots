################################################Relationship between luminosity and Radius at specific wavelength
import matplotlib.pyplot as plt
import numpy
import math
i=0
xaxis=[]
yaxis=[]
hlrn_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy_uv.txt")
for x in hlrn_uv :
    strname1="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{i:03}"+ "/flares_cube_UV_sed.dat"
    flux=numpy.loadtxt(strname1,usecols=1)
    wav_all=numpy.loadtxt(strname1,usecols=0)
    xaxis.append(math.log((flux[0]*4*math.pi*1*1*(10**12)*3.0856*(10**18)*3.0856*(10**18)*(10**-23)),10))
    yaxis.append(math.log(x[0],10)) #select x index based on wavelength to be evaluated
    i+=1
plt.scatter(xaxis, yaxis ,marker='*')
plt.plot(numpy.unique(xaxis), numpy.poly1d(numpy.polyfit(xaxis, yaxis, 1))(numpy.unique(xaxis)))
slope, intercept = numpy.polyfit(xaxis, yaxis, 1)
#slope_store_temp.append(slope)
plt.title("Relationship between L and r at 1000 A")
plt.xlabel('log(L) (erg/s/Hz)')
plt.ylabel('log(r) (pc)')
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/UV Luminosity vs Half Light radius at 1000 A.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/UV Luminosity vs Half Light radius at 1000 A.png")
