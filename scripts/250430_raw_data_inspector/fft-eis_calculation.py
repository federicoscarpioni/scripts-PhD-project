import json
import numpy as np
import matplotlib.pyplot as plt

from deistools.processing import MultiFrequencyAnalysis
from deistools.processing.data_loader import load_voltage_current

sampling_time = 1e-6

multisine_high_path = 'E:/multisine_collection/2412111607multisine_splitted_100kHz-10mHz_8ptd_fgen1MHz_flat_norm_random_phases/low_freqs/'
multisine_low_path = 'E:/multisine_collection/2412111607multisine_splitted_100kHz-10mHz_8ptd_fgen1MHz_flat_norm_random_phases/high_freqs/'
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
frequencies_analysis = frequencies_multisine[28:]

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