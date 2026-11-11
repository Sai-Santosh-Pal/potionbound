import pygame
import os, random, math
from os import listdir
from os.path import isfile, join

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
 
player_vel = 5
player_jump =  1

pygame.init()
pygame.display.set_caption("Potionbound")
window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_bg(color):
    image = pygame.image.load(join("assets", "Background", color))
    x, y, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT//height + 1):
            pos = [i*width, j*height]
            tiles.append(pos)
    
    return tiles, image

def draw(window, bg_list, img):
    for tile in bg_list:
        window.blit(img, tuple(tile))
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    bg, bg_img = get_bg("Green.png")
    run = True
    while run:
        draw(window, bg, bg_img)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)