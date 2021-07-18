# Here, I will define the function for calculating the emitter discharge exponent
import numpy as np


def calc_exp(flow_rate_at_low_pressure, flow_rate_at_high_pressure, low_pressure, high_pressure):
    return np.log(flow_rate_at_low_pressure / flow_rate_at_high_pressure) / np.log(low_pressure / high_pressure)
