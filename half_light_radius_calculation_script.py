from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
import numpy
from scipy import interpolate
import time

start = time.time()
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
file_names_fits=["C:/Users/pauru/Documents/SKIRT/flares_00/gal_000/flares_cube_dust_total.fits",
                 "C:/Users/pauru/Documents/SKIRT/flares_00/gal_001/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_002/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_003/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_004/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_005/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_006/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_007/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_008/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_009/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_010/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_011/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_012/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_013/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_014/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_015/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_016/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_017/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_018/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_019/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_020/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_021/flares_cube_dust_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_022/flares_cube_dust_total.fits"]
extracted_wav=[]
half_light_r_filewise=[]
half_light_r_filewise_scipy=[]
half_light_r_filewise_numpy=[]
half_light_filewise=[]
amount_of_layers=0
for x in file_names_wav:
    with open(x) as f:
        lines_after_2 = f.readlines()[2:]
        column1 = [x.split() for x in lines_after_2]
        extracted = [float(y[0]) for y in column1]
        amount_of_layers= len(extracted)
        extracted_wav.append(extracted)
plt.style.use(astropy_mpl_style)
counter=1
for x in file_names_fits:
    print("File started:",counter)
    image_file = get_pkg_data_filename(x)
    image_data = fits.getdata(image_file, ext=0)
    z=0
    total_light=[]
    half_light=[]
    half_light_radius=[]
    half_light_radius_scipy=[]
    half_light_radius_numpy=[]
    center=(0,0)
    while z<amount_of_layers :
        r=[]
        sum_r=[]
        sum=0
        radius=0
        sumhf=0
        k=center[0]
        l=center[1]
        image=image_data[z]
        size_x=0
        size_y=0
        for x in image:
            size_x+=1
            for y in x:
                size_y+=1
                sum+=y
        total_light.append(sum)
        while sumhf<sum :
            m=max(0,k-radius)
            while m<min(k+radius+1,size_x):
                n=max(0,l-radius)
                while n<min(l+radius+1,size_y):
                    sumhf+=image[m][n]
                    sum_r.append(sumhf)
                    r.append(radius)
                    n+=1
                m+=1
            radius+=1
        nr=numpy.array(r)
        nsum_r=numpy.array(sum_r)
        f=interpolate.interp1d(nr,nsum_r, fill_value="extrapolate")
        numpy_interpolated_radius=numpy.interp((sum/2),nr,nsum_r)
        scipy_interpolated_radius=f(sum/2)
        half_light_radius.append(radius)
        half_light_radius_numpy.append(numpy_interpolated_radius)
        half_light_radius_scipy.append(scipy_interpolated_radius)
        half_light.append((sum/2))
        print("Running for :", round(((time.time()-start)/60),2), "min. File Number :", counter,"Image Number in file :", (z+1) )
        z+=1
    half_light_r_filewise.append(half_light_radius)
    half_light_r_filewise_scipy.append(half_light_radius_scipy)
    half_light_r_filewise_numpy.append(half_light_radius_numpy)
    half_light_filewise.append(half_light)
    print("File done :", counter)
    counter+=1
hlr = numpy.array(half_light_r_filewise)
hlrn = numpy.array(half_light_r_filewise_numpy)
hlrs = numpy.array(half_light_r_filewise_scipy)
hl = numpy.array(half_light_filewise)
wavelengths= numpy.array(extracted_wav)
print("Total exec time :" , round(((time.time()-start)/60),2), "min.")
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light.txt", hl)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R.txt", hlr)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy.txt", hlrn)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_scipy.txt", hlrs)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths.txt", wavelengths)
i=0
redshift=8
for x in hlrn :
    name="C:/Users/pauru/Documents/SKIRT/run/figures/galaxy"+str(i)+".pdf"
    title="Half Light Radius v/s Wavelength (z=",redshift,"): Galaxy " + str(i)
    wavelength_axis=extracted_wav[i]
    wavelength_axis=[10000*x for x in wavelength_axis]
    half_light_axis=half_light_r_filewise_numpy[i]
    half_light_axis=[0.15*x for x in half_light_axis]
    plt.plot(wavelength_axis, half_light_axis)
    plt.title(title)
    plt.xlabel('Wavelength (Angstom)')
    plt.ylabel('Half Light radius (Kpc) ')
    #plt.show()
    plt.savefig(name)
    plt.clf()
    i+=1
sed_flux=[]
t=0
for x in file_names_wav:
    with open(x) as f:
        lines_after_2 = f.readlines()[2:]
        title1="Spectral Energy Distribution (z=",redshift,"): Galaxy " + str(t)
        name1="C:/Users/pauru/Documents/SKIRT/run/figures/sed_galaxy"+str(t)+".png"
        column1 = [x.split() for x in lines_after_2]
        extracted_flux = [float(y[1]) for y in column1]
        x_wav_axis=extracted_wav[t]
        x_wav_axis=[10000*x for x in x_wav_axis]
        plt.plot(x_wav_axis, extracted_flux)
        plt.title(title1)
        plt.xlabel('Wavelength (Angstom)')
        plt.ylabel('Total Flux F_nu (Jy) ')
        #plt.show()
        plt.savefig(name1)
        plt.clf()
    t+=1
