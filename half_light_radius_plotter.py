import matplotlib.pyplot as plt
i=0
redshift=8
hlrn=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy.txt")
wavnumpy=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wav.txt")
hlrn_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy_uv.txt")
wavnumpy_uv=numpy.loadtxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths_uv.txt")
for x in hlrn :
    name="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/combined.pdf"
    namepng="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/combined.png"
    name_uv="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/uv.pdf"
    namepng_uv="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/uv.png"
    name_dust="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/dust.pdf"
    namepng_dust="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+"/dust.png"
    title="Half Light Radius v/s Wavelength (z="+str(redshift)+"): Galaxy " + str(i)
    wavelength_axis=list(wavnumpy[i])
    half_light_axis=list(hlrn[i])
    wavelength_axis_uv=list(wavnumpy_uv[i])
    half_light_axis_uv=list(hlrn_uv[i])
    half_light_axis=[150*x for x in half_light_axis]
    half_light_axis_uv=[150*x for x in half_light_axis_uv]
    plt.plot(wavelength_axis, half_light_axis,marker='.' ,linewidth=1)
    plt.title(title)
    plt.xlabel('Wavelength (Micron)')
    plt.ylabel('Half Light radius (pc) ')
    plt.xscale('log')
    plt.savefig(name_dust)
    plt.savefig(namepng_dust)
    plt.plot(wavelength_axis_uv, half_light_axis_uv,marker='.',linewidth=1)
    #plt.show()
    plt.savefig(name)
    plt.savefig(namepng)
    plt.clf()
    plt.plot(wavelength_axis_uv, half_light_axis_uv,marker='.',linewidth=1)
    plt.title(title)
    plt.xlabel('Wavelength (Micron)')
    plt.ylabel('Half Light radius (pc) ')
    plt.xscale('log')
    plt.savefig(name_uv)
    plt.savefig(namepng_uv)
    plt.clf()
    i+=1
print("Done")
