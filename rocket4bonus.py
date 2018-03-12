# Lundar Lander Simulation
from ggrocket import Rocket, Planet
from math import radians, sqrt, log
from ggmath import InputButton, Timer
from ggame import Color

G = 6.673E-11   # universal gravitation constant
moonmass = 7.3477E22
moonradius = 1738000
alt = 15000     # approximately 15 km orbital altitude
vel = sqrt(G*moonmass/(moonradius + alt))

moon = Planet(planetmass=moonmass, radius=moonradius, color=Color(0x202020,1)) 

# Create a function for determining the rocket thrust
def GetThrust():
    return 0

# Function for starting the rocket thrust (called by the START "button")
def StartRocket():
    global RocketStarted
    global StartTime
    if not RocketStarted:
        RocketStarted = True
        # Note the starting time
        StartTime = rocket.shiptime
        
# Function for calculating the total rocket mass, based on burn time and total
# propellent mass.
def GetMass():
    return 1

# Create a button for starting the simulation
# Physical positioning at 10,400 pixels, calls the StartRocket function
start = InputButton((10,400), "START", StartRocket, positioning="physical", size=15)

#Create and "run" the rocket
lander = Rocket(moon, thrust=GetThrust, mass=GetMass)
moon.run(lander)
