import pygame

class Grid:
    color = (200, 200, 200)
    x_distortion = 0
    y_distortion = 0

    def __init__(self, env):
        self.env = env
        if self.env.has_time_dim:
            self.x_offset = 20
            self.y_offset = 10
            self.spacing = 50
        else:
            self.x_offset = 0
            self.y_offset = 0
            self.spacing = 80
            
    def update(self):
        if self.env.reference_frame == 'train' and not self.env.showing_transformation:
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
