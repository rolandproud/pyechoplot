'''

plot simple echogram with pulse mask

Modification History:

'''

## import packages
import matplotlib.pyplot as plt
import gzip
import pickle
from pyechomask.masks import binary_pulse

## import pyechoplot methods
from pyechoplot.plotting import plot_Sv, plot_mask, save_png_plot

## read Sv data data
def getSv(filepath):
    f   = gzip.open(filepath,'rb')
    obj = pickle.load(f,encoding = 'bytes')
    f.close()
    return obj
    
## parse PERG obj and output Sv (see readers.py)
Sv18 = getSv('./data/PS_Sv18.pklz')

## plot 18 kHz echogram
plot_Sv(Sv18)
plt.title("Sv18")
plt.show()

## create mask
pulse_mask_18 = binary_pulse(Sv18)

## plot 18 kHz echogram with pulse mask
plot_Sv(Sv18,mask = pulse_mask_18)
plt.title("18 kHz echogram with pulse mask")
plt.show()

#save
#save_png_plot('./','echogram')


