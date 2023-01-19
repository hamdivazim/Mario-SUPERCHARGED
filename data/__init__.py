""" GAME LOOP """
import pygame
import player
import controls

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mario SUPERCHARGED')

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Colours
BG = (8, 234, 255)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

run = True
while run:
    clock.tick(FPS)

    draw_bg()

    player.mario.update_animation()
    player.mario.draw(screen)

    # Update player actions
    if player.mario.alive:
        player.mario.vel_x *= 0.8
        if abs(player.mario.vel_x) < 0.01:
            player.mario.vel_x = 0
        player.mario.rect.x += ((player.mario.vel_x*5)*player.mario.direction)

        if player.mario.in_air:
            if player.mario.vel_y > 0:
                player.mario.update_action(3)
            else:
                player.mario.update_action(2)
        elif player.moving_left or player.moving_right:
            player.mario.update_action(1)
        else:
            player.mario.update_action(0)

    player.mario.move(player.moving_left, player.moving_right)

    for event in pygame.event.get():
		# Quit game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if controls.left_down(event.key):
                player.moving_left = True
            if controls.right_down(event.key):
                player.moving_right = True
            if controls.up_down(event.key) and player.mario.alive:
                player.mario.jump = True

        if event.type == pygame.KEYUP:
            if controls.left_down(event.key):
                player.moving_left = False
                player.mario.vel_x = 0
            if controls.right_down(event.key):
                player.moving_right = False
                player.mario.vel_x = 0


    pygame.display.update()

pygame.quit()