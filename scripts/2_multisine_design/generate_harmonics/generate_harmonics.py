import numpy as np
# from scripts.2_multisine_design.generate_harmonics.functions import multi_ac_design, multi_ac_interferelinear
import matplotlib.pyplot as plt

import importlib
module_path = 'scripts/2_multisine_design/generate_harmonics/functions.py'
loader = importlib.machinery.SourceFileLoader('functions',module_path)
funlm = loader.load_module()

# Part 1: Create the frequency vector f
harmonics = np.floor(np.logspace(0, 7, 57))
# Remove duplicates
harmonics = np.unique(harmonics)
# Remove or move harmonics that cause intermodulation
harmonics_no_inter = funlm.multi_ac_design(
    harmonics, 
    5, 
    20, 
    funlm.multi_ac_interferelinear, 
    0, 
    0.01
)

plt.figure(1)
plt.stem(harmonics, np.ones(harmonics.size)+0.5, label='Original')
plt.stem(harmonics_no_inter, np.ones(harmonics_no_inter.size),'orange',label='No intermod')
plt.xscale('log')
plt.legend()
plt.show()

saving_path = 'scripts/2_multisine_design/generate_harmonics/harmonic_series/'
np.savetxt(saving_path+'harmonics_no_int.txt', harmonics_no_inter, fmt = '%d')