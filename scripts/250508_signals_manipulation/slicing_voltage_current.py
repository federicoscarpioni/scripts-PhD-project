import numpy as np
import os
from deistools.processing.data_loader import load_voltage_current

# ===============
# User parameters
# ===============

sampling_time = 1e-6
starting_time_s = 0
ending_time_s = 1

# ==========
# Main code
# ==========

# Convert to array indexes
starting_time_index = int(starting_time_s / sampling_time)
ending_time_index = int(ending_time_s / sampling_time)

voltage, current, dir = load_voltage_current()

time = np.arange(0, voltage.size * sampling_time, sampling_time)

subfolder_name = f'/sliced_signals_{ending_time_s-starting_time_s}_s_start_{starting_time_s}_s'
os.makedirs(dir+subfolder_name)
np.save(dir+subfolder_name+'/voltage.npy', voltage[starting_time_index:ending_time_index])
np.save(dir+subfolder_name+'/current.npy', current[starting_time_index:ending_time_index])