import numpy as np
import matplotlib.pyplot as mpl

def read_sampling_data(fn):

    data = []
    fs = open(fn,'r')
    for line in fs:
        strs = line.split()
        vec = []
        for si in strs:
            if si.strip() == '#':
                break
            else:
                vec.append(float(si))
        if len(vec) > 0 and vec[2] == 0:
            data.append(vec)

    fs.close()

    return np.array(data)

def sort_data(data):

    
    idx0 = np.where(data[:,0] == 0)
    idx1 = np.where(data[:,0] == 1)[0][0]

    data_01 = data[0:idx1+1]
    data_02 = data[idx1+2:]
          
    return [np.array(data_01), np.array(data_02)]

# ******************** 
# *** Main program ***
# ********************

file_name = 'foil.xy'

data = read_sampling_data(file_name)
[upper, lower] = sort_data(data)

xu = upper[:,0]
pu = upper[:,3]
xl = list(lower[:,0]); xl.insert(0,upper[0,0]);xl.append(upper[-1,0])
pl = list(lower[:,3]); pl.insert(0,upper[0,3]);pl.append(upper[-1,3])

fig, ax = mpl.subplots()
ax.plot(xu,pu,'-r')
ax.plot(xl,pl,'-g')
ax.set_xlabel('x')
ax.set_ylabel('p')
ax.grid()

fig.savefig('foil_pressure.pdf')