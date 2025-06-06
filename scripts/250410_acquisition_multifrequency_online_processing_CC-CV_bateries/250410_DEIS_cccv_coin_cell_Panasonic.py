from pathlib import Path
import json

import numpy as np

from pyeclab import BiologicDevice, ChannelConfig, FileWriter, Channel, BANDWIDTH, E_RANGE, I_RANGE, EXIT_COND, Condition
from pyeclab.techniques import ChronoAmperometry, ChronoPotentiometryWithLimits, OpenCircuitVoltage, Loop, build_limit, generate_xctr_param
from trueformawg import TrueFormAWG, VISAdevices, import_awg_txt
from pypicostreaming import Picoscope5000a
from deistools.processing import MultiFrequencyAnalysis, fermi_dirac_filter, BlockCalculator
from deistools.acquisition import DEISchannel, PicoCalculator, ConditionAverage, MultisineGenerator, MultisineGeneratorCombined


# ===============
# User parameters
# ===============

saving_directory = 'E:/Experimental_data/Federico/2025/method_validation_coins/'
experiment_name = "2506051643_aged_coin_broad_multisine_CCCV_2800-2200_1cyc_stfft_10s_fc_500Hz_optimized_ms_"
saving_path = saving_directory + experiment_name 

# Potentiostat
potentiostat_ip = "172.28.26.10"
eclabsdk_binary_path = "C:/EC-Lab Development Package/EC-Lab Development Package/"
potentiostat_channel = 1
config = ChannelConfig(
    live_plot = True,
    external_control = True,
    record_ece = False,
    record_charge = False,
)

# values for all techniqes
xctr = generate_xctr_param(config)
i_range = I_RANGE.I_RANGE_10mA
e_range = E_RANGE.E_RANGE_5V
bandwidth = BANDWIDTH.BW_9
# chrono-potentiometry charge technique
cpc_current = 0.0045
cpc_duration = 60*60*10
cpc_vs_init = False
cpc_nb_steps = 0
cpc_record_dt = 1
cpc_record_dE = 5
cpc_repeat = 0
cpc_limit_variable = build_limit("Ewe", ">", "or", True)
cpc_limit_value = 4
# chrono-amperometry technique
ca_voltage = 2.8
ca_duration = 60*60*6
ca_vs_init = False
ca_nb_steps = 0
ca_record_dt = 1
ca_record_dI = 1
ca_repeat = 0
# chrono-potentiometry discharge technique
cpd_current = - 0.0045
cpd_duration = 60*60*10
cpd_vs_init = False
cpd_nb_steps = 0
cpd_record_dt = 1
cpd_record_dE = 5
cpd_repeat = 0
cpd_limit_variable = build_limit("Ewe", "<", "or", True)
cpd_limit_value = 0
# ocv between techniques
ocv_duration = 5
ocv_record_dt = 1
# rest ocv technique
rest_duration = 60*5
rest_record_dt = 1
# loop technique
loop_repeat_N = 0 
loop_start = 0
cccv_software_conditions = [
    ConditionAverage(0, 'Ewe', '>', 2.8, 60),
    ConditionAverage(2, 'I', '<', 0.002, 60),
    ConditionAverage(4, 'Ewe', '<', 2.2, 60),
]


# Waveform generator
trueform_address = 'USB0::0x0957::0x4B07::MY59000581::0::INSTR'
waveforms_directory = 'E:/multisine_collection/'
waveform_name = '2506051636multisine_splitted_quasi-log_100kHz-10mHz_8ptd_ampli_avg_exp_norm_random_phases'
multisine_high_path = waveforms_directory+waveform_name+'/high_band/'
multisine_high_name = 'ms_high'
multisine_low_path = waveforms_directory+waveform_name+'/low_band/'
multisine_low_name = 'ms_low'
amplitude_galvano = 1.5
amplitude_potentio = 0.1


# Digital oscilloscope
pico_samples_total = 500000000
pico_capture_size = pico_samples_total
pico_sampling_time = 1
pico_sampling_time_scale = 'PS5000A_US'
pico_bandwidth_chA = 'PS5000A_5V'
pico_bandwidth_chB = 'PS5000A_2V'
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
              )["Frequencies / Hz"]
)
frequencies_ffteis = np.array(frequencies[28:])
sampling_time = 1e-6
time_window = 10

# Decimation
filter_cutoff = 90
filter_order = 25
time_experiment = 60*60*12
sampling_frequency = 1e6
resampling_frequency = 500
ds_factor = int(sampling_frequency / resampling_frequency)
buffer_size = int(time_experiment * resampling_frequency)


# ==========================
# Initialize devices objects
# ==========================

# Initialize potentiostat
device = BiologicDevice(potentiostat_ip, binary_path=eclabsdk_binary_path)
cpc = ChronoPotentiometryWithLimits(
    device=device,
    current=cpc_current,
    duration=cpc_duration,
    vs_init=cpc_vs_init,
    nb_steps=cpc_nb_steps,
    record_dt=cpc_record_dt,
    record_dE=cpc_record_dE,
    repeat=cpc_repeat,
    i_range=i_range,
    e_range=e_range,
    bandwidth=bandwidth,
    exit_cond=EXIT_COND.NEXT_TECHNIQUE,
    limit_variable=cpc_limit_variable,
    limit_value= cpc_limit_value,
    xctr = xctr,
)
cpc.make_technique()
ca = ChronoAmperometry(
    device=device,
    voltage=ca_voltage,
    duration=ca_duration,
    vs_init=ca_vs_init,
    nb_steps=ca_nb_steps,
    record_dt=ca_record_dt,
    record_dI=ca_record_dI,
    repeat=ca_repeat,
    e_range=e_range,
    i_range=i_range,
    bandwidth=bandwidth,
    xctr = xctr,
)
ca.make_technique()
cpd = ChronoPotentiometryWithLimits(
    device=device,
    current=cpd_current,
    duration=cpd_duration,
    vs_init=cpd_vs_init,
    nb_steps=cpd_nb_steps,
    record_dt=cpd_record_dt,
    record_dE=cpd_record_dE,
    repeat=cpd_repeat,
    i_range=i_range,
    e_range=e_range,
    bandwidth=bandwidth,
    exit_cond=EXIT_COND.NEXT_TECHNIQUE,
    limit_variable=cpd_limit_variable,
    limit_value= cpd_limit_value,
    xctr = xctr,
)
cpd.make_technique()
ocv = OpenCircuitVoltage(
    device=device,
    duration= ocv_duration,
    record_dt=ocv_record_dt,
    e_range=e_range,
    bandwidth=bandwidth,
)
ocv.make_technique()
rest = OpenCircuitVoltage(
    device = device,
    duration = rest_duration,
    record_dt = rest_record_dt,
    e_range = e_range,
    bandwidth = bandwidth,
)
rest.make_technique()
loop = Loop(
    device=device, 
    repeat_N=loop_repeat_N, 
    loop_start=loop_start,
)
loop.make_technique()
sequence = [
    cpc,
    ocv,
    ca,
    rest,
    cpd,
    rest,
    loop,
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
awg_ch1.set_offset(0)
awg_ch2.set_offset(0)
sample_rate_multisine_high = json.load(open(multisine_high_path + "waveform_metadata.json"))["Sample frequency / Hz"]
sample_rate_multisine_low = json.load(open(multisine_low_path + "waveform_metadata.json"))["Sample frequency / Hz"]
awg_ch1.set_sample_rate(sample_rate_multisine_high)
awg_ch2.set_sample_rate(sample_rate_multisine_low)
multisine_gen_high = MultisineGenerator(
    awg_ch1, 
    [0, 2, 4], 
    ['ms_high'] * 3, 
    [sample_rate_multisine_high] * 3, 
    [amplitude_galvano, amplitude_potentio, amplitude_galvano],
)
multisine_gen_low = MultisineGenerator(
    awg_ch2, 
    [0, 2, 4], 
    ['ms_low'] * 3, 
    [sample_rate_multisine_low] * 3, 
    [amplitude_galvano, amplitude_potentio, amplitude_galvano],
)
multisine_gen = MultisineGeneratorCombined(
    multisine_gen_high,
    multisine_gen_low,
)


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
    frequencies_ffteis, 
    np.zeros(block_size),
    np.zeros(block_size),
    sampling_time,
)
high_z_calculator.compute_freq_axis()

# Initialize the bock calculator
fermi_dirac_low_pass = fermi_dirac_filter(
    high_z_calculator.freq_axis, 
    0, 
    filter_cutoff, 
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
    awg = multisine_gen,
)
deischannel.conditions.extend(cccv_software_conditions)

# =====================
# Start the measurement
# =====================

deischannel.start()