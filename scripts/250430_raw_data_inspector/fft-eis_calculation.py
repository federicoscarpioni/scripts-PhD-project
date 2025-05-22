import json
import numpy as np
import matplotlib.pyplot as plt

from deistools.processing import MultiFrequencyAnalysis
from deistools.processing.data_loader import load_voltage_current


# ================
# User parameters
# ================

sampling_time = 4e-6

waveforms_directory = 'E:/multisine_collection/'
waveform_name = '2505151210multisine_splitted_quasi-log_100kHz-10mHz_8ptd_flat_norm_random_phases'
multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
multisine_low_path = waveforms_directory+waveform_name+'/low_band/'
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
frequencies_analysis = frequencies_multisine[20:]

# ==========
# Main code
# ==========

voltage, current, _ = load_voltage_current()

analysis = MultiFrequencyAnalysis(
	frequencies_analysis,
	voltage,
	current,
	sampling_time,
)

analysis.compute_fft()
analysis.compute_freq_axis()
analysis.search_freq_indexes(analysis.ft_current)
impedance = analysis.run_fft_eis()
plt.figure()
plt.plot(impedance.real, - impedance.imag, '-o')
plt.axis('equal')
plt.show()