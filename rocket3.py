from ggrocket import Rocket, Planet
from math import radians, sqrt
from ggmath import InputButton, Timer

earth = Planet(planetmass=0)  # no gravity to simplify things

RocketStarted = False
timer = Timer()

# Falcon F9R specifications
me = 25600          # Empty mass
mp =  395700        # Propellent mass
F1D = 716000        # Single engine thrust (Newtons)
N1D = 9             # Number of rocket engines
Ftotal = F1D * N1D  # Total thrust (Newtons)
tburn = 180         # Burn time (seconds)

# Predict the final velocity
vmax = N1D*F1D*tburn/(me+mp)
print("Predicted final velocity, vmax: ", vmax, " m/s")

# Create a function for determining the rocket thrust
def GetThrust():
    if RocketStarted:
        return Ftotal
    else:
        return 0

# Function for starting the rocket thrust (called by the START "button")
def StartRocket():
    global RocketStarted
    if not RocketStarted:
        RocketStarted = True
        # Start a timer that will STOP the rocket engine
        timer.callAfter(tburn, StopRocket)
    
# Function for stopping the rocket thrust (called by timer)
def StopRocket(timer):
    global RocketStarted
    if RocketStarted:
        RocketStarted = False
    
# Create a button for starting the simulation
# Physical positioning at 10,400 pixels, calls the StartRocket function
start = InputButton((10,400), "START", StartRocket, positioning="physical", size=15)

#Create and "run" the rocket
rocket = Rocket(earth, thrust=GetThrust, mass=me+mp, heading=radians(90))
earth.run(rocket)