import pygame

pygame.init()

# Game vars
GRAVITY  = 0.75

class Mario(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True

        self.speed = speed
        self.scale = scale
        self.direction = 1
        self.vel_x = 0
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.char_type = char_type
        self.animation_list = []
        self.index_frame = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        image = pygame.image.load(f'data/assets/{self.char_type}_sprites/smstand.png')
        image = pygame.transform.smoothscale(image, (int(image.get_width()*self.scale), int(image.get_height()*self.scale)))

        temp = []
        temp.append(image)
        self.animation_list.append(temp)
        temp = []

        temp = []
        temp.append(image)
        image = pygame.image.load(f'data/assets/{self.char_type}_sprites/smrun.png')
        image = pygame.transform.smoothscale(image, (int(image.get_width()*self.scale), int(image.get_height()*self.scale)))
        temp.append(image)
        self.animation_list.append(temp)

        image = pygame.image.load(f'data/assets/{self.char_type}_sprites/smjump.png')
        image = pygame.transform.smoothscale(image, (int(image.get_width()*self.scale), int(image.get_height()*self.scale)))
        temp = [image]
        self.animation_list.append(temp)
        image = pygame.image.load(f'data/assets/{self.char_type}_sprites/smfall.png')
        image = pygame.transform.smoothscale(image, (int(image.get_width()*self.scale), int(image.get_height()*self.scale)))
        temp = [image]
        self.animation_list.append(temp)

        self.image = self.animation_list[self.action][self.index_frame]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        # Left-Right
        if moving_left and moving_right:
            self.update_action(0)
        else:
            if moving_left:
                self.vel_x += 0.1
                if self.vel_x > 1:
                    self.vel_x = 1
                dx = -self.speed*self.vel_x
                self.flip = True
                self.direction = -1
            if moving_right:
                self.vel_x += 0.1
                if self.vel_x > 1:
                    self.vel_x = 1
                dx = self.speed*self.vel_x
                self.flip = False
                self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        self.image = self.animation_list[self.action][self.index_frame]

        if pygame.time.get_ticks() - self.update_time > 100:
            self.update_time = pygame.time.get_ticks()
            self.index_frame += 1

        if self.index_frame >= len(self.animation_list[self.action]):
            self.index_frame = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index_frame = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

mario = Mario("mario", 200, 200, 0.375, 8)

# Player actions
moving_left = False
moving_right = False