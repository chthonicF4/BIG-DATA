import numpy , matplotlib.pyplot as plt , math

plot = plt.title("TEST")

# SIM SETTINGS

ball_mass = 1 #kg
angle_of_shooting = 90 # number between 0 and 90
speed_of_ball = 5 # m/s
height = 5 # m
g = 9.81 # n/kg

# GRAPH SETTINGS

time_step = 0.05

# -------

def deg2rad(deg:float):
    return (deg/180)*math.pi

angle_of_shooting = deg2rad(float(angle_of_shooting))

resultant_horisontal = math.cos(angle_of_shooting)*speed_of_ball
resultant_vertical = math.sin(angle_of_shooting)*speed_of_ball
gravitational_force = ball_mass*g

x,y,t = [0],[height],0
current_x , current_y = 0,height

while current_y > 0 :
    t += time_step

    current_x += resultant_horisontal*time_step

    current_y += resultant_vertical - (gravitational_force*t)
    
    
    x.append(current_x)
    y.append(current_y)

print("done")

plt.plot(x,y)
plt.show()




