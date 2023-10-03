############################################                    HLR_statictics_vs_DTM
import numpy as np
import matplotlib.pyplot as plt
stats=np.loadtxt("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statistics.txt")
DTM=np.loadtxt("C:/Users/pauru/Documents/SKIRT/flares_00/DTM.txt")
#print(DTM)
minvals=[]
maxvals=[]
averages=[]
sigmas=[]
variation=[]
diff=[]
for x in stats :
    minvals.append(x[0])
    maxvals.append(x[1])
    averages.append(x[2])
    sigmas.append(x[3])
    variation.append(x[4])
    diff.append(x[1]-x[0])
plt.scatter(DTM,minvals, color="blue", s=5, label="min HLRs")
plt.scatter(DTM,maxvals, color="red", s=5, label="max HLRs")
plt.scatter(DTM,averages, color="orange", s=5, label="Mean HLR")
plt.scatter(DTM,sigmas, color="green", s=5, label="standard Deviation of HLRs")
plt.scatter(DTM,variation, color="magenta", s=5, label="variation of HLRs")
plt.scatter(DTM,diff, color="cyan", marker="*", label="max-min HLRs")
plt.title("DTM vs HLR")
plt.xlabel('Dust to Metal Ratio')
plt.ylabel('HLR statistics (px)')
plt.plot(numpy.unique(DTM), numpy.poly1d(numpy.polyfit(DTM, diff,1))(numpy.unique(DTM)), color="cyan", linestyle="--", label="best fit (max-min)HLR")
plt.plot(numpy.unique(DTM), numpy.poly1d(numpy.polyfit(DTM, maxvals,1))(numpy.unique(DTM)), color="red", linestyle="--",label="best fit max HLR")
plt.plot(numpy.unique(DTM), numpy.poly1d(numpy.polyfit(DTM, minvals,1))(numpy.unique(DTM)), color="blue", linestyle="--", label="best fit min HLR")
plt.plot(numpy.unique(DTM), numpy.poly1d(numpy.polyfit(DTM, averages,1))(numpy.unique(DTM)), color="gold", linestyle="--",label="best fit mean HLR")
#plt.plot(numpy.unique(DTM), numpy.poly1d(numpy.polyfit(DTM, diff,1))(numpy.unique(DTM)), color="cyan", linestyle="--")
#plt.xlim(0,0.1)
#plt.ylim(0,3)
plt.legend(loc='upper right',fontsize="7")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statictics_vs_DTM z=8.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statictics_vs_DTM z=8.png")
print("Done")
