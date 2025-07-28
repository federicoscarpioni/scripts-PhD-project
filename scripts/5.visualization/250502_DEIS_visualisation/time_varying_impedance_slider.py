from deistools.processing.data_loader import load_impedance_set
from deistools.visualise import plot_impedance_set

imp, _ = load_impedance_set()

plot_impedance_set(imp)