import matplotlib.pyplot as plt
import numpy
import math
import scipy
half_light_radius=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy.txt")
wavelengths=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths.txt")
half_light_radius_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy_uv.txt")
wavelengths_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths_uv.txt")
i=0
rsum1=[]
rsum2=[]
psum=[]
for x in half_light_radius :
    hlr0=half_light_radius[i]
    wav0=wavelengths[i]
    hlr0_uv=half_light_radius_uv[i]
    wav0_uv=wavelengths_uv[i]
    #wav0=[x/80.0 for x in wav0]
    hlrx=[]
    wavx=[]
    j=0
    while j<25:
        #print(wav0[j],wav0_uv[j])
        hlrx.append(hlr0[j])
        wavx.append(wav0[j])
        j+=1
    #plt.plot(wavx,hlrx, marker='o')
    #plt.plot(wav0_uv,hlr0_uv, marker='o')
    #plt.xlim(0,0.45)
    r=numpy.corrcoef(hlrx, hlr0_uv)
    r_scipy, p = scipy.stats.pearsonr(hlrx, hlr0_uv)
    rsum1.append(r[0][1])
    rsum2.append(r_scipy)
    psum.append(p)
    #print(r[0][1], r_scipy, p)
    i+=1
rs1=numpy.array(rsum1)
rs2=numpy.array(rsum2)
ps=numpy.array(psum)
r1avg=numpy.mean(rs1)
r2avg=numpy.mean(rs2)
pavg=numpy.mean(ps)
xaxis=numpy.arange(1,24)
line7=np.full((23,),0.7)
line0=np.full((23,),0.0)
plt.scatter(xaxis,rs1,s=7,marker='x',color='green')
plt.plot(xaxis,line7,linestyle="--",color='red')
plt.ylim(0,1)
print("Averaged Values:")
print(r1avg,r2avg,pavg)
plt.title("Galaxy-wise correlation factor b/w HLR in dust and UV continuum")
plt.ylabel('Pearson correlation coefficient')
plt.xlabel('Galaxy number')
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/Pearson correlation coefficient z=8.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/Pearson correlation coefficient z=8.png")
plt.clf()
plt.scatter(xaxis,ps,s=15,marker='x',color='magenta')
plt.plot(xaxis,line0,linestyle="--",color='red')
plt.title("Galaxy-wise p-value b/w HLR in dust and UV continuum")
plt.ylabel('P-value')
plt.xlabel('Galaxy number')
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/P-value z=8.pdf")
plt.savefig("C:/Users/pauru/Documents/SKIRT/flares_00/P-value z=8.png")
