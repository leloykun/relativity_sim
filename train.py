import pygame

class Train:
    main_color = (172, 240, 242)
    gun_color = (34, 83, 120)
    w = 200
    h = 20
    
    def __init__(self, env, type):
        self.env = env
        self.type = type
        
        if self.type == 'train_frame':
            self.x = (self.env.screen_X_size - self.w) // 2
            self.y = 0
            self.dx = 0
            self.dy = 1
        elif self.type == 'ground_frame':
            self.x = 0
            self.y = 0
            self.dx = self.env.def_train_speed
            self.dy = 1
        elif self.type == 'stationary_train':
            self.x = (self.env.screen_X_size - self.w) // 2
            self.y = (self.env.screen_Y_size - self.h) // 2
            self.dx = 0
            self.dy = 0
        elif self.type == 'moving_train':
            self.x = -200
            self.y = (self.env.screen_Y_size - self.h) // 2
            self.dx = self.env.def_train_speed
            self.dy = 0
            if self.env.light_type == 'einstein':
                self.contract()
            
    def update(self):
        self.move()
        self.display()
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def display(self):
        rec = (self.x, self.y, self.w, self.h)
        cir = (int(self.x+self.w//2), int(self.y+self.h//2))
        pygame.draw.rect(self.env.screen, self.main_color, rec, 0)
        pygame.draw.circle(self.env.screen, self.gun_color, cir, 10, 0)
        
    def contract(self):
        from math import sqrt
        self.w = self.w * sqrt(1-self.dx*self.dx)
        #  from light import Light
        #  self.w = self.w * sqrt(1-(self.dx*self.dx)/(Light.c*Light.c))
        