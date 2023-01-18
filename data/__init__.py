""" GAME LOOP """
import pygame
import player

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mario SUPERCHARGED')



run = True
while run:
    player.mario.draw(screen)

    for event in pygame.event.get():
		# Quit game
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()