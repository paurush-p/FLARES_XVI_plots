#############################Slopes of best fit line in Relationship between luminosity and Radius at specific wavelength
import matplotlib.pyplot as plt
import numpy
import math
hlrn_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy_uv.txt")
Wav_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths_uv.txt")
same_wav=Wav_uv[0]
klm=0
total_x=[]
total_y=[]
total_slope=[]
for y in same_wav:
    xaxis=[]
    yaxis=[]
    i=0
    for x in hlrn_uv :
        strname1="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{i:03}"+ "/flares_cube_UV_sed.dat"
        flux=numpy.loadtxt(strname1,usecols=1)
        wav_all=numpy.loadtxt(strname1,usecols=0)
        xaxis.append(math.log((flux[klm]*4*math.pi*1*1*(10**12)*3.086*(10**18)*3.086*(10**18)*(10**-23)),10))
        yaxis.append(math.log(x[klm],10))
        i+=1
    total_x.append(xaxis)
    total_y.append(yaxis)
    klm+=1
    slope, intercept= numpy.polyfit(xaxis, yaxis, 1)
    total_slope.append(slope)
xaxis=list(same_wav)
#print(xaxis)

#print(total_slope)
plt.scatter(same_wav, total_slope)
plt.plot(numpy.unique(xaxis), numpy.poly1d(numpy.polyfit(xaxis, total_slope,2))(numpy.unique(xaxis)))
plt.title("Slope Relation")
plt.xlabel('UV Wavelength (um)')
plt.ylabel('Slope')
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/Slope of logRbylogL wrt wavelength.pdf")
tx=numpy.array(total_x)
ty=numpy.array(total_y)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/flares_00/Wavelength_Wise_Luminosity_UV.txt", tx)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/flares_00/Wavelength_Wise_HLR_UV.txt", ty)
print("Done")
