############################################                    HLR_statictics_vs_SFR
import numpy as np
import matplotlib.pyplot as plt
stats=np.loadtxt("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statistics.txt")
SFR=np.loadtxt("C:/Users/pauru/Documents/SKIRT/flares_00/SFR.txt")
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
plt.scatter(SFR,minvals, color="blue", s=5, label="min HLRs")
plt.scatter(SFR,maxvals, color="red", s=5, label="max HLRs")
plt.scatter(SFR,averages, color="orange", s=5, label="Mean HLR")
plt.scatter(SFR,sigmas, color="green", s=5, label="standard Deviation of HLRs")
plt.scatter(SFR,variation, color="magenta", s=5, label="variation of HLRs")
plt.scatter(SFR,diff, color="cyan", marker="*", label="max-min HLRs")
plt.title("SFR vs HLR")
plt.xlabel('Star Formation Rate (M\u2609/yr)')
plt.ylabel('HLR statistics (px)')
plt.plot(numpy.unique(SFR), numpy.poly1d(numpy.polyfit(SFR, diff,1))(numpy.unique(SFR)), color="cyan", linestyle="--", label="best fit (max-min)HLR")
plt.plot(numpy.unique(SFR), numpy.poly1d(numpy.polyfit(SFR, maxvals,1))(numpy.unique(SFR)), color="red", linestyle="--",label="best fit max HLR")
plt.plot(numpy.unique(SFR), numpy.poly1d(numpy.polyfit(SFR, minvals,1))(numpy.unique(SFR)), color="blue", linestyle="--", label="best fit min HLR")
plt.plot(numpy.unique(SFR), numpy.poly1d(numpy.polyfit(SFR, averages,1))(numpy.unique(SFR)), color="gold", linestyle="--",label="best fit mean HLR")
plt.plot(numpy.unique(SFR), numpy.poly1d(numpy.polyfit(SFR, variation,1))(numpy.unique(SFR)), color="black", linestyle="--",label="best fit variation of HLR")
plt.legend(loc='upper right',fontsize="7")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statictics_vs_SFR z=8.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/HLR_statictics_vs_SFR z=8.png")
print("Done")
