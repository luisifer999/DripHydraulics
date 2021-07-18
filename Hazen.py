#This program calculates the headloss in a pipe

import numpy as np

def Hazen(pipe_length, cfactor, pipe_diam, gpm):
    PipeArea = (np.pi * pipe_diam ** 2) / 4

    return 10.5 * (gpm / cfactor) ** (1.85) * pipe_length * pipe_diam ** (-4.87)

