import numpy as np
import matplotlib.pyplot as plt
from deistools.processing.data_loader import load_pyeclab_data

data = load_pyeclab_data()

print(data.head())

plt.figure()
plt.plot(data['Time/s'],data['I/A']*1000)
plt.show()