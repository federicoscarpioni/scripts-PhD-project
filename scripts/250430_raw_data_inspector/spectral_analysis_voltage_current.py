import json
import numpy as np

from deistools.processing import MultiFrequencyAnalysis

from deistools.processing.data_loader import load_voltage_current

sampling_time = 2e-2

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
frequencies_analysis = frequencies_multisine[:28]

voltage, current, _ = load_voltage_current()

analysis = MultiFrequencyAnalysis(
	frequencies_analysis,
	voltage,
	current,
	sampling_time,
)

analysis.compute_fft()
analysis.compute_freq_axis()
fig, axs = analysis.inspect_spectrum()