from ggrocket import Rocket, Planet
from math import radians, sqrt, log
from ggmath import InputButton, Timer

earth = Planet(planetmass=0)  # no gravity to simplify things

RocketStarted = False
timer = Timer()
starttime = None    # to keep track of when burn started
burntime = 0        # to keep track of how long the burn has lasted

# Falcon F9R specifications
me = 25600          # Empty mass
mp =  395700        # Propellent mass
F1D = 716000        # Single engine thrust (Newtons)
N1D = 9             # Number of rocket engines
Ftotal = F1D * N1D  # Total thrust (Newtons)
tburn = 180         # Burn time (seconds)

# Predict the final velocity based on simple Newtons' 2nd Law
vmax = Ftotal*tburn/(me+mp)
print("Predicted final velocity (Newton's 2nd Law), vmax: ", vmax, " m/s")

# Predict the final velocity using Tsiolkovsky's Rocket Equation
vmaxre = Ftotal*tburn/mp*log((me+mp)/me)
print("Predicted final velocity (Rocket Equation), vmax: ", vmaxre, " m/s")

# Create a function for determining the rocket thrust
def GetThrust():
    if RocketStarted:
        return Ftotal
    else:
        return 0

# Function for starting the rocket thrust (called by the START "button")
def StartRocket():
    global RocketStarted
    global starttime
    if not RocketStarted:
        RocketStarted = True
        # Start a timer that will STOP the rocket engine
        timer.callAfter(tburn, StopRocket)
        # Note the starting time
        starttime = timer.time
    
# Function for stopping the rocket thrust (called by timer)
def StopRocket(timer):
    global RocketStarted
    if RocketStarted:
        RocketStarted = False
        
# Function for calculating the total rocket mass, based on burn time and total
# propellent mass.
def GetMass():
    # calculate empty mass plus a fraction of the propellent mass
    return me + mp*(tburn-burntime)/tburn
    
    
# Create a button for starting the simulation
# Physical positioning at 10,400 pixels, calls the StartRocket function
start = InputButton((10,400), "START", StartRocket, positioning="physical", size=15)

#Create and "run" the rocket
rocket = Rocket(earth, thrust=GetThrust, mass=me+mp, heading=radians(90))
earth.run(rocket)