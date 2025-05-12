import json
import numpy as np

from deistools.processing.data_loader import load_voltage_current


multisine_path = "E:/multisine_collection/2409131232multisine_1kHz-100mHz_8ptd_fgen10kHz_random_phases_flat_normalized/"
frequencies = json.load(open(multisine_path + "waveform_metadata.json"))["Frequencies / Hz"]
frequencies = np.array(frequencies[11:])
sampling_time = 1e-4
time_window = 10

# Decimation
filter_cutoff = 8
filter_order = 8
time_experiment = 600
sampling_frequency = 1e4
resampling_frequency = 50
ds_factor = int(sampling_frequency // resampling_frequency)
buffer_size = int(time_experiment * resampling_frequency)

