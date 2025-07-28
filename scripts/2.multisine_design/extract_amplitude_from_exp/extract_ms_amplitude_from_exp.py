import numpy as np
import matplotlib.pyplot as plt
from deistools.processing.data_loader import load_impedance_set

imp, directory = load_impedance_set()

imp_avarage = np.mean(imp, axis=1)

plt.plot(imp_avarage.real, -imp_avarage.imag, '-o')
plt.axis('equal')
plt.title('Avarage impedance')
plt.show()

np.save(directory+'/impedance_avarage.npy', imp_avarage)