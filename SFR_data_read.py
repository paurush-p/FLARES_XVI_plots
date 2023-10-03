import h5py
import numpy
f = h5py.File("C:/Users/pauru/Documents/SKIRT/flares_00/flares_skirt_outputs.hdf5",'r')
data=f['00/007_z008p000/Galaxy/SFR']
SFR=numpy.array(data)
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/flares_00/SFR.txt", SFR)
print("Done")
