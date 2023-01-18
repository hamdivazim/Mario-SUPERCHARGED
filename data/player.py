import pygame

pygame.init()

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/assets/mario_sprites/smstand.png")
        self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_width()*scale), int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

mario = Mario(200, 200, 0.375)
