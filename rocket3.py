from ggrocket import Rocket, Planet
from math import radians, sqrt
from ggmath import InputButton, Timer

earth = Planet(planetmass=0)  # no gravity to simplify things

RocketStarted = False
timer = Timer()

# Falcon F9R specifications
me = 25600      # Empty mass
mp =  395700   # Propellent mass
F1D = 716000    # Single engine thrust
N1D = 9         # Number of rocket engines
Ftotal = F1D * N1D
tburn = 180

# Create a function for determining the rocket thrust
def GetThrust():
    if RocketStarted:
        return Ftotal
    else:
        return 0

# Function for starting the rocket thrust
def StartRocket():
    global RocketStarted
    RocketStarted = True
    timer.callAfter(tburn, StopRocket)
    
# Function for stopping the rocket thrust (called by timer)
def StopRocket(timer):
    global RocketStarted
    RocketStarted = False
    
# Create a button for starting the simulation
start = InputButton((10,400), "START", StartRocket, positioning="physical")

rocket = Rocket(earth, heading=radians(90), thrust=)
earth.run(rocket)