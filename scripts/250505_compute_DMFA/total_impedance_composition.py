import numpy as np
from deistools.processing.data_loader import load_impedance_set

high_frequency_band_filename = load_impedance_set('Select high frequency impedance file')

high_frequency_band = np.load(high_frequency_band_filename)

low_frequency_band_filename = load_impedance_set('Select low frequency impedance file')

low_frequency_band = np.load(high_frequency_band)

total_frequency = np.append(
    low_frequency_band,
    high_frequency_band,
)