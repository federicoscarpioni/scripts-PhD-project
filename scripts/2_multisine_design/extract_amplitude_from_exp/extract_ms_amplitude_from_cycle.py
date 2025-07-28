import numpy as np
import matplotlib.pyplot as plt
from deistools.processing.data_loader import load_impedance_set

imp_charge_cp, _ = load_impedance_set('Select deis charge CP')
imp_ca, _ = load_impedance_set('Select deis charge CA')
imp_discharge, _ = load_impedance_set('Select deis discharge')

imp_cp = np.concatenate((imp_charge_cp, imp_discharge), axis=1)

imp_cp_avarage = np.mean(imp_cp, axis=1)
imp_ca_avarage = np.mean(imp_ca, axis=1)

plt.plot(imp_cp_avarage.real, -imp_cp_avarage.imag, '-o', label = 'CP')
plt.plot(imp_ca_avarage.real, -imp_ca_avarage.imag, '-o', label = 'CA')
plt.axis('equal')
plt.title('Avarage impedance')
plt.legend()
plt.show()

np.save('scripts/250528_extract_ms_amplitude_from_exp/results'+'/impedance_avarage_cp.npy', imp_cp_avarage)
np.save('scripts/250528_extract_ms_amplitude_from_exp/results'+'/impedance_avarage_ca.npy', imp_ca_avarage)