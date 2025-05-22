import json

import numpy as np
import matplotlib.pyplot as plt

from deistools.processing import MultiFrequencyAnalysis, fermi_dirac_filter
from deistools.processing.data_loader import load_voltage_current

# ================
# User parameters
# ================

sampling_time = 1e-6
filter_cutoff = 9
filter_order = 25

waveforms_directory = 'E:/multisine_collection/'
waveform_name = '2505151210multisine_splitted_quasi-log_100kHz-10mHz_8ptd_flat_norm_random_phases'
multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
multisine_low_path = waveforms_directory+waveform_name+'/low_band/'

# ==========
# Main code
# ==========

frequencies_multisine = np.array(
    json.load(
        open(multisine_low_path + "waveform_metadata.json")
        )["Frequencies / Hz"]
)
frequencies_multisine = np.append(
    frequencies_multisine,
    json.load(open(multisine_high_path + "waveform_metadata.json")
              )["Frequencies / Hz"]
)
frequencies_analysis = frequencies_multisine[:28]

voltage, current, _ = load_voltage_current()

analysis = MultiFrequencyAnalysis(
	frequencies_analysis,
	voltage,
	current,
	sampling_time,
)

analysis.compute_freq_axis()
analysis.compute_fft()

fermi_dirac_low_pass = fermi_dirac_filter(
    analysis.freq_axis, 
    0, 
    filter_cutoff, 
    filter_order
   )


fig, ax1 = plt.subplots()
ax1.semilogy(analysis.freq_axis, abs(analysis.ft_voltage)*fermi_dirac_low_pass, '-o', color = 'blue', label = 'Filtered signal')
ax1.semilogy(analysis.freq_axis, abs(analysis.ft_voltage), '-o', color = 'blue',alpha = 0.1, label = 'Original signal')
ax1.set_ylabel('Voltage / V')
ax1.axvline(filter_cutoff, color = 'gray', ls = '--', label='Cut-off freq')
ax1.legend()
ax1.set_ylim((1e-8, max(abs(analysis.ft_voltage))))
ax2 = ax1.twinx()
ax2.semilogy(analysis.freq_axis, fermi_dirac_low_pass, color = 'orange')
ax2.set_ylabel('Filter value')
ax2.set_ylim((1e-8,max(abs(analysis.ft_voltage))))
ax1.set_xlim((-4, 50))
plt.show()