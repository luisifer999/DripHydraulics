import numpy as np

# This function calculates kinematic viscosity in Imperial units (ft^2/s*10^-5)
def kinvisc(deg_fahrenheit):


    tempF_x = [32.02, 34, 39.2, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
    muImperial_y = [1.9287, 1.8579, 1.6906, 1.6668, 1.4063, 1.2075, 1.0503, 0.925, 0.8234, 0.7392, 0.6682, 0.6075,
                    0.5551]
    return np.interp(deg_fahrenheit, tempF_x, muImperial_y) * 10 ** -5