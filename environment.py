from grid import Grid
from light import Light
from train import Train
import pygame
import sys

class Environment:
    screen_X_size = 640
    screen_Y_size = 640
    def_train_speed = 0.7
    
    #  def __init__(self, (reference_frame='ground', has_time_dim=False, transformation='galilean'), menu=None, switchable=True):
    def __init__(self, menu=None, reference_frame='train', has_time_dim=True, transformation='lorrentz', switchable=True):
        self.reference_frame = reference_frame
        self.has_time_dim   = has_time_dim
        self.transformation = transformation
        self.menu = menu
        self.switchable = switchable
        
        self.switch_count = 0
        self.paused = False
        self.showing_transformation = False
    
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_X_size, self.screen_Y_size))
        
        self.grid = Grid(self)
        
        self.train = Train(self)
        
        self.left_light = Light(self, 'left')
        self.right_light = Light(self, 'right')
        
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
        while True:
            ms_elapsed = clock.tick(100)
            
            if self.reference_frame == 'ground' and self.has_time_dim == 'notime':
                if self.train.x >= self.screen_X_size:
                    self.train = Train(self)
                    self.left_light = Light(self, 'left')
                    self.right_light = Light(self, 'right')
            elif self.switchable and self.train.y >= self.screen_Y_size:
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
            if self.transformation == 'galilean':
                left_dx = (self.train.w//2)*(self.def_train_speed - Light.c)
                right_dx = (self.train.w//2)*(self.def_train_speed + Light.c)
                print(left_dx, right_dx)
                vx = self.train.w//2 + (self.train.w//2)*self.def_train_speed*i
                vy = self.train.h//2 + 100*i
                self.twisted_light_paths.append(((vx, vy), (vx + left_dx, vy + 100)))
                self.twisted_light_paths.append(((vx, vy), (vx + right_dx, vy + 100)))
                self.twisted_lengths.append(((vx + left_dx, vy + 100), (vx + right_dx, vy + 100)))
            elif self.transformation == 'lorrentz':
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
                if self.menu:
                    self.menu.run()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                if self.has_time_dim == True:
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
            self.left_light = Light(self, 'left', is_dummy=True)
        if self.left_light.is_dummy and self.right_light.x >= self.train.x + self.train.w:
            self.left_light = Light(self, 'left')
            self.right_light = Light(self, 'right')
        
        if self.has_time_dim == True:
            self.persistent_info()
        
        pygame.display.flip()
    
    def change_train(self):
        if self.has_time_dim:
            if self.reference_frame == 'train':
                self.reference_frame = 'ground'
            elif self.reference_frame == 'ground':
                self.reference_frame = 'train'
            self.train = Train(self)
            self.left_light = Light(self, 'left')
            self.right_light = Light(self, 'right')
            self.switch_count += 1
    
    def persistent_info(self):
        for line in self.lengths:
            pygame.draw.line(self.screen, (127, 127, 127), line[0], line[1], 7)
        for position in self.light_positions:
            pygame.draw.circle(self.screen, Light.color, position, 3, 0)
