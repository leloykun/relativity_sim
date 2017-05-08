import pygame
import sys

class Grid:
    color = (127, 127, 127)
    x_distortion = 0
    y_distortion = 0

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
        if (self.env.sim_type == 'stationary_train' or self.env.sim_type == 'train_frame') and not self.env.showing_transformation:
            self.x_offset -= self.env.def_train_speed
        self.display()
        
    def display(self, distorted=False):
        for x in range(int(self.x_offset), self.env.screen_X_size + (self.env.screen_X_size - self.env.screen_X_size%self.spacing), self.spacing):
            pygame.draw.aaline(self.env.screen, self.color,  (x, 0), (x + (self.x_distortion if distorted else 0), self.env.screen_Y_size))
        for y in range(self.y_offset - (self.env.screen_Y_size - self.env.screen_Y_size%self.spacing), self.env.screen_Y_size, self.spacing):
            pygame.draw.aaline(self.env.screen, self.color,  (0, y), (self.env.screen_X_size, y + (self.y_distortion if distorted else 0)))
            
    def distort(self):
        y_rise = self.env.twisted_light_paths[1][1][1] - self.env.twisted_light_paths[0][1][1]
        y_run = self.env.twisted_light_paths[1][1][0] - self.env.twisted_light_paths[0][1][0]
        self.y_distortion = int(self.env.screen_X_size*y_rise/y_run)
        
        x_rise = self.env.twisted_lengths[1][0][1] - self.env.twisted_lengths[0][0][1]
        x_run = self.env.twisted_lengths[1][0][0] - self.env.twisted_lengths[0][0][0]
        print(x_rise, x_run)
        self.x_distortion = int(-self.y_distortion)
        
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
            self.x = self.train.env.screen_X_size + 10
            self.y = self.train.env.screen_Y_size + 10
            self.dx = -self.c
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
    def_train_speed = 0.7
    
    def __init__(self, menu, sim_type, light_type, switchable=True):
        self.menu = menu
        self.sim_type = sim_type
        self.light_type = light_type
        self.switchable = switchable
        self.switch_count = 0
        self.stopped = False
    
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_X_size, self.screen_Y_size))
        
        self.paused = False
        self.showing_transformation = False
        
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
        
        self.normal_light_paths = [] 
        self.normal_lengths = []
        self.twisted_light_paths = [] 
        self.twisted_lengths = []
        
        self.calculate_normal()
        self.calculate_twisted()
        
        self.grid.distort()
        
        self.light_positions = set()
        self.lengths = set()
        
    def run(self):
        clock = pygame.time.Clock()
        while not self.stopped:
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
    
    def show_transformation(self):
        self.showing_transformation = not self.showing_transformation
        self.anim_frame = 0
        while self.showing_transformation:
            self.animate_transformation()
            pygame.time.delay(5)
            self.anim_frame = (self.anim_frame + 1) % 100
    
    def calculate_normal(self):
        for i in range(6):
            self.normal_light_paths.append(((self.screen_X_size//2, self.train.h//2 + 100*i), 
                                           ((self.screen_X_size - self.train.w)//2, self.train.h//2 + 100*(i+1))))
            self.normal_light_paths.append(((self.screen_X_size//2, self.train.h//2 + 100*i), 
                                           ((self.screen_X_size + self.train.w)//2, self.train.h//2 + 100*(i+1))))
            self.normal_lengths.append((((self.screen_X_size - self.train.w)//2, self.train.h//2 + 100*(i+1)), 
                                        ((self.screen_X_size + self.train.w)//2, self.train.h//2 + 100*(i+1))))
        
    def calculate_twisted(self):
        for i in range(6):
            if self.light_type == 'gallilean':
                left_dx = (self.train.w//2)*(self.def_train_speed - Light.c)
                right_dx = (self.train.w//2)*(self.def_train_speed + Light.c)
                print(left_dx, right_dx)
                vx = self.train.w//2 + (self.train.w//2)*self.def_train_speed*i
                vy = self.train.h//2 + 100*i
                self.twisted_light_paths.append(((vx, vy), (vx + left_dx, vy + 100)))
                self.twisted_light_paths.append(((vx, vy), (vx + right_dx, vy + 100)))
                self.twisted_lengths.append(((vx + left_dx, vy + 100), (vx + right_dx, vy + 100)))
            elif self.light_type == 'einstein':
                left_dx = -(self.train.w//2)//(self.def_train_speed + Light.c)
                right_dx = -(self.train.w//2)//(self.def_train_speed - Light.c)
                vx = self.train.w//2 + right_dx*self.def_train_speed*i
                vy = self.train.h//2 + right_dx*i
                self.twisted_light_paths.append(((vx, vy), (vx + left_dx, vy - left_dx)))
                self.twisted_light_paths.append(((vx, vy), (vx + right_dx, vy + right_dx)))
                self.twisted_lengths.append(((vx + left_dx, vy - left_dx), (vx - left_dx, vy - left_dx)))
    
    def animate_transformation(self):
        self.check_for_events()
        
        self.screen.fill((255, 255, 255))
        
        self.grid.update()
        
        
        if self.anim_frame == 0:
            pygame.time.delay(100)
        
        for i in range(len(self.normal_lengths)):
            if self.anim_frame < 50:
                (nx0, ny0), (nx1, ny1) = self.normal_lengths[i]
                (tx0, ty0), (tx1, ty1) = self.twisted_lengths[i]
                fro_x = nx0 + (tx0-nx0)*(self.anim_frame+1)//50
                fro_y = ny0 + (ty0-ny0)*(self.anim_frame+1)//50
                to_x = nx1 + (tx1-nx1)*(self.anim_frame+1)//50
                to_y = ny1 + (ty1-ny1)*(self.anim_frame+1)//50
                pygame.draw.line(self.screen, (127, 127, 127), (fro_x, fro_y), (to_x, to_y), 7)
            else:
                (nx0, ny0), (nx1, ny1) = self.normal_lengths[i]
                (tx0, ty0), (tx1, ty1) = self.twisted_lengths[i]
                fro_x = tx0 - (tx0-nx0)*(self.anim_frame-49)//50
                fro_y = ty0 - (ty0-ny0)*(self.anim_frame-49)//50
                to_x = tx1 - (tx1-nx1)*(self.anim_frame-49)//50
                to_y = ty1 - (ty1-ny1)*(self.anim_frame-49)//50
                pygame.draw.line(self.screen, (127, 127, 127), (fro_x, fro_y), (to_x, to_y), 7)
        
        for i in range(len(self.normal_light_paths)):
            if self.anim_frame < 50:
                (nx0, ny0), (nx1, ny1) = self.normal_light_paths[i]
                (tx0, ty0), (tx1, ty1) = self.twisted_light_paths[i]
                fro_x = nx0 + (tx0-nx0)*(self.anim_frame+1)//50
                fro_y = ny0 + (ty0-ny0)*(self.anim_frame+1)//50
                to_x = nx1 + (tx1-nx1)*(self.anim_frame+1)//50
                to_y = ny1 + (ty1-ny1)*(self.anim_frame+1)//50
                pygame.draw.line(self.screen, Light.color, (fro_x, fro_y), (to_x, to_y), 7)
            else:
                (nx0, ny0), (nx1, ny1) = self.normal_light_paths[i]
                (tx0, ty0), (tx1, ty1) = self.twisted_light_paths[i]
                fro_x = tx0 - (tx0-nx0)*(self.anim_frame-49)//50
                fro_y = ty0 - (ty0-ny0)*(self.anim_frame-49)//50
                to_x = tx1 - (tx1-nx1)*(self.anim_frame-49)//50
                to_y = ty1 - (ty1-ny1)*(self.anim_frame-49)//50
                pygame.draw.line(self.screen, Light.color, (fro_x, fro_y), (to_x, to_y), 7)
        
        if self.anim_frame == 50:
            pygame.time.delay(100)
        
        pygame.display.flip()
    
    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.menu.run()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                if self.sim_type == 'train_frame' or self.sim_type == 'ground_frame':
                    self.show_transformation()
    
    def update(self):
        self.check_for_events()
        
        if self.paused:
            return
    
        self.screen.fill((255, 255, 255))
        
        self.grid.update()
        
        self.train.update()
        
        #print(self.right_light.x - self.left_light.x)
        
        self.left_light.update()
        self.right_light.update()
        
        if self.left_light.x <= self.train.x:
            self.lengths.add(((int(self.left_light.x), int(self.left_light.y)), 
                              (int(self.right_light.x), int(self.right_light.y))))
            self.left_light = Light(self.train, 'dummy')
        if self.left_light.type == 'dummy' and self.right_light.x >= self.train.x + self.train.w:
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
        
        if self.sim_type == 'train_frame' or self.sim_type == 'ground_frame':
            self.persistent_info()
        
        pygame.display.flip()
    
    def change_train(self):
        if self.train.type == 'train_frame':
            self.sim_type = 'ground_frame'
            self.train = Train(self, 'ground_frame')
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
            self.switch_count += 1
        elif self.train.type == 'ground_frame':
            self.sim_type = 'train_frame'
            self.train = Train(self, 'train_frame')
            self.left_light = Light(self.train, self.light_type+'_left')
            self.right_light = Light(self.train, self.light_type+'_right')
            self.switch_count += 1
    
    def persistent_info(self):
        for line in self.lengths:
            pygame.draw.line(self.screen, (127, 127, 127), line[0], line[1], 7)
        for position in self.light_positions:
            pygame.draw.circle(self.screen, Light.color, position, 3, 0)
        
if __name__ == '__main__': 
    env = Environment(sim_type=input(), light_type=input())
    env.run()
    #env = Environment(sim_type='train_frame', light_type='gallilean')
    #env = Environment(sim_type='train_frame', light_type='einstein')
    #env = Environment(sim_type='stationary_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='einstein')
    #env = Environment(sim_type='moving_train', light_type='gallilean')
    #env.run()
    pass
    
    