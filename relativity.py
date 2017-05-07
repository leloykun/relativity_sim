import pygame
import sys

class Grid:
    color = (0, 0, 0)

    def __init__(self, env):
        self.env = env
        if self.env.sim_type == 'train_frame' or self.env.sim_type == 'ground_frame':
            self.x_offset = 20
            self.y_offset = 10
            self.spacing = 50
        elif self.env.sim_type == 'stationary_train' or self.env.sim_type == 'moving_train':
            self.x_offset = 0
            self.y_offset = 0
            self.spacing = 80
            
    def update(self):
        if self.env.sim_type == 'stationary_train':
            self.x_offset -= self.env.def_train_speed
        self.display()
        
    def display(self):
        for x in range(int(self.x_offset), self.env.screen_X_size, self.spacing):
            pygame.draw.aaline(self.env.screen, self.color,  (x, 0), (x, self.env.screen_Y_size))
        for y in range(self.y_offset, self.env.screen_Y_size, self.spacing):
            pygame.draw.aaline(self.env.screen, self.color,  (0, y), (self.env.screen_X_size, y))
            
class Light:
    color = (255, 152, 0)
    r = 1
    c = 1

    def __init__(self, train, type):
        self.train = train
        
        self.type = type
        if type == 'gallilean_left':
            self.x = self.train.x + self.train.w//2
            self.y = self.train.y + self.train.h//2
            self.dx = self.train.dx - self.c
            self.dy = self.train.dy
        elif type == 'gallilean_right':
            self.x = self.train.x + self.train.w//2
            self.y = self.train.y + self.train.h//2
            self.dx = self.train.dx + self.c
            self.dy = self.train.dy
        elif type == 'einstein_left':
            self.x = self.train.x + self.train.w//2
            self.y = self.train.y + self.train.h//2
            self.dx = -self.c
            self.dy = self.train.dy
        elif type == 'einstein_right':
            self.x = self.train.x + self.train.w//2
            self.y = self.train.y + self.train.h//2
            self.dx = self.c
            self.dy = self.train.dy
        elif type == 'dummy':
            self.x = -5
            self.y = -5
            self.dx = 0
            self.dy = 0
        #print('light created: ', self.x, self.y, self.dx, self.dy)
        
    def update(self):
        self.move()
        if self.train.type == 'train_frame' or self.train.type == 'ground_frame':
            if self.train.env.switch_count <= 1:
                self.train.env.light_positions.add((int(self.x), int(self.y)))
        elif self.train.type == 'stationary_train' or self.train.type == 'moving_train':
            self.display()
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def display(self):
        pygame.draw.circle(self.train.env.screen, self.color, (int(self.x), int(self.y)), 3, 0)

        
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
        
        
class Environment:
    screen_X_size = 640
    screen_Y_size = 640
    def_train_speed = 0.5
    
    def __init__(self, sim_type, light_type, switchable=True):
        self.sim_type = sim_type
        self.light_type = light_type
        self.switchable = switchable
        self.switch_count = 0
    
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_X_size, self.screen_Y_size))
        
        self.paused = False
        
        self.grid = Grid(self)
        
        if sim_type == 'train_frame':
            self.train = Train(self, 'train_frame')
        elif sim_type == 'ground_frame':
            self.train = Train(self, 'ground_frame')
        elif sim_type == 'stationary_train':
            self.train = Train(self, 'stationary_train')
        elif sim_type == 'moving_train':
            self.train = Train(self, 'moving_train')
        
        self.left_light = Light(self.train, self.light_type+'_left')
        self.right_light = Light(self.train, self.light_type+'_right')
        
        self.light_positions = set()
        
    def run(self):
        clock = pygame.time.Clock()
        while True:
            ms_elapsed = clock.tick(100)
            
            if self.sim_type == 'moving_train':
                if self.train.x >= self.screen_X_size:
                    self.train = Train(self, 'moving_train')
            elif self.switchable and self.train.y >= self.screen_Y_size :
                self.change_train()
            
            #pygame.time.delay(10) 
            self.update()
    
    def pause(self):
        self.paused = not self.paused
        while self.paused:
            self.update()
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
        
        if self.paused:
            return
    
        self.screen.fill((255, 255, 255))
        
        self.grid.update()
        
        self.train.update()
        
        #print(self.right_light.x - self.left_light.x)
        
        self.left_light.update()
        if self.left_light.x <= self.train.x:
            self.left_light = Light(self.train, 'dummy')
        
        self.right_light.update()
        if self.right_light.x >= self.train.x + self.train.w:
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
        
        if self.sim_type == 'train_frame' or self.sim_type == 'ground_frame':
            self.display_light_positions()
        
        pygame.display.flip()
    
    def change_train(self):
        if self.train.type == 'train_frame':
            self.train = Train(self, 'ground_frame')
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
            self.switch_count += 1
        else:
            self.train = Train(self, 'train_frame')
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
            self.switch_count += 1
    
    def display_light_positions(self):
        for position in self.light_positions:
            pygame.draw.circle(self.screen, Light.color, position, 3, 0)
    

if __name__ == '__main__':
    #env = Environment(sim_type='train_frame', light_type='gallilean')
    #env = Environment(sim_type='train_frame', light_type='einstein')
    #env = Environment(sim_type='stationary_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='gallilean')
    #env.run()
    pass
    
    