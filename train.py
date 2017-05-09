import pygame

class Train:
    main_color = (172, 240, 242)
    gun_color = (34, 83, 120)
    len_tracker_color = (127, 127, 127)
    w = 200
    h = 20
    
    def __init__(self, env):
        self.env = env
        
        if self.env.has_time_dim:
            self.y = 0
            self.dy = 1
        elif self.env.has_time_dim == False:
            self.y = (self.env.screen_Y_size - self.h) // 2
            self.dy = 0
        else:
            print("ERROR: has_time_dim not initialized")
        
        if self.env.reference_frame == 'train':
            self.x = (self.env.screen_X_size - self.w) // 2
            self.dx = 0
        elif self.env.reference_frame == 'ground':
            self.x = 0
            self.dx = self.env.def_train_speed
        else:
            print("ERROR: reference_frame not initialized")
        
        #  special case:
        if self.env.reference_frame == 'ground' and self.env.has_time_dim == False:
            self.x = -200
            if self.env.transformation == 'lorentz':
                self.contract()
        
    def update(self):
        self.move()
        self.display()
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def display(self):
        #  main body
        rec = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.env.screen, self.main_color, rec, 0)
        #  photon gun
        cir = (int(self.x+self.w//2), int(self.y+self.h//2))
        pygame.draw.circle(self.env.screen, self.gun_color, cir, 10, 0)
        #  receivers?
        
    def contract(self):
        from math import sqrt
        self.w = self.w * sqrt(1-self.dx*self.dx)
        #  from light import Light
        #  self.w = self.w * sqrt(1-(self.dx*self.dx)/(Light.c*Light.c))
        