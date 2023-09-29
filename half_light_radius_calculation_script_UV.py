###################UV###########################################
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
import numpy
from scipy import interpolate
import time

start = time.time()
file_names_wav=["C:/Users/pauru/Documents/SKIRT/flares_00/gal_000/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_001/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_002/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_003/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_004/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_005/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_006/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_007/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_008/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_009/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_010/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_011/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_012/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_013/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_014/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_015/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_016/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_017/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_018/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_019/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_020/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_021/flares_cube_UV_sed.dat",
               "C:/Users/pauru/Documents/SKIRT/flares_00/gal_022/flares_cube_UV_sed.dat"]
file_names_fits=["C:/Users/pauru/Documents/SKIRT/flares_00/gal_000/flares_cube_UV_total.fits",
                 "C:/Users/pauru/Documents/SKIRT/flares_00/gal_001/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_002/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_003/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_004/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_005/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_006/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_007/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_008/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_009/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_010/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_011/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_012/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_013/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_014/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_015/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_016/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_017/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_018/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_019/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_020/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_021/flares_cube_UV_total.fits",
                "C:/Users/pauru/Documents/SKIRT/flares_00/gal_022/flares_cube_UV_total.fits"]
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
print(amount_of_layers)
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
    center=(199,199)
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
        while sumhf<(0.75*sum) :
            #print(radius)
            #print(sumhf, sum)
            m=max(0,k-radius)
            while m<min(k+radius+1,size_x):
                n=max(0,l-radius)
                while n<min(l+radius+1,size_y):
                    sumhf+=image[m][n]
                    #print(r,radius)
                    n+=1
                m+=1
            sum_r.append(sumhf)
            r.append(radius)
            radius+=1
            #print(radius)
        #print(sum_r)
        #print(r)
        nr=numpy.array(r)
        nsum_r=numpy.array(sum_r)
        f=interpolate.interp1d(nsum_r,nr, fill_value="extrapolate")
        numpy_interpolated_radius=numpy.interp((sum/2),nsum_r,nr)
        scipy_interpolated_radius=f(sum/2)
        half_light_radius.append(radius)
        #print("Test", radius, numpy_interpolated_radius, scipy_interpolated_radius)
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
hlr_uv = numpy.array(half_light_r_filewise)
hlrn_uv = numpy.array(half_light_r_filewise_numpy)
hlrs_uv = numpy.array(half_light_r_filewise_scipy)
hl_uv = numpy.array(half_light_filewise)
wavelengths_uv= numpy.array(extracted_wav)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_uv.txt", hl_uv)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_uv.txt", hlr_uv)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_numpy_uv.txt", hlrn_uv)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Half_light_R_scipy_uv.txt", hlrs_uv)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/run/Wavelengths_uv.txt", wavelengths_uv)
print("Done")
print("Total exec time :" , round(((time.time()-start)/60),2), "min.")
