# This is an attempt to duplicate the Single5.exe program from ITRC

import numpy as np
import math

from Scripts import Calculate_Exponent, Calculate_GPM, KinematicViscosity_US, Velocity_fps, ReynoldsNumber
from Scripts import FrictionFactor, DarcyWeisbach, Bernoulli, PipeArea_sqft


# the program will ask the user to enter one of three possible scenarios to solve for
print("You must specify one of the features below.\n"
      "The program will solve for the other hydraulic variables. \n"
      "Only one of these can be set. \n \n \n"
      "For example, if you specify option 1, then you will need \n"
      "to tell the  program what inlet pressure you want. \n"
      "The program will then determine what the pressures and flows \n"
      "will be along the entire hose, given that inlet pressure. \n")
print("1. You know the HOSE INLET PRESSURE; program solves for avg. GPH \n"
      "2. You know the AVG. GPH/EMITTER, program solves for the inlet P \n"
      "3. Pressure and flows for FLUSHING \n")
print("Which one do you want to specify?")

menuOne = int(input())

# the program will ask the user for inputs
if menuOne == 1:
    # todo enter an error handling message for this question
    # the drip tape and drip hose options will affect the solution by how much friction there is
    print("There are two types of drip hose \n"
          "1. Drip tape (thin material with holes every foot or so) \n"
          "2. Drip HOSE with thicker walls and regular emitters \n"
          "Which describes your system (1 or 2) ?")
    tapeHosemenu = int(input())
    if tapeHosemenu == 1:
        try:
            print("Tape inside diameter, inches?")
            diam_inches = float(input())
            divzero = 12 / diam_inches
            divalph = 12 / diam_inches
        except ZeroDivisionError:
            print("The diameter must be greater than zero")
        except TypeError:
            print("Please enter a numerical value")

        try:
            print("Water temperature going into the hose, deg. F?")
            temperature = float(input())
        except TypeError:
            print("Please enter a numerical value")

        print("Hole or emitter spacing, not include snaking% \n")
        print(" ** note** \n"
              "THIS PROGRAM CAN ONLY MAKE COMPUTATIONS FOR UP TO 2000 EMITTERS \n"
              "SO IF YOU HAVE MORE, INPUT A VALUE DOUBLE THE ACTUAL SPACING \n")
        print("WITH TAPE, DO *NOT* CHANGE THE gpm/100'\n"
              "THE COMPUTATIONS WILL THEN WORK OUT OK.")

        print("inches (not feet) = ?")
        spacing = float(input())

        print("Manufacturing coefficient of variation, cv. (a decimal) = ?")
        cv = float(input())

        print("The program needs to know the sensitivity \n"
              "of the flow rate to pressure changes.")
        print("Do you know the emitter discharge exponent? 1 = Yes or 2 = No")
        knowEmitExp = int(input())
        # If the emitter exponent is known; answer to above is "YES"
        if knowEmitExp == 1:
            print("The answer for the next 2 questions come from the\n"
                  "manufacturer's literature \n"
                  "An example of a 'nominal' flow rate is 1.0 GPH for an emitter, or \n"
                  "0.25 GPH/100 feet for a tape. \n"
                  "Your 'desired' average flow rate may be higher or lower \n"
                  "than the 'nominal' flow \n"
                  "Here you are being asked for a flow and pressure from \n"
                  "the manufacturer's literature.")
            print("Nominal flow rate of tape, GPM/100' (Not GPH) = ?")
            nomTapeGPMper100 = float(input())
            print("Pressure of the above nominal flow rate, psi = ?")
            nomTapePr = float(input())
            print("Emitter discharge exponent, x = ?")
            emitExp = float(input())
            GPM_per_emitter = (nomTapeGPMper100 / 100) * (spacing / 12)
            GPH_per_emitter = GPM_per_emitter * 60
            k_factor = GPH_per_emitter / nomTapePr ** emitExp
        else:
            print("You will need to input two emitter flows and two emitter pressures \n"
                  "This information usually comes from the manufacturer's literature. \n \n"
                  "Pressure must be in PSI. \n \n"
                  "Flow must be in GPH (gallons/hour) for a single emitter, \n"
                  "OR ... GPM/100' (not GPH) for tape.")
            print("Highest pressure, psi?")
            emitterPHigh = float(input())
            print("Flow rate at that highest pressure, GPM/100?")
            eQatPHigh = float(input())
            print("Lowest pressure, psi?")
            emitterPLow = float(input())
            print("Flow rate at that lowest pressure, GPM/100?")
            eQatPLow = float(input())
            emitExp = Calculate_Exponent.calc_exp(eQatPLow, eQatPHigh, emitterPLow, emitterPHigh)
            print("Your calculated emitter exponent is " + str(emitExp) + "\n \n")
            k_factor = eQatPHigh / emitterPHigh ** emitExp

        print("Slope of the hose (downhill from inlet is positive), & = ?")
        hoseSlope = float(input())
        # this part asks the user about the length of the hose
        print("The hose length answer for the next question should not include any extra \n"
              "length to account for expansion and contraction (snaking) \n \n"
              "(That extra percentage is handled in the subsequent question) \n \n"
              "There must always be some length of hose upstream of the first emitter. \n \n"
              "Hose length in one direction from the manifold, feet = ?")
        hoseLen = int(input())
        print("What extra percentage (%) of hose length is added for temperature \n"
              "expansion and contraction?")
        snaking = int(input())
        print("What is the DESIRED inlet pressure for the hose,\n"
              "(downstream of fittings such as hose screen washers), PSI =?")
        desiredInletPressure = int(input())

        # the program will now populate the initial bernoulli table
        # the program will first calculate the initial row of values for the table, then it will populate

        # the kinematic viscosity is constant for the calculation - no list required
        mu = KinematicViscosity_US.kinvisc(temperature)

        # the program inputs the variable "desiredInletPressure" as a starting point
        # this value will change when solution is calculated
        point_psi = [desiredInletPressure]

        # area is in square feet
        # this value is constant per hose length - does not require list
        area = PipeArea_sqft.area(diam_inches)

        # percent slope entered is downhill if positive, uphill if negative
        # change in elevation is converted to psi by dividing by 2.31 ft/psi
        # this value is constant per hose length - does not require list
        delta_elevation = ((hoseSlope / 100) * (spacing / 12) / 2.31)

        # the outlet number is the emitter number starting at the most downstream emitter
        # the outlet number is found by dividing total hose length in one direction by the emitter spacing
        index = range(int(math.ceil(hoseLen / (spacing / 12))) - 1)

        outletGPM = []  # defining the start of the outletGPM list
        cumulativeGPM = []  # defining the start of the cumulativeGPM list
        cumulativeLen = []  # defining the start of the cumulativeLen list
        v = []  # defining the start of the v list
        Re = []  # defining the start of the Re list
        f = []  # defining the start of the f list
        friction_psi = []  # defining the start of the friction_psi list

        # this is where the table population happens
        for i in index:
            # the outlet GPM is calculated using the point psi, calculated k-factor and emitter exponent
            # Q = k * p^x

            # calculates outlet GPM for point_psi index i
            outletGPM.append(Calculate_GPM.calc_gpm(k_factor, point_psi[i], emitExp))

            # calculates the cumulative GPM in the hose
            if i == 0:
                cumulativeGPM.append(outletGPM[i])
            else:
                cumulativeGPM.append(cumulativeGPM[i - 1] + outletGPM[i])

            # calculates the cumulative length in hose
            if i == 0:
                cumulativeLen.append(spacing / 12)
            else:
                cumulativeLen.append(cumulativeLen[i - 1] + (spacing / 12))

            # the v of the upstream section is calculated based on the
            # cumulative GPM
            v.append(cumulativeGPM[i] / area)

            # the Reynolds number is calculated
            Re.append(ReynoldsNumber.Re(mu, v[i], diam_inches))

            # the Darcy Friction Factor "f" is calculated
            f.append(FrictionFactor.f(Re[i]))

            # friction is calculated in feet, then converted to psi by dividing by 2.31 ft/psi
            friction_psi.append(DarcyWeisbach.darcy_weisbach(f[i], spacing / 12, v[i], diam_inches / 12) / 2.31)

            # the upstream emitter pressure (psi) is calculated using the Energy "Bernoulli" Equation
            upstream_psi = Bernoulli.bernoulli(point_psi[i], friction_psi[i], delta_elevation)

            # the upstream psi is added to the point_psi list and becomes the next input in the iteration
            point_psi.append(upstream_psi)


        max_psi = np.maximum(point_psi)
        min_psi = np.minimum(point_psi)
        max_pressure_diff = max_psi - min_psi
        total_friction = np.sum(friction_psi)

