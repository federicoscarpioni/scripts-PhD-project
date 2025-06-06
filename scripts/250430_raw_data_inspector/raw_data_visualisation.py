import numpy as np
from deistools.processing.data_loader import load_voltage_current
from deistools.visualise.raw_data import plot_technique

sampling_time = 2e-3

voltage, current, _ = load_voltage_current()

time = np.arange(0, voltage.size * sampling_time, sampling_time)

fig, axs = plot_technique(voltage, current, time)