import matplotlib.pyplot as plt
import numpy
sed_flux=[]
t=0
redshift=8
file_names_wav=["C:/Users/pauru/Documents/SKIRT/flares_00/gal_000/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_001/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_002/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_003/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_004/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_005/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_006/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_007/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_008/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_009/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_010/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_011/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_012/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_013/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_014/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_015/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_016/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_017/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_018/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_019/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_020/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_021/flares_cube_dust_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_022/flares_cube_dust_sed.dat"]
extracted_wav=[]
extracted_wav_d1=[]
extracted_wav_d2=[]
t=0
for x in file_names_wav:
    title1="Spectral Energy Distribution (z="+str(redshift)+"): Galaxy " + str(t)
    name1="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(t)+"/sed.png"
    name2="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(t)+"/sed.pdf"
    raw_wavelengths=numpy.loadtxt(x,usecols=0)
    extracted_wav.append(raw_wavelengths)
    strname1="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{t:03}"+ "/flares_def1_sed.dat"
    strname2="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{t:03}"+ "/flares_def2_sed.dat"
    raw_wavelengths_d1=numpy.loadtxt(strname1,usecols=0)
    raw_wavelengths_d2=numpy.loadtxt(strname2,usecols=0)
    extracted_wav_d1.append(raw_wavelengths_d1)
    extracted_wav_d2.append(raw_wavelengths_d2)
    tot_flux=numpy.loadtxt(x,usecols=1)
    tot_flux_d1=numpy.loadtxt(strname1,usecols=1)
    tot_flux_d2=numpy.loadtxt(strname2,usecols=1)
    
    plt.plot(raw_wavelengths_d1,tot_flux_d1,label="def_1 instrument",marker='.',linewidth=1)
    plt.plot(raw_wavelengths_d2,tot_flux_d2,label="def_2 instrument",marker='.',linewidth=1)
    plt.plot(raw_wavelengths,tot_flux,label="cube instrument",marker='.',linewidth=1)
    plt.legend(loc='lower right')
    plt.title(title1)
    plt.xlabel('Wavelength (Micron)')
    plt.ylabel('Total Flux F_nu (Jy) ')
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(name1)
    plt.savefig(name2)
    plt.clf()
    t+=1
    
wav_numpy=numpy.array(extracted_wav)
wav_d1_numpy=numpy.array(extracted_wav_d1)
wav_d2_numpy=numpy.array(extracted_wav_d2)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav.txt", wav_numpy)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav_d1.txt", wav_d1_numpy)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav_d2.txt", wav_d2_numpy)
print("Done")
