from pathlib import Path
from pyeclab import BiologicDevice, ChannelConfig, FileWriter, Channel, BANDWIDTH, E_RANGE, I_RANGE, EXIT_COND, Condition
from pyeclab.techniques import ChronoPotentiometryWithLimits, build_limit

# ===============
# User parameters
# ===============

saving_directory = 'E:/Experimental_data/Federico/2025/python_software_test/'
experiment_name = "2505061907_aged_coin_discharge"
saving_path = saving_directory + experiment_name 

# Potentiostat
potentiostat_ip = "172.28.26.10"
eclabsdk_binary_path = "C:/EC-Lab Development Package/EC-Lab Development Package/"
potentiostat_channel = 1
# values for all techniqes
i_range=I_RANGE.I_RANGE_10mA
e_range=E_RANGE.E_RANGE_5V
bandwidth=BANDWIDTH.BW_9
# chrono-potentiometry 
cp_current = - 0.0045
cp_duration=200
cp_vs_init=False
cp_nb_steps=0
cp_record_dt=1
cp_record_dE=5
cp_repeat=0
cp_limit_variable = build_limit("Ewe", "<", "or", True)
cp_limit_value = 2.5

# ==========================
# Initialize devices objects
# ==========================

# Initialize potentiostat
device = BiologicDevice(potentiostat_ip, binary_path=eclabsdk_binary_path)
cp = ChronoPotentiometryWithLimits(
    device=device,
    current=cp_current,
    duration=cp_duration,
    vs_init=cp_vs_init,
    nb_steps=cp_nb_steps,
    record_dt=cp_record_dt,
    record_dE=cp_record_dE,
    repeat=cp_repeat,
    i_range=i_range,
    e_range=e_range,
    bandwidth=bandwidth,
    exit_cond=EXIT_COND.NEXT_TECHNIQUE,
    limit_variable=cp_limit_variable,
    limit_value= cp_limit_value,
)
cp.make_technique()
sequence = [cp]
writer = FileWriter(
    file_dir=Path(saving_directory),
    experiment_name=experiment_name,
)
channel1 = Channel(
    device,
    potentiostat_channel,
    writer=writer,
    config=ChannelConfig(live_plot=True),
)
channel1.load_sequence(sequence)

channel1.start()

