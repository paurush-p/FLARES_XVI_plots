###################################Observed Wavelength HLR ratio with 866 um
import matplotlib.pyplot as plt
import numpy
import math
half_light_radius=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy.txt")
wavelengths=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths.txt")
#print(wavelengths.shape)
#print(half_light_radius.shape)
i=0
redshift=8
ratios_vs_866um=[]
for x in half_light_radius :
    wav_axis=wavelengths[i]
    wav_axis=[xyz*(redshift+1) for xyz in wav_axis]
    hlrs=x
    hlrs=[y/hlrs[51] for y in hlrs]
    ratios_vs_866um.append(hlrs)
    plt.scatter(wav_axis,hlrs,s=0.3)
    i+=1
averaged_ratio=[]
#print(wav_axis)
n=0
while n<100 :
    sum_val=0
    m=0
    while m<23 :
        sum_val+=ratios_vs_866um[m][n]
        m+=1
    av_val=sum_val/23.0
    averaged_ratio.append(av_val)
    n+=1
#print(averaged_ratio)
plt.plot(wav_axis,averaged_ratio, linewidth=3)
plt.title("HLR Ratio")
plt.xlabel('Observed Wavelengths (lamda) (um)')
plt.ylabel('r_lamda_obs/r_866um')
plt.xlim(0,2000)
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR diff wav vs HLR 866.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR diff wav vs HLR 866.png")
