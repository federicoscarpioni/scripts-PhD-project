import numpy as np
import math
from numpy.fft import fft,ifft,fftshift,fftfreq
import matplotlib.pyplot as plt

from deistools.processing.data_loader import load_impedance_set
from deistools.visualise import plot_impedance_set
from deistools.processing.passband_filters import FermiDiracFilter

# ================
# User parameters
# ================

stfft_widow = 10
filter_bw = 0.01
filter_order = 8
dmfa_time_resolution = 100

# ==========
# Main code
# ==========

impedance_high_band, directory = load_impedance_set('Select high frequency impedance file')

impedance_low_band, _ = load_impedance_set('Select low frequency impedance file')


total_impedance = np.concatenate(
    (impedance_low_band,
    impedance_high_band),
    axis=0,
)

print(total_impedance.shape)
print(type(total_impedance))

plot_impedance_set(total_impedance)

np.save(directory+'/impedance_total.npy', total_impedance)