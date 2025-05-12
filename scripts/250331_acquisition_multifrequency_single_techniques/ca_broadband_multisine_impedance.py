from pathlib import Path
import json

import numpy as np

from pyeclab import BiologicDevice, ChannelConfig, FileWriter, Channel, BANDWIDTH, E_RANGE, I_RANGE
from pyeclab.techniques import ChronoAmperometry, generate_xctr_param
from trueformawg import TrueFormAWG, import_awg_txt
from pypicostreaming import Picoscope5000a
from deistools.processing import MultiFrequencyAnalysis, fermi_dirac_filter, BlockCalculator
from deistools.acquisition import DEISchannel, PicoCalculator


# ===============
# User parameters
# ===============

saving_directory = 'E:/Experimental_data/Federico/2025/method_validation_coins/'
experiment_name = "2505051605_aged_coin_broadband-multisine_ca"
saving_path = saving_directory + experiment_name

# Potentiostat
potentiostat_ip = "172.28.26.10"
eclabsdk_binary_path = "C:/EC-Lab Development Package/EC-Lab Development Package/"
potentiostat_channel = 1
config = ChannelConfig(
    live_plot=True,
    external_control=True,
    record_ece = False,
    record_charge = False,
)

# chrono-amperometry technique
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
multisine_high_path = 'E:/multisine_collection/2412111607multisine_splitted_100kHz-10mHz_8ptd_fgen1MHz_flat_norm_random_phases/low_freqs/'
multisine_high_name = 'ms_high'
sample_rate_multisine_high = 1000000
multisine_low_path = 'E:/multisine_collection/2412111607multisine_splitted_100kHz-10mHz_8ptd_fgen1MHz_flat_norm_random_phases/high_freqs/'
multisine_low_name = 'ms_low'
sample_rate_multisine_low = 10000
multisine_amplitude = 0.1


# Digital oscilloscope
pico_samples_total = 300000000
pico_capture_size = pico_samples_total
pico_sampling_time = 1
pico_sampling_time_scale = 'PS5000A_US'
pico_bandwidth_chA = 'PS5000A_5V'
pico_bandwidth_chB = 'PS5000A_500MV'
pico_current_conversion_factor = 0.01


# Online calculation
frequencies = np.array(
    json.load(
        open(multisine_low_path + "waveform_metadata.json")
        )["Frequencies / Hz"]
)
frequencies = np.append(
    frequencies,
    json.load(open(multisine_high_path + "waveform_metadata.json")
              )["Frequencies / Hz"],
)
frequencies = frequencies[20:]
sampling_time = 1e-6
time_window = 100

# Decimation
filter_cutoff = 80
filter_order = 8
time_experiment = 400
sampling_frequency = 1e6
resampling_frequency = 500
ds_factor = int(sampling_frequency / resampling_frequency)
buffer_size = int(time_experiment * resampling_frequency)


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
    e_range=e_range,
    i_range=i_range,
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
awg_ch1.set_amplitude(multisine_amplitude)
awg_ch2.set_amplitude(multisine_amplitude)
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

# Initialize the method for multi-frequency analysis
block_size =  int(time_window / sampling_time)
high_z_calculator = MultiFrequencyAnalysis(
    frequencies, 
    np.zeros(block_size),
    np.zeros(block_size),
    sampling_time,
)
high_z_calculator.compute_freq_axis()

# Initialize the bock calculator
fermi_dirac_low_pass = fermi_dirac_filter(
    high_z_calculator.freq_axis, 
    0, 
    2 * filter_cutoff, 
    filter_order
   )
block_calculator = BlockCalculator(
    input_size = block_size,
    sampling_time = sampling_time,
    high_z_calculator = high_z_calculator,
    lp_filter = fermi_dirac_low_pass,
    ds_factor = ds_factor,
    buffer_size =buffer_size,
)

# Inject block calculator into PicoCalculator

pico_calculator = PicoCalculator(
    pico = pico,
    block_calculator= block_calculator,
)

# Inject instrument object into DEISchannel object
deischannel = DEISchannel(
    potentiostat = channel1,
    pico = pico_calculator,
)

# =====================
# Start the measurement
# =====================

awg_ch1.turn_on()
deischannel.start()
