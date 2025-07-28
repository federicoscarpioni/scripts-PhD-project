from multisine import Multisine, compute_crest_factor, compute_crest_factor
import numpy as np

harmonics = np.loadtxt('scripts/2_multisine_design/generate_harmonics/harmonic_series/harmonics_7decs_no_intermod_second_8ptsdec.txt')
base_frequency = 10
max_frequency = 100000
frequencies = harmonics * base_frequency

amplitudes = np.ones(frequencies.size)*1  # V
sampling_frequency = 250000
ms1 = Multisine(sampling_frequency, frequencies, amplitudes,)
# ms1.best_random_phases(10)
ms1.normalize_waveform()#int(2**16 /2 - 1))
ms1.plot('voltage')
ms1.fourier_analysis(5)
ms1.plot_dft((0.001,sampling_frequency//2))
ms1.plot_phase((0.001,sampling_frequency//2))
# ms1.save('/multisine_collection/')