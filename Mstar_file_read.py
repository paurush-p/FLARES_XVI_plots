import h5py
import numpy
f = h5py.File("C:/Users/pauru/Documents/SKIRT/flares_00/flares_skirt_outputs.hdf5",'r')
data=f['00/007_z008p000/Galaxy/Mstar']
Mass=numpy.array(data)

Mass= [abc*(10**10) for abc in Mass]
numpy.savetxt("C:/Users/pauru/Documents/SKIRT/flares_00/Mass.txt", Mass)
print("Done")
