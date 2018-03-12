from ggrocket import Rocket, Planet
from math import radians, sqrt, log
from ggmath import InputButton, Timer, Label, Slider

earth = Planet(planetmass=0)  # no gravity to simplify things

Stage1Started = False
Stage2Started = False
PayloadLaunched = False
StartTime = None    # to keep track of when burn started
BurnTime = 0        # keep track of how much time the burn has lasted

# Falcon F9R specifications
# FIRST STAGE
me1 = 25600          # Empty mass (kg) 
mp1 =  395700        # Propellent mass (kg)
Ftotal1 = 6.444E6    # Total thrust (Newtons)
tburn1 = 180         # Burn time (seconds)
# SECOND STAGE
me2 = 3900           # Empty mass (kg)
mp2 =  92670         # Propellent mass (kg)
Ftotal2 = 8.01E5     # Total thrust (Newtons)
tburn2 = 372         # Burn time (seconds)
# PAYLOAD
mep = 13150          # Payload mass (kg)


# Predict the final velocity using Tsiolkovsky's Rocket Equation,
# In two stages!
vmax1 = Ftotal1*tburn1/mp1*log((me1+mp1+me2+mp2+mep)/(me1+me2+mp2+mep))
vmax2 = Ftotal2*tburn2/mp2*log((me2+mp2+mep)/(me2+mep))

print("Predicted final staged rocket velocity (Rocket Equation), vmax: ", vmax1+vmax2, " m/s")

# Create a function for determining the rocket thrust
def GetThrust():
    global StartTime
    global BurnTime
    global Stage1Started
    global Stage2Started
    global PayloadLaunched
    if Stage1Started:
        tburn = tburn1
        Ftotal = Ftotal1
    elif Stage2Started:
        tburn = tburn2
        Ftotal = Ftotal2
    if Stage1Started or Stage2Started:
        # get the burn time: seconds since start
        BurnTime = rocket.shiptime - StartTime
        # is it time to stop this stage?
        if BurnTime >= tburn:
            if Stage1Started:
                # stage the rocket
                Stage1Started = False
                Stage2Started = True
                # Note the new starting time
                StartTime = rocket.shiptime
                return Ftotal2
            else:
                # stop the rocket
                Stage2Started = False
                PayloadLaunched = True
                return 0
        else:
            # still burning, report full thrust
            return Ftotal
    else:
        return 0

# Function for starting the rocket thrust (called by the START "button")
def StartRocket():
    global Stage1Started
    global StartTime
    if not (Stage1Started or Stage2Started):
        Stage1Started = True
        # Note the starting time
        StartTime = rocket.shiptime
        
# Function for calculating the total rocket mass, based on burn time and total
# propellent mass.
def GetMass():
    global Stage1Started
    global Stage2Started
    global PayloadLaunched
    if Stage1Started:
        # calculate empty mass plus a fraction of the propellent mass based on time
        return me1 + me2 + mep + mp2 + mp1*(tburn1-BurnTime)/tburn1
    elif Stage2Started:
        return me2 + mep + mp2*(tburn2-BurnTime)/tburn2
    elif PayloadLaunched:
        # just payload mass now
        return mep
    else:
        # not even started: just return the full pre-launch rocket mass
        return me1 + mp1 + me2 + mp2 + mep

# Function for displaying the rocket status
def GetStatus():
    global Stage1Started
    global Stage2Started
    global PayloadLaunched
    if Stage1Started:
        return "STAGE 1 FIRING"
    elif Stage2Started:
        return "STAGE 2 FIRING"
    elif PayloadLaunched:
        return "PAYLOAD DELIVERED"
    else:
        return "WAITING FOR LAUNCH"

# Create a button for starting the simulation
# Physical positioning at 10,400 pixels, calls the StartRocket function
start = InputButton((10,400), "START", StartRocket, positioning="physical", size=15)

# Create a label for showing the current rocket status
status = Label((10,420), GetStatus, positioning="physical", size=15)

# Add a slider for conrolling the timezoom
tz = Slider((10,360), 0, 5, 0, positioning="physical")

#Create and "run" the rocket
rocket = Rocket(earth, thrust=GetThrust, mass=GetMass, timezoom=tz)
earth.run(rocket)
