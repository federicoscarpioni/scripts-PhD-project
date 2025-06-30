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

# Apply the same filter of the DMFA to the STFFT-EIS impedance
number_points = impedance_low_band.shape[1]
frequencies_fft = fftshift(fftfreq(number_points, dmfa_time_resolution))
filter_dmfa = FermiDiracFilter(
    frequencies_fft,
    0,
    filter_bw,
    filter_order,
)
impedance_high_band_filtered = np.zeros((impedance_high_band.shape[0], number_points), dtype=np.complex64)
frequencies_axis = fftshift(fftfreq(impedance_high_band.shape[1], stfft_widow))
# index_f0 = np.where(frequencies_axis == 0)[0][0]
index_f0 = int(frequencies_axis.size/2)
filter_range = np.arange(index_f0 - math.floor(number_points/2), index_f0 + math.ceil(number_points/2), 1)
for i in range(impedance_high_band.shape[0]):
    fft_z_high = fftshift(fft(impedance_high_band[i,:]))/impedance_high_band[i,:].size
    impedance_high_band_filtered[i,:] = number_points * ifft(fftshift(fft_z_high[filter_range]*filter_dmfa.values))

    plt.semilogy(frequencies_axis[filter_range], np.abs(fft_z_high[filter_range]), label= f'Freq {i}', alpha=0.3)
    plt.semilogy(frequencies_axis[filter_range], np.abs(fft_z_high[filter_range]*filter_dmfa.values))
    # plt.semilogy(frequencies_fft, abs(impedance_high_band_filtered[i,:]), label= f'Freq {i}')
plt.semilogy(frequencies_fft, filter_dmfa.values, color = 'black')
plt.legend()
plt.show()

plot_impedance_set(impedance_high_band_filtered)

total_impedance = np.concatenate(
    (impedance_low_band,
    impedance_high_band_filtered),
    axis=0,
)

print(total_impedance.shape)
print(type(total_impedance))

plot_impedance_set(total_impedance)

np.save(directory+'/impedance_total.npy', total_impedance)