from multisine import Multisine, compute_crest_factor, compute_crest_factor
import numpy as np
import matplotlib.pyplot as plt

harmonics = np.loadtxt('scripts/250512_multisine_design/data/harmonics_7decs_no_intermod_second_8ptsdec.txt')
base_frequency = 0.01
max_frequency = 100000
frequencies = harmonics * base_frequency

# Remove higher frequencies
# frequencies = frequencies[0:np.where(frequencies>max_frequency)[0][0]]
# frequencies[-1] = max_frequency

splitting_index = 28 # 100 Hz

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15,3),sharex=True, gridspec_kw={'hspace': 0})

ax1.vlines(frequencies, 0 , 1, )

# Regenerate from 100 Hz
base_frequency = 100 
max_frequency = 100000
frequencies_high = harmonics * base_frequency 
frequencies_high = frequencies_high[0:np.where(frequencies_high>max_frequency)[0][0]]
frequencies_high[-1] = max_frequency

ax2.vlines(frequencies_high, 0 , 1, color = 'orange')
ax2.vlines(frequencies[0:splitting_index], 0 , 1)
ax2.vlines(frequencies[splitting_index:], 0 , 1, color= 'gray', alpha = 0.3)

# Regenerate from 10 Hz
base_frequency = 10 
max_frequency = 100000
frequencies_high = harmonics * base_frequency 
frequencies_high = frequencies_high[0:np.where(frequencies_high>max_frequency)[0][0]]
frequencies_high[-1] = max_frequency
# Discard one decade
frequencies_high = frequencies_high[4:]

ax3.vlines(frequencies_high, 0 , 1, color = 'orange')
ax3.vlines(frequencies[0:splitting_index], 0 , 1)
ax3.vlines(frequencies[splitting_index:], 0 , 1, color= 'gray', alpha = 0.3)

# Regenerate from 1 Hz
base_frequency = 1 
max_frequency = 100000
frequencies_high = harmonics * base_frequency 
frequencies_high = frequencies_high[0:np.where(frequencies_high>max_frequency)[0][0]]
frequencies_high[-1] = max_frequency
# Discard the new decade
frequencies_high = frequencies_high[12:]

ax4.vlines(frequencies_high, 0 , 1, color = 'orange')
ax4.vlines(frequencies[0:splitting_index], 0 , 1)
ax4.vlines(frequencies[splitting_index:], 0 , 1, color= 'gray', alpha = 0.3)

# Set all plots to log scale
ax1.set_xscale('log')
ax2.set_xscale('log')
ax3.set_xscale('log')
ax4.set_xscale('log')

# Hide y-axis labels and ticks
ax1.set_yticks([])
ax1.set_yticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])
ax3.set_yticks([])
ax3.set_yticklabels([])
ax4.set_yticks([])
ax4.set_yticklabels([])
ax1.set_ylim(0, 1) 
ax2.set_ylim(0, 1)
ax3.set_ylim(0, 1)
ax4.set_ylim(0, 1)

# Add tites
ax1.set_title('Comparison between single harmonic sequence and two summed sequences.')
ax1.set_ylabel('Quasi-log harmonic sequence', labelpad=10, rotation=0, ha='right', va='center')
ax2.set_ylabel('Restart harmonic seires from 100 Hz', labelpad=10, rotation=0, ha='right', va='center')
ax3.set_ylabel('Restart harmonic seires from 10 Hz', labelpad=10, rotation=0, ha='right', va='center')
ax4.set_ylabel('Restart harmonic seires from 1 Hz', labelpad=10, rotation=0, ha='right', va='center')



plt.tight_layout()
plt.show()
