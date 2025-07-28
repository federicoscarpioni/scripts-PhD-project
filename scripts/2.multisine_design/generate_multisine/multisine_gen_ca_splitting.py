from multisine import Multisine, amplitude_extraction_from_experiment, show_extracted_amplitude_from_experiment
import numpy as np
import json
import matplotlib.pyplot as plt

harmonics = np.loadtxt('scripts/250512_multisine_design/data/harmonics_7decs_no_intermod_second_8ptsdec.txt')
base_frequency = 0.01
max_frequency = 100000
frequencies = harmonics * base_frequency
print(harmonics)
print(frequencies)


# Remove higher frequencies
# frequencies = frequencies[0:np.where(frequencies>max_frequency)[0][0]]
# frequencies[-1] = max_frequency

# Load data from the experiment
waveforms_directory = 'C:/multisine_collection/'
waveform_name = '2506051636multisine_splitted_quasi-log_100kHz-10mHz_8ptd_ampli_avg_exp_norm_random_phases'
multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
multisine_low_path = waveforms_directory+waveform_name+'/low_band/'
frequencies_experiment = np.array(
    json.load(
        open(multisine_low_path + "waveform_metadata.json")
        )["Frequencies / Hz"]
)
frequencies_experiment = np.append(
    frequencies,
    json.load(open(multisine_high_path + "waveform_metadata.json")
              )["Frequencies / Hz"],
)
frequencies_experiment=frequencies_experiment[0:52]
path_impedance_avarage = 'scripts/250528_extract_ms_amplitude_from_exp/results/impedance_avarage_ca.npy'
impedance_average_cp = np.absolute(np.load(path_impedance_avarage))
# Extract desired amplitude from experiment data
impedance_module = amplitude_extraction_from_experiment(
    impedance_average_cp,
    frequencies_experiment,
    frequencies,
)
amplitudes = np.reciprocal(impedance_module)

show_extracted_amplitude_from_experiment(impedance_average_cp,
                                         frequencies_experiment,
                                         frequencies)

plt.show()

# Splitting into two waveforms

splitting_index = 28 
sampling_frequency_low = 1000

msfirst = Multisine(
    sampling_frequency_low,
    frequencies[0:splitting_index], 
    amplitudes[0:splitting_index], 
)
msfirst.best_random_phases(200)
msfirst.normalize_waveform()
msfirst.compute_crest_factor()
msfirst.plot('voltage')
msfirst.fourier_analysis(6)
msfirst.plot_dft((0.001, sampling_frequency_low//2))

base_frequency = 1 # Regenarate from two decades below the desired
max_frequency = 100000
frequencies_high = harmonics * base_frequency 
frequencies_high = frequencies_high[0:np.where(frequencies_high>max_frequency)[0][0]]
frequencies_high[-1] = max_frequency
# Discard the new decade
frequencies_high = frequencies_high[12:]

# Generate multisine high band
sampling_frequency_high = 1000000
waveform_period = 1
number_of_points_high = int(waveform_period*sampling_frequency_high)
mssecond = Multisine(
    sampling_frequency_high,
    frequencies_high, #frequencies[splitting_index:], 
    amplitudes[splitting_index:],
    # phases[splitting_index:],
    number_points = number_of_points_high,
)
mssecond.best_random_phases(200)
mssecond.normalize_waveform()
mssecond.compute_crest_factor
mssecond.plot('voltage')
mssecond.fourier_analysis(6)
mssecond.plot_dft((1,sampling_frequency_high//2))

plt.show()

# Save waveforms
multisine_basename = '2507261031multisine_splitted_100kHz-10mHz_ca'
msfirst.save('C:/multisine_collection/'+multisine_basename+'/low_band/')
mssecond.save('C:/multisine_collection/'+multisine_basename+'/high_band/')
np.save('C:/multisine_collection/'+multisine_basename+'/total_frequencies.npy', frequencies)