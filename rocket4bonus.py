# Lundar Lander Simulation
from ggrocket import Rocket, Planet
from math import radians, sqrt, log
from ggmath import Label, Slider
from ggame import Color

G = 6.673E-11   # universal gravitation constant
moonmass = 7.3477E22
moonradius = 1738000
alt = 15000     # approximately 15 km orbital altitude
vel = sqrt(G*moonmass/(moonradius + alt))

# Lunar Lander specifications
mascent = 4700          # Ascent stage gross (fueled) mass
mdescent = 10344        # Descent stage gross (fueled) mass
mdescfuel = 8200        # Descent stage fuel mass
Fdmax = 45040           # Descent stage maximum thrust
SpecIdesc = 3050        # Descent specific impulse (Ns/kg)
mdotmax = Fdmax/SpecIdesc # Maximum propellent flow rate
MinThrottle = 0.1       # 10% minimum throttle
MaxThrottle = 0.6       # 60% full throttle
MinThrust = MinThrottle * Fdmax
MaxThrust = MaxThrottle * Fdmax


class Lem(Rocket):
    def __init__(self, planet, **kwargs):
        kwargs['thrust'] = self.GetThrust
        kwargs['mass'] = self.GetMass
        self.LastTime = self.shiptime
        self.FuelLeft = mdescfuel
        super().__init__(planet, **kwargs)
        # Clue for the thrust slider
        self.lab1 = Label((10,345), "Thrust: up/down key", positioning="physical", size=15)
        # Define a thrust slider
        self.ThrustSlider = Slider((10,360), 0, MaxThrottle, 0, positioning="physical", steps=20, leftkey="down arrow", rightkey="up arrow")
        
        
    # Create a function for determining the rocket thrust
    def GetThrust(self):
        elapsedtime = self.shiptime - self.LastTime
        self.LastTime = self.shiptime
        thrustpct = self.ThrustSlider()
        if thrustpct < 0.1:
            return 0
        elif self.FuelLeft > 0:
            self.FuelLeft = self.FuelLeft - mdotmax*thrustpct*elapsedtime
            return Fdmax*thrustpct
        return 0
    
    # Function for calculating the total rocket mass, based on burn time and total
    # propellent mass.
    def GetMass(self):
        return self.FuelLeft + mdescent - mdescfuel + mascent
    
    


moon = Planet(planetmass=moonmass, radius=moonradius, color=Color(0x202020,1)) 



#Create and "run" the rocket
lander = Lem(moon, altitude=alt, velocity=vel)

moon.run(lander)
