import pygame

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
