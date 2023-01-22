import pygame

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