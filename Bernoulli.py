# this is the Energy or Bernoullie Equation solving for upstream pressure
# P u/s = P d/s + Hf + (E d/s - E u/s)
# the term (E d/s - E u/s) is negative (-) when slope is going downhill
# the user slope input assumes downhill slope is positive
# the equation will subtract the change in elevation as a default
def bernoulli(pressure_ds, friction, change_in_elevation):
    return pressure_ds + friction - change_in_elevation