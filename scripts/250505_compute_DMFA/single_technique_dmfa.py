import math
import json

import numpy as np

from deistools.processing import MultiFrequencyAnalysis
from deistools.processing.passband_filters import FermiDiracFilter
from deistools.processing.data_loader import load_voltage_current
from deistools.processing import detrending

from deistools.visualise import plot_impedance_set


# ================
# User parameters
# ================

sampling_time = 2e-3
filter_bw = 0.01
filter_order = 8
dmfa_time_resolution = 100

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

# ==========
# Main code
# ==========

voltage, current, directory = load_voltage_current()
# Detrend original signals
voltage, coord_volt = detrending.remove_baseline(voltage, sampling_time)
current, coord_curr = detrending.remove_baseline(current, sampling_time)


analysis = MultiFrequencyAnalysis(
	frequencies_analysis,
	voltage,
	current,
	sampling_time,
)

# Perform frequency analysis
analysis.compute_fft()
analysis.compute_freq_axis()
analysis.compute_freq_indexes(analysis.ft_current)

# Perform DMFA
total_exp_time = analysis.ft_voltage.size * sampling_time
Npts_elab = math.floor(total_exp_time/dmfa_time_resolution)
print(f'Number of impedance spectra: {Npts_elab}')
frequency_range = np.linspace(-1/(2*dmfa_time_resolution), 1/(2*dmfa_time_resolution), Npts_elab)
fd_filter = FermiDiracFilter(
    frequency_range,
    0,
    filter_bw,
    filter_order,
)
impedance, voltage, current, time = analysis.run_dmfa(
    fd_filter.values, 
    dmfa_time_resolution,
    Npts_elab
)

plot_impedance_set(impedance)

np.save(directory+'/impedance_low_freq.npy', impedance)