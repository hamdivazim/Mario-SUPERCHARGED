""" GAME LOOP """
import pygame
from pygame import mixer
import player
import items
import controls
import csv

mixer.init()
pygame.init()


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

# Load music and sounds
pygame.mixer.music.load('data/assets/sounds/tracks/overworld.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 1000)

jump_fx = pygame.mixer.Sound('data/assets/sounds/effects/jump.mp3')
jump_fx.set_volume(0.6)

# Vars
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 15
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
mushroom_group = pygame.sprite.Group()

# Classes
class TileSprite(pygame.sprite.Sprite):
    def __init__(self, tile, animation=[]):
        pygame.sprite.Sprite.__init__(self)

        self.tile = tile

        self.animation = animation if animation != [] else [self.tile[0]]

        self.frame = 0

    def draw(self, screen):
        self.frame += 1

        self.tile[0] = self.animation[self.frame % len(self.animation)]

class World():
    def __init__(self, tile_images, tile_size):
        self.obstacle_list = []
        self.player = None

        self.tile_images = tile_images
        self.TILE_SIZE = tile_size

        self.tile_animation = -1

        self.screen_scroll = screen_scroll

    def process_data(self, data):
        self.level_length = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.tile_images[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.TILE_SIZE
                    img_rect.y = y * self.TILE_SIZE

                    tile_data = [img, img_rect, tile, x, y]

                    # CHANGE FOR WHEN ADD DECOR
                    if tile >= 0 and tile <= 5:
                        self.obstacle_list.append(tile_data)
                    elif tile == 6: # Create Player
                        self.player = player.Mario("mario", x*self.TILE_SIZE, y*self.TILE_SIZE, 7/16, 5)
                    elif tile >= 7 and tile <= 9:
                        decoration = items.Decoration(img, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)
                        decor_group.add(decoration)
                    elif tile == 10:
                        self.obstacle_list.append(tile_data)

    def sprout_mushroom(self, tile, x, tile_size):
        mushroom = items.Mushroom(x, ((tile[4]-1)*tile_size), tile_size)
        mushroom_group.add(mushroom)

    def upgrade_player(self):
        if not self.player.power > 0:
            self.player.power = 1
            self.player.update_animation()
            self.player.rect = self.player.image.get_rect()
            self.player.width = self.player.image.get_width()
            self.player.height = self.player.image.get_height()
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y
            if not self.player.in_air:
                self.player.rect.y -= 26

    def draw(self, screen):
        self.screen_scroll = screen_scroll
        print(self.player.height)
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            if tile[1].y != tile[4] * self.TILE_SIZE:
                tile[1].y = tile[4] * self.TILE_SIZE
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
dash_timer = 0

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

    mushroom_group.update((world))
    mushroom_group.draw(screen)

    # Draw player
    world.player.update_animation()
    world.player.draw(screen)

    # Update player actions
    if world.player.alive:
        world.player.vel_x *= 0.8
        if abs(world.player.vel_x) < 0.01:
            world.player.vel_x = 0
        world.player.rect.x += ((world.player.vel_x*5)*world.player.direction)

        if world.player.in_air:
            if world.player.vel_y > 0:
                world.player.update_action(3)
            else:
                world.player.update_action(2)
        elif moving_left or moving_right:
            if dash_timer > 0:
                world.player.update_action(5)
            else:
                world.player.update_action(1)
        else:
            world.player.update_action(0)

    

    screen_scroll = world.player.move(moving_left, moving_right, world, bg_scroll, TILE_SIZE, SCREEN_WIDTH, screen_scroll)
    bg_scroll -= screen_scroll

    for event in pygame.event.get():
		# Quit game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if controls.left_down(event.key):
                moving_left = True
            if controls.right_down(event.key):
                moving_right = True
            if controls.up_down(event.key) and world.player.alive:
                world.player.jump = True
                if not world.player.in_air:
                    jump_fx.play()
            if controls.z_down(event.key):
                world.player.speed = 6
                dash_timer += 1

        if event.type == pygame.KEYUP:
            if controls.left_down(event.key):
                moving_left = False
                world.player.vel_x = 0
            if controls.right_down(event.key):
                moving_right = False
                world.player.vel_x = 0
            if controls.z_down(event.key):
                world.player.speed = 5
                dash_timer = 0

    if world.player.power > 0:
        world.player.height = 83

    pygame.display.update()

pygame.quit()