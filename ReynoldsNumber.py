# this function calculates the Reynolds Number
def Re(kinematic_viscosity, velocity, pipediam):
    return velocity * (pipediam / 12) / kinematic_viscosity

