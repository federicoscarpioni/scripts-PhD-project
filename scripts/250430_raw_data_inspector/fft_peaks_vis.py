import json
import math
import numpy as np

from deistools.processing import MultiFrequencyAnalysis
from deistools.processing.data_loader import load_voltage_current
from deistools.processing.data_preparation import cut_signal_head

# ================
# User parameters
# ================

sampling_time = 2e-2
multisine_period = 1

# waveforms_directory = 'E:/multisine_collection/'
# waveform_name = '2505151210multisine_splitted_quasi-log_100kHz-10mHz_8ptd_flat_norm_random_phases'
# multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
# multisine_low_path = waveforms_directory+waveform_name+'/low_band/'

# frequencies_multisine = np.array(
#     json.load(
#         open(multisine_low_path + "waveform_metadata.json")
#         )["Frequencies / Hz"]
# )
# frequencies_multisine = np.append(
#     frequencies_multisine,
#     json.load(open(multisine_high_path + "waveform_metadata.json")
#               )["Frequencies / Hz"]
# )
# frequencies_analysis = frequencies_multisine[:12]
waveforms_directory = 'E:/multisine_collection/'
waveform_name_cp = '2507261009multisine_splitted_100kHz-10mHz_cp'
frequencies = np.load(waveforms_directory + waveform_name_cp + '/total_frequencies.npy')
frequencies_analysis = frequencies[0:20]

# ==========
# Main code
# ==========

voltage, current, _ = load_voltage_current()
# Check for integer number of multisine periods
# signal_duration = voltage.size * sampling_time
# if signal_duration % multisine_period != 0:
#     signal_size = int(math.floor(signal_duration/multisine_period)*multisine_period /sampling_time)
#     voltage = cut_signal_head(voltage, signal_size)
#     current = cut_signal_head(current, signal_size)
#     print('Signal reduced')

analysis = MultiFrequencyAnalysis(
	frequencies_analysis,
	voltage,
	current,
	sampling_time,
)

analysis.compute_fft()
analysis.compute_freq_axis()
analysis.compute_freq_indexes(analysis.ft_current)
analysis.visualise_peaks()