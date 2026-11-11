import pygame
import os, random, math
from os import listdir
from os.path import isfile, join

bg_color = (255, 255, 255)
width, height = 1000, 800
fps = 60
 
player_vel = 5
player_jump =  1

pygame.init()
pygame.display.set_caption("Potionbound")
window = pygame.display.set_mode((width, height))

def main(window):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()
            
            

if __name__ == "__main__":
    main(window)