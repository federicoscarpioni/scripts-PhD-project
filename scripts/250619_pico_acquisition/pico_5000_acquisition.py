import numpy as np
from pypicostreaming import Picoscope5000a

# ===============
# User parameters
# ===============

saving_directory = 'E:/Experimental_data/Federico/2025/test_metadata_saving/'
experiment_name = "2506191118_pico_acquisition"
pico_samples_total = 10
pico_capture_size = pico_samples_total
pico_sampling_time = 1
pico_sampling_time_scale = 'PS5000A_MS'
pico_bandwidth_chA = 'PS5000A_5V'
pico_bandwidth_chB = 'PS5000A_1V'
pico_current_conversion_factor = 0.01


# ==========================
# Initialize devices objects
# ==========================

pico = Picoscope5000a('PS5000A_DR_14BIT')
pico.set_pico(
    pico_capture_size, 
    pico_samples_total, 
    pico_sampling_time, 
    pico_sampling_time_scale, 
    saving_directory + experiment_name,
)
pico.set_channel(
    'PS5000A_CHANNEL_A', 
    pico_bandwidth_chA,
)
pico.set_channel(
    'PS5000A_CHANNEL_B', 
    pico_bandwidth_chB, 
    pico_current_conversion_factor,
)

# =====================
# Start the measurement
# =====================

pico.run_streaming_blocking(autoStop=True)


# ===================================================
# Save oscilloscope acquisition and close connections
# ===================================================

voltage, current = pico.get_all_signals()
np.save(pico.saving_dir+'/voltage.npy', voltage)
np.save(pico.saving_dir+'/current.npy', current)
pico.disconnect()