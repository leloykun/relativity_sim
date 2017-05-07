from __future__ import division
from visual import *
from visual.graph import *
from math import *

size=1e-15
size2=1e-10
b=0.005*size2
start=100*size2
k=9e9
e=1.6e-19

alpha=sphere(pos=(-start,b,0),radius=0.1*size,color=color.red)

alpha.mass=4*1.67e-27
alpha.charge=+2*e
alpha.size=1e-12
alpha.energy=4e6*1.6e-19
alpha.speed=sqrt(2*alpha.energy/alpha.mass)

gold=sphere(pos=(0,0,0), radius=size, color=color.yellow)

gold.mass=197*1.67e-27
gold.charge=+79*e

shell=sphere(pos=gold.pos, radius=size2, color=color.green)
shell.mass=gold.mass/1837
shell.charge=-gold.charge

alpha.momentum=alpha.mass*alpha.speed*vector(1,0,0)
gold.momentum=gold.mass*vector(0,0,0)

alpha.trail=curve(color=alpha.color)
alpha.trail.append(pos=alpha.pos)
gold.trail=curve(color=gold.color)
gold.trail.append(pos=gold.pos)

r=alpha.pos-gold.pos
rhat=r/r.mag
r_min=r.mag

init_r=alpha.pos.mag

print(r,rhat,r.mag2)

dt=0.01*r.mag/alpha.speed
t=0

while alpha.pos.mag<2*init_r:
    if r.mag>size:
        F_alpha=k*alpha.charge*gold.charge*rhat/r.mag2
        F_gold=-F_alpha
    else:
        F_alpha=k*alpha.charge*gold.charge*rhat*(r.mag/size)/(size*size)
        F_gold=-F_alpha

    if r.mag>size2:
        F_alpha=F_alpha+k*alpha.charge*shell.charge*rhat/r.mag2
        F_gold=-F_alpha
    
    check=F_alpha+F_gold
    #print(F_alpha.y)

    alpha.momentum=alpha.momentum+F_alpha*dt
    gold.momentum=gold.momentum+F_gold*dt

    alpha.pos=alpha.pos+(alpha.momentum/alpha.mass)*dt
    alpha.trail.append(pos=alpha.pos)
    gold.pos=gold.pos+(gold.momentum/gold.mass)*dt
    shell.pos=gold.pos
    gold.trail.append(pos=gold.pos)

    r=alpha.pos-gold.pos
    rhat=r/r.mag

    alpha.speed=alpha.momentum.mag/alpha.mass
    dt=0.01*r.mag/alpha.speed
    
    if r.mag<r_min:
        r_min=r.mag
        
    t=t+dt

if alpha.pos.x>0:
    angle=degrees(atan(abs((alpha.pos.y-b)/alpha.pos.x)))
else:
    angle=180-degrees(atan(abs((alpha.pos.y-b)/alpha.pos.x)))

print(b,alpha.pos.y/b,angle)
print(r.mag/size,r_min/size,r_min/size2)
