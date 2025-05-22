from pathlib import Path
import json

import numpy as np

from pyeclab import BiologicDevice, ChannelConfig, FileWriter, Channel, BANDWIDTH, E_RANGE, I_RANGE
from pyeclab.techniques import ChronoAmperometry, generate_xctr_param
from trueformawg import TrueFormAWG,  import_awg_txt
from pypicostreaming import Picoscope5000a

import matplotlib

# ===============
# User parameters
# ===============

saving_directory = 'E:/Experimental_data/Federico/2025/method_validation_coins/'
experiment_name = "2505151509_aged_coin_multisine_ca0V_400s_pico_acq"
saving_path = saving_directory + experiment_name

# Potentiostat
potentiostat_ip = "172.28.26.10"
eclabsdk_binary_path = "C:/EC-Lab Development Package/EC-Lab Development Package/"
potentiostat_channel = 1
config = ChannelConfig(
    live_plot=False,
    external_control=True,
    record_ece = False,
    record_charge = False,
)

# chrono-potentiometry technique
voltage = 0
duration = 402
vs_init = True
nb_steps = 0
record_dt = 1
record_dI = 1
repeat = 0
i_range = I_RANGE.I_RANGE_10mA
e_range = E_RANGE.E_RANGE_5V
bandwidth = BANDWIDTH.BW_9

# Waveform generator
trueform_address = 'USB0::0x0957::0x4B07::MY59000581::0::INSTR'
waveforms_directory = 'E:/multisine_collection/'
waveform_name = '2505151210multisine_splitted_quasi-log_100kHz-10mHz_8ptd_flat_norm_random_phases'
multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
multisine_high_name = 'ms_high'
multisine_low_path = waveforms_directory+waveform_name+'/low_band/'
multisine_low_name = 'ms_low'


# Digital oscilloscope
pico_samples_total = 100000000
pico_capture_size = pico_samples_total
pico_sampling_time = 1
pico_sampling_time_scale = 'PS5000A_US'
pico_bandwidth_chA = 'PS5000A_5V'
pico_bandwidth_chB = 'PS5000A_1V'
pico_current_conversion_factor = 0.01

# ==========================
# Initialize devices objects
# ==========================

# Initialize potentiostat
device = BiologicDevice(potentiostat_ip, binary_path=eclabsdk_binary_path)
ca = ChronoAmperometry(
    device=device,
    voltage=voltage,
    duration=duration,
    vs_init=vs_init,
    nb_steps=nb_steps,
    record_dt=record_dt,
    record_dI=record_dI,
    repeat=repeat,
    i_range=i_range,
    e_range=e_range,
    bandwidth=bandwidth,
    xctr = generate_xctr_param(config),
)
ca.make_technique()
sequence = [
    ca,
]
writer = FileWriter(
    file_dir=Path(saving_directory),
    experiment_name=experiment_name,
)
channel1 = Channel(
    device,
    potentiostat_channel,
    writer=writer,
    config=config,
)
channel1.load_sequence(sequence)

# Initialize AWG
awg_ch1 = TrueFormAWG(trueform_address, 1)
awg_ch1.clear_ch_mem()
multisine_high = import_awg_txt(multisine_high_path + "waveform.txt")
awg_ch1.load_awf(multisine_high_name, multisine_high) 
awg_ch2 = TrueFormAWG(trueform_address, 2)
awg_ch2.clear_ch_mem()
multisine_low = import_awg_txt(multisine_low_path + "waveform.txt")
awg_ch2.load_awf(multisine_low_name, multisine_low) 
awg_ch2.avalable_memory()
awg_ch1.select_awf(multisine_high_name)
awg_ch2.select_awf(multisine_low_name)
sample_rate_multisine_high = json.load(open(multisine_high_path + "waveform_metadata.json"))["Generation frequency / Hz"]
sample_rate_multisine_low = json.load(open(multisine_low_path + "waveform_metadata.json"))["Generation frequency / Hz"]
awg_ch1.set_sample_rate(sample_rate_multisine_high)
awg_ch2.set_sample_rate(sample_rate_multisine_low)
awg_ch1.set_Z_out_infinite()
awg_ch2.set_Z_out_infinite()
awg_ch1.combine_channels()

# Initialize oscilloscope
pico = Picoscope5000a('PS5000A_DR_14BIT')
pico.set_pico(
    pico_capture_size, 
    pico_samples_total, 
    pico_sampling_time, 
    pico_sampling_time_scale, 
    saving_path,
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

awg_ch1.turn_on()
channel1.start()
pico.run_streaming_non_blocking(autoStop=True)

channel1.run_thread.join()
awg_ch1.turn_off()

# ===================================================
# Save oscilloscope acquisition and close connections
# ===================================================

voltage, current = pico.get_all_signals()
np.save(pico.saving_dir+'/voltage.npy', voltage)
np.save(pico.saving_dir+'/current.npy', current)
pico.disconnect()
device.disconnect()
