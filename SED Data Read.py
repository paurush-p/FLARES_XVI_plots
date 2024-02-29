import os
import matplotlib.pyplot as plt
import numpy
import time
path="/home/projects/dtu_00026/people/aswvij/Sims/SKIRT_FLARES/output"
save_path="/home/projects/dtu_00026/people/paupun/dust_continuum/output"
ini_fold=["z_5","z_6","z_7","z_8","z_9","z_10"]
#ini_fold=["z_10"]
start=time.time()
t=0
for x in ini_fold :
	current=path+"/"+x
	regions=[]
	dir_list = os.listdir(current)
	regions=dir_list
	regions=[f for f in regions if os.path.isdir(current+'/'+f)]
	for y in regions :
		latest=current+"/"+y
		galaxies = os.listdir(latest)
		galaxies=[f for f in galaxies if os.path.isdir(latest+'/'+f)]
		for z in galaxies:
			#print(x,y,z)
			final=latest+"/"+z
			edited="/"+x+"/"+y+"/"+z
			data_files=os.listdir(final)
			#print(data_files, x,y,z)
			######### Your are in the folder where the SKIRT files are
			#extracted_wav=[]
			#extracted_wav_d1=[]
			#extracted_wav_d2=[]
			file_name=final+"/flares_cube_dust_sed.dat"
			strname1=final+"/flares_def1_sed.dat"
			strname2=final+"/flares_def2_sed.dat"
			title1="Spectral Energy Distribution "+x+" Region "+y+" "+z
			name1=save_path+edited+"/sed.png"
			name2=save_path+edited+"/sed.pdf"
			raw_wavelengths=numpy.loadtxt(file_name,usecols=0)
			    #extracted_wav.append(raw_wavelengths)
			    #strname1="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{t:03}"+ "/flares_def1_sed.dat"
			    #strname2="C:/Users/pauru/Documents/SKIRT/flares_00/gal_"+f"{t:03}"+ "/flares_def2_sed.dat"
			raw_wavelengths_d1=numpy.loadtxt(strname1,usecols=0)
			raw_wavelengths_d2=numpy.loadtxt(strname2,usecols=0)
			    #extracted_wav_d1.append(raw_wavelengths_d1)
			    #extracted_wav_d2.append(raw_wavelengths_d2)
			tot_flux=numpy.loadtxt(file_name,usecols=1)
			tot_flux_d1=numpy.loadtxt(strname1,usecols=1)
			tot_flux_d2=numpy.loadtxt(strname2,usecols=1)
			plt.figure(figsize=(15,5))
			plt.plot(raw_wavelengths_d1,tot_flux_d1,label="def_1 instrument",linewidth=1)
			plt.plot(raw_wavelengths_d2,tot_flux_d2,label="def_2 instrument",linewidth=1)
			plt.plot(raw_wavelengths,tot_flux,label="cube instrument",linewidth=1)
			plt.legend(loc='lower right')
			plt.title(title1)
			plt.xlabel('Wavelength (Micron)')
			plt.ylabel('Total Flux F_nu (Jy) ')
			plt.yscale('log')
			plt.xscale('log')
			plt.savefig(name1)
			plt.savefig(name2)
			plt.close()
			t+=1
			#print("Galaxies Done :",t)
			   
			#wav_numpy=numpy.array(extracted_wav)
			#wav_d1_numpy=numpy.array(extracted_wav_d1)
			#wav_d2_numpy=numpy.array(extracted_wav_d2)
			#numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav.txt", wav_numpy)
			#numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav_d1.txt", wav_d1_numpy)
			#numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wav_d2.txt", wav_d2_numpy)
print("Done.Total execute time :", round((time.time()-start)/60.0,2))
