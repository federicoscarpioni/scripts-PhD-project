import numpy as np
from deistools.processing.data_loader import load_voltage_current
from deistools.visualise.raw_data import plot_technique

sampling_time = 2e-3
multisine_period = 100

voltage, current, _ = load_voltage_current()

assert voltage.size == current.size , 'Volage and current have different sizes.'

signal_duration = voltage.size * sampling_time

print(f'Signal size is {voltage.size} Sa, total duration is {signal_duration} s and number of period {int(signal_duration / multisine_period)}')

assert signal_duration % multisine_period == 0 , 'Signals contains a non integer ammount of periods.'