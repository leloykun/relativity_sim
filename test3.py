from visual import *
from visual.controls import *
import numpy

def cos(x):
    return numpy.cos(x*numpy.pi/180)

def sin(x):
    return numpy.sin(x*numpy.pi/180)

def reaction(): #sets what type of reaction will happen based on the user's input
    trigger = scene.kb.getkey()
    if trigger == 'a' or trigger == 'A':
        #triggers the commands for alpha decay
        while True:
            rate(100)
            #print(alpha1.pos, alpha2.pos, alpha3.pos, alpha4.pos)
            alpha1.pos += alpha1.velocity*1
            alpha2.pos += alpha2.velocity*1
            alpha3.pos += alpha3.velocity*1
            alpha4.pos += alpha4.velocity*1
            if alpha3.pos.x >= paper1.pos.x - 5 or alpha1.pos.y >= paper3.pos.y - 5 or alpha2.pos.x <= paper2.pos.x + 5 or alpha4.pos.y <= paper4.pos.y + 5:
                #when the particle has hit the boundaries of the paper
                if alpha3.pos.x >= paper1.pos.x - 5:
                    #when the particle hits the right boundary
                    print("alpha3",alpha3.pos.x)
                    alpha1.velocity.x = -alpha1.velocity.x
                    alpha2.velocity.x = -alpha2.velocity.x
                    alpha3.velocity.x = -alpha3.velocity.x
                    alpha4.velocity.x = -alpha4.velocity.x
                elif alpha1.pos.y >= paper3.pos.y - 5:
                    #when the particle hits the top boundary
                    print("alpha1",alpha1.pos.y)
                    alpha1.velocity.y = -alpha1.velocity.y
                    alpha2.velocity.y = -alpha2.velocity.y
                    alpha3.velocity.y = -alpha3.velocity.y
                    alpha4.velocity.y = -alpha4.velocity.y
                elif alpha2.pos.x <= paper2.pos.x + 5:
                    #when the particle hits the left boundary
                    print("alpha2",alpha2.pos.x)
                    alpha1.velocity.x = -alpha1.velocity.x
                    alpha2.velocity.x = -alpha2.velocity.x
                    alpha3.velocity.x = -alpha3.velocity.x
                    alpha4.velocity.x = -alpha4.velocity.x
                else:
                    #when the particle hits the bottom boundary
                    print("alpha4",alpha4.pos.y)
                    alpha1.velocity.y = -alpha1.velocity.y
                    alpha2.velocity.y = -alpha2.velocity.y
                    alpha3.velocity.y = -alpha3.velocity.y
                    alpha4.velocity.y = -alpha4.velocity.y
                #b1.set_visible = True
                
                counter = 1
    if trigger == 'b' or trigger == 'B':
        while True:
            rate(100)
            electron.pos += electron.velocity*1
            if electron.pos.x >= wood1.pos.x - 5:
                counter = 1
                break
    if trigger == 'g' or trigger == 'G':
        yinvert = 0
        while True:
            rate(100)
            if yinvert == 0:
                gamma.pos += gamma.velocity*1
            else:
                gamma.pos.x += gamma.velocity.x
                gamma.pos.y += gamma.velocity.y
            if yinvert == 1: yinvert = 0
            else: yinvert = 1
            if gamma.pos.x >= metal1.pos.x - 5:
                counter = 1
                break
            
#def wirecube (s): #setting the cube borders
#    c=curve (color=color.white, radius=1)
#    pts = [(-s, -s, -s),(-s, -s, s), (-s, s, s),
#           (-s, s, -s), (-s, -s, -s), (s, -s, -s),
#           (s, s, -s), (-s, s, -s), (s, s, -s),
#           (s, s, s), (-s, s, s), (s, s, s),
#           (s, -s, s), (-s, -s, s), (s, -s, s),(s, -s, -s)]
#    for pt in pts:
#        c.append(pos=pt)
        
scene = display(title='Radioactive Decay', x=0, y=0, background=(0,0,0)) #setting the size of the display screen

#wirecube(100) #create the cube
#wirecube(125)
#wirecube(150)
counter = 0

atom = sphere(pos=(0,0,0), radius=20, color=color.white)

#---creating the electron---------
electron = sphere(pos=(0,5,0), radius=2, color=color.yellow)
electron.velocity = vector(5,0,0)
#---------------------------------

#---creating the gamma ray--------
gamma = sphere(pos=(0,5,0), radius=10, color=color.yellow, make_trail=true)
gamma.velocity = vector(50,50,0)
#---------------------------------

#---creating the alpha particle---
alpha1 = sphere(pos=(0,5,0), radius=5, color=color.white)
alpha2 = sphere(pos=(-5,0,0), radius=5, color=color.red)
alpha3 = sphere(pos=(5,0,0), radius=5, color=color.red)
alpha4 = sphere(pos=(0,-5,0), radius=5, color=color.white)
alphaangle = 45
alphavelocity = 5
alpha1.velocity = vector(alphavelocity*cos(alphaangle),alphavelocity*sin(alphaangle),0)
alpha2.velocity = vector(alphavelocity*cos(alphaangle),alphavelocity*sin(alphaangle),0)
alpha3.velocity = vector(alphavelocity*cos(alphaangle),alphavelocity*sin(alphaangle),0)
alpha4.velocity = vector(alphavelocity*cos(alphaangle),alphavelocity*sin(alphaangle),0)
#---------------------------------

#---creating the paper obstacle---
paper1 = box(pos=(100,0,0), length=5, height=200, width=200)
paper2 = box(pos=(-100,0,0), length=5, height=200, width=200)
paper3 = box(pos=(0,100,0), length=200, height=5, width=200)
paper4 = box(pos=(0,-100,0), length=200, height=5, width=200)
#---------------------------------

#---creating the wood obstacle---
wood1 = box(pos=(150,0,0), length=5, height=300, width=300, material = materials.wood)
wood2 = box(pos=(-150,0,0), length=5, height=300, width=300, material = materials.wood)
wood3 = box(pos=(0,150,0), length=300, height=5, width=300, material = materials.wood)
wood4 = box(pos=(0,-150,0), length=300, height=5, width=300, material = materials.wood)
#---------------------------------

#---creating the metal obstacle---
metal1 = box(pos=(200,0,0), length=5, height=400, width=400, material = materials.silver)
metal2 = box(pos=(-200,0,0), length=5, height=400, width=400, material = materials.silver)
metal3 = box(pos=(0,200,0), length=400, height=5, width=400, material = materials.silver)
metal4 = box(pos=(0,-200,0), length=400, height=5, width=400, material = materials.silver)
#---------------------------------


if counter == 0: reaction()