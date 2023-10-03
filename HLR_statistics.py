import matplotlib.pyplot as plt
import numpy

half_light_radius=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy.txt")
wavelengths=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths.txt")

i=0
stats=[]
for x in half_light_radius :
    galaxy_wise_stats=[]
    hlr=x
    wav=wavelengths[i]
    minv=numpy.min(hlr)
    maxv=numpy.max(hlr)
    avg=numpy.mean(hlr)
    sigma=numpy.std(hlr)
    var=numpy.var(hlr)
    galaxy_wise_stats.append(minv)
    galaxy_wise_stats.append(maxv)
    galaxy_wise_stats.append(avg)
    galaxy_wise_stats.append(sigma)
    galaxy_wise_stats.append(var)
    stats.append(galaxy_wise_stats)
    i+=1
stats_in_numpy=numpy.array(stats)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statistics.txt", stats_in_numpy)
print("Done")
