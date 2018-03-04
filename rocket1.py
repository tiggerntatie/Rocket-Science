from ggrocket import Rocket, Planet

planet = Planet(viewscale=0.00005)

rocket = Rocket(planet, altitude=400000, velocity=1000, timezoom=1)

planet.run(rocket)