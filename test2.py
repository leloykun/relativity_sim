import pygame
import sys


class Light:
    color = (255, 255, 0)
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
        self.train.env.light_positions.append((self.x, self.y))
        
    def move(self):
        self.x += self.dx
        self.y += self.dy


class Train:
    color = (0,0,0)
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
            self.dx = 0.3
            self.dy = 1
        
    def update(self):
        self.move()
        self.display()
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def display(self):
        rec = (self.x, self.y, self.w, self.h)
        cir = (int(self.x+100), int(self.y+10))
        pygame.draw.rect(self.env.screen, self.color, rec, 1)
        pygame.draw.circle(self.env.screen, self.color, cir, 10, 0)
        
        
class Environment:
    screen_X_size = 640
    screen_Y_size = 640
    
    def __init__(self, sim_type, light_type):
        self.sim_type = sim_type
        self.light_type = light_type
    
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_X_size, self.screen_Y_size))
        
        self.paused = False
        
        if sim_type == 'train_frame':
            self.train = Train(self, 'train_frame')
        elif sim_type == 'ground_frame':
            self.train = Train(self, 'ground_frame')
        
        self.left_light = Light(self.train, self.light_type+'_left')
        self.right_light = Light(self.train, self.light_type+'_right')
        
        self.light_positions = []
        
    def run(self):
        clock = pygame.time.Clock()
        while True:
            ms_elapsed = clock.tick(100)
            
            #  change train
            if self.train.y >= self.screen_Y_size :
                if self.train.type == 'train_frame':
                    self.train = Train(env, 'ground_frame')
                    self.left_light = Light(self.train, self.light_type+'_left')
                    self.right_light = Light(self.train, self.light_type+'_right')
                else:
                    self.train = Train(self, 'train_frame')
                    self.left_light = Light(self.train, self.light_type+'_left')
                    self.right_light = Light(self.train, self.light_type+'_right')
            
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
        
        self.train.update()
        
        self.left_light.update()
        if self.left_light.x <= self.train.x:
            self.left_light = Light(self.train, 'dummy')
            #print(pygame.time.get_ticks())
        self.right_light.update()
        if self.right_light.x >= self.train.x + self.train.w:
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
            
        for i in range(0, len(self.light_positions), 9):
            x, y = map(int, self.light_positions[i])
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 3, 0)
        
        for x in range(20, self.screen_X_size, 50):
            pygame.draw.aaline(self.screen, (0, 0, 0),  (x, 0), (x, self.screen_Y_size))
        for y in range(10, self.screen_Y_size, 50):
            pygame.draw.aaline(self.screen, (0, 0, 0),  (0, y), (self.screen_X_size, y))
        
        pygame.display.flip()
        

if __name__ == '__main__':
    env = Environment(sim_type='train_frame', light_type='einstein')
    env.run()
