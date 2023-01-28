import pygame
from pygame import mixer

mixer.init()
pygame.init()

# Player sound effects
powerup_fx = pygame.mixer.Sound('data/assets/sounds/effects/powerup.mp3')
powerup_fx.set_volume(0.6)

reserve_pwrup_fx = pygame.mixer.Sound('data/assets/sounds/effects/reserve.mp3')
reserve_pwrup_fx.set_volume(0.6)

# Images
coin_images = []
for x in range(19,23):
    img = pygame.image.load(f'data/assets/tiles/{x}.png')
    img = pygame.transform.scale(img, (img.get_width()*0.8, img.get_height()*0.8))
    coin_images.append(img)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x+tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/assets/items/mushroom.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.8, self.image.get_height()*0.8))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y + (tile_size - self.image.get_height()))

        self.direction = 3

        self.vel_y = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, world):
        self.rect.x += world.screen_scroll

        dx = 0
        dy = 0
        
        # Gravity
        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        # Check for collisions
        for tile in world.obstacle_list:
            # Check x collisions
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.vel_x = 0
                dx = 0
                self.direction *= -1

            # Check y collisions
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Falling
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Check if touching player
        if self.rect.colliderect(world.player.rect.x, world.player.rect.y + dy, world.player.width, world.player.height):
            if world.player.power > 0:
                reserve_pwrup_fx.play()
            
            powerup_fx.play()
            self.kill()
            world.upgrade_player()

        self.rect.x += self.direction
        self.rect.y += dy

class CoinParticle(pygame.sprite.Sprite):
    def __init__(self, tile, tile_size, screen_scroll):
        pygame.sprite.Sprite.__init__(self)

        self.ani_frame = 0

        self.x = tile[3]*tile_size

        self.image = coin_images[round(self.ani_frame)]
        self.rect = self.image.get_rect()
        self.rect.x = (tile[3]*tile_size)+ screen_scroll
        self.rect.y = (tile[4]*tile_size) - (tile_size)

        self.vel_y = -12

    def update(self, screen_scroll):
        self.rect.x = self.x+screen_scroll

        self.image = coin_images[round(self.ani_frame) % len(coin_images)]

        self.ani_frame += 0.25

        self.rect.y += self.vel_y
        self.vel_y += 1

        if self.vel_y > 13:
            self.kill()