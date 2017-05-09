import pygame

class Light:
    color = (255, 152, 0)
    r = 1
    c = 1

    def __init__(self, env, dir, is_dummy=False):
        self.env = env
        self.train = env.train
        self.dir = dir
        self.is_dummy = is_dummy
        
        if is_dummy:
            self.x = self.train.env.screen_X_size + 100
            self.y = self.train.env.screen_Y_size + 100
            self.dx = 0
            self.dy = 0
            return
        
        self.x = self.train.x + self.train.w//2
        self.y = self.train.y + self.train.h//2
        self.dx = self.c
        self.dy = self.train.dy
        
        if self.dir == 'left':
            self.dx *= -1
        
        if self.env.transformation == 'galilean':
            self.dx += self.train.dx
        
        #print('light created: ', self.x, self.y, self.dx, self.dy)
        
    def update(self):
        self.move()
        if self.env.has_time_dim:
            if self.env.switch_count <= 1:
                self.env.light_positions.add((int(self.x), int(self.y)))
        else:
            self.display()
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def display(self):
        pygame.draw.circle(self.env.screen, self.color, (int(self.x), int(self.y)), 3, 0)
