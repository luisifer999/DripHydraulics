# this function calculates the flow rate in the Bernoulli Table
def calc_gpm(kfactor, psi, emitterexponent):
    return kfactor * psi ** emitterexponent
