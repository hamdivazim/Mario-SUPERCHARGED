""" GAME LOOP """
import pygame
import csv

pygame.init()

def left_down(key):
    return key == pygame.K_LEFT or key == pygame.K_a

def right_down(key):
    return key == pygame.K_RIGHT or key == pygame.K_d

def up_down(key):
    return key == pygame.K_UP or key == pygame.K_w

def down_down(key):
    return key == pygame.K_DOWN or key == pygame.K_s

def z_down(key):
    return key == pygame.K_z

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

# Game vars
GRAVITY  = 0.75

class Mario(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True

        self.crouching = False

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

        image = pygame.image.load(f'data/assets/{self.char_type}_sprites/smcrouch.png')
        image = pygame.transform.smoothscale(image, (int(image.get_width()*self.scale), int(image.get_height()*self.scale)))
        temp = [image]
        self.animation_list.append(temp)

        self.image = self.animation_list[self.action][self.index_frame]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        

    def move(self, moving_left, moving_right, world, bg_scroll, tile_size, screen_width):
        dx = 0
        dy = 0

        scroll = 0

        # Left-Right
        if moving_left and moving_right:
            self.update_action(0)
        else:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -16
            self.jump = False
            self.in_air = True
        
        # Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        # Check for collisions
        for tile in world.obstacle_list:
            # Check x collisions
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.vel_x = 0
                dx = 0

            # Check y collisions
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                # Falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

        if self.crouching:
            self.rect.y += 15

        self.update_animation()

        if moving_left:
            if self.rect.left < 200 and bg_scroll > abs(dx):
                self.rect.x -= dx
                scroll = -dx
        elif moving_right:
            if self.rect.right > 800 and bg_scroll < (world.level_length*tile_size)-screen_width:
                self.rect.x -= dx
                scroll = -dx

        return scroll

    def update_animation(self):
        if self.crouching:
            self.image = self.animation_list[4][0]
        else:
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




SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SCROLL_THRESH = 200

screen_scroll = 0
bg_scroll = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mario SUPERCHARGED')

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Colours
BG = (8, 234, 255)
RED = (255, 0, 0)


# Vars
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 10
world = 1
level = 1

# Images
tile_images = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'data/assets/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_images.append(img)

# Load Backgrounds
overworld_img = pygame.image.load('data/assets/backgrounds/overworld.png').convert_alpha()
overworld_img = pygame.transform.scale(overworld_img, (overworld_img.get_width()*2, overworld_img.get_height()*2))

# Draw Background
def draw_bg():
    screen.fill(BG)
    width = overworld_img.get_width()
    for x in range(10):
        screen.blit(overworld_img, (width*(x-1)-(bg_scroll*0.5), 0))

# Sprite groups
decor_group = pygame.sprite.Group()

# Classes
class World():
    def __init__(self, tile_images, tile_size):
        self.obstacle_list = []
        self.player = None

        self.tile_images = tile_images
        self.TILE_SIZE = tile_size

    def process_data(self, data):
        self.level_length = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.tile_images[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.TILE_SIZE
                    img_rect.y = y * self.TILE_SIZE

                    tile_data = (img, img_rect)

                    # CHANGE FOR WHEN ADD DECOR
                    if tile >= 0 and tile <= 5:
                        self.obstacle_list.append(tile_data)
                    elif tile == 6: # Create Player
                        self.player = Mario("mario", x*self.TILE_SIZE, y*self.TILE_SIZE, 7/16, 5)
                    elif tile >= 7 and tile <= 9:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
                        decor_group.add(decoration)

    def draw(self, screen):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

# Load level
world_data = []
for row in range(ROWS):
    r = [-1]*COLS
    world_data.append(r)

with open(f'levs/w{world}l{level}.csv', newline='') as file:
    reader = csv.reader(file, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World(tile_images, TILE_SIZE)
world.process_data(world_data)

mario = world.player

# Player actions
moving_left = False
moving_right = False

run = True
while run:
    clock.tick(FPS)

    # Update Background
    draw_bg()

    # Draw world
    world.draw(screen)

    # Update and draw groups
    decor_group.update((screen_scroll))
    decor_group.draw(screen)

    # Draw player
    mario.update_animation()
    mario.draw(screen)

    # Update player actions
    if mario.alive:
        mario.vel_x *= 0.8
        if abs(mario.vel_x) < 0.01:
            mario.vel_x = 0
        mario.rect.x += ((mario.vel_x*5)*mario.direction)

        if mario.in_air:
            if mario.vel_y > 0:
                mario.update_action(3)
            else:
                mario.update_action(2)
        elif moving_left or moving_right:
            mario.update_action(1)
        else:
            mario.update_action(0)

    screen_scroll = mario.move(moving_left, moving_right, world, bg_scroll, TILE_SIZE, SCREEN_WIDTH)
    bg_scroll -= screen_scroll

    for event in pygame.event.get():
		# Quit game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if left_down(event.key):
                moving_left = True
            if right_down(event.key):
                moving_right = True
            if up_down(event.key) and mario.alive:
                mario.jump = True
            if z_down(event.key):
                mario.speed = 6

        if event.type == pygame.KEYUP:
            if left_down(event.key):
                moving_left = False
                mario.vel_x = 0
            if right_down(event.key):
                moving_right = False
                mario.vel_x = 0
            if z_down(event.key):
                mario.speed = 5

    pygame.display.update()

pygame.quit()
