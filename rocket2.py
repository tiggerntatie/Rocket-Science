from ggame.astro import Rocket, Planet
from math import radians, sqrt
from ggame.slider import Slider

earth = Planet()

# Constants relating to Earth and physics
Re = 6.371E6  # Earth radius: 6371000 meters in scientific notation
Me = 5.972E24 # Earth mass in kg (5.972 x 10^24)
G = 6.674E-11 # Gravitational constant

# Calculate the escape velocity from Earth's surface radius
Ve=sqrt(2*Me*G/Re)
print("Predicted escape velocity is ", Ve, " m/s")

# Add a slider for controlling the timezoom
tz = Slider((10,400), 0, 5, 0, positioning="physical")

rocket = Rocket(earth, heading=radians(90), directiond=90, velocity=Ve, timezoom=tz)
earth.run(rocket)
