# friction factor calculated from Reynolds Number
def f(reynolds_number):
    if reynolds_number < 2000:
        return 64 * reynolds_number ** -1
    else:
        return 0.0056 + 0.5 * reynolds_number ** (-0.32)