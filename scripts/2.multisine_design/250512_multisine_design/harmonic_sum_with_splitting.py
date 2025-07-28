from multisine import Multisine
import numpy as np
import matplotlib.pyplot as plt

harmonics = np.loadtxt('scripts/250512_multisine_design/data/harmonics_8dec_quasi-log-8pts_no_intermod_second.txt')
base_frequency = 0.01
max_frequency = 100000
frequencies = harmonics * base_frequency

# Remove higher frequencies
frequencies = frequencies[0:np.where(frequencies>max_frequency)[0][0]]
frequencies[-1] = max_frequency

# # Generating the complete multisine to perform first the phase minimization
path_impedance_avarage = 'E:/Experimental_data/Federico/2025/method_validation_coins/2505270932_aged_coin_broad_multiine_CCCV_2800-2200_1cyc_stfft_10s_fc_500Hz_more_rest_time/pico_aquisition/cycle_0_sequence_0/impedance_avarage.npy'
amplitudes = np.absolute(np.load(path_impedance_avarage))
# amplitudes = np.ones(frequencies.size)  # V
sampling_frequency = 250000
# ms = Multisine(
#     sampling_frequency, 
#     frequencies, 
#     amplitudes,
# )
# ms.best_random_phases(5)
# ms.normalize_waveform()
# ms.plot('voltage')
# ms.fourier_analysis(5)
# ms.plot_dft((0.001,sampling_frequency//2))
# ms.plot_phase((0.001,sampling_frequency//2))


# Splitting into two waveforms

splitting_index = 28 
# phases = ms.phases

sampling_frequency_low = 1000

msfirst = Multisine(
    sampling_frequency_low,
    frequencies[0:splitting_index], 
    amplitudes[0:splitting_index], 
)
msfirst.best_random_phases(200)
msfirst.normalize_waveform()
msfirst.plot('voltage')
msfirst.fourier_analysis(6)
msfirst.plot_dft((0.001, sampling_frequency_low//2))

base_frequency = 1 # Regenarate from one decade below the desired
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
mssecond.plot('voltage')
mssecond.fourier_analysis(6)
mssecond.plot_dft((1,sampling_frequency_high//2))

plt.show()

# Save waveforms
multisine_basename = '2506051636multisine_splitted_quasi-log_100kHz-10mHz_8ptd_ampli_avg_exp_norm_random_phases'
msfirst.save('C:/multisine_collection/'+multisine_basename+'/low_band/')
mssecond.save('C:/multisine_collection/'+multisine_basename+'/high_band/')
