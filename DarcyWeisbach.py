# pipe section friction calculated using the Darcy-Weisbach Equation
# returns friction in psi
def darcy_weisbach(frictionfactor, length, pipediam, velocity):
    return (frictionfactor * (length * velocity ** 2 / 2 / (pipediam / 12) / 32.2)) / 2.31