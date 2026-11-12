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

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, self.rect)

    

def draw(window, bg_list, img, player):
    for tile in bg_list:
        window.blit(img, tuple(tile))
    player.draw(window)
    pygame.display.update()

def movement(player):
    key = pygame.key.get_pressed()
    player.x_vel = 0
    if key[pygame.K_LEFT]:
        player.move_left(player_vel)
    if key[pygame.K_RIGHT]:
        player.move_right(player_vel)



def main(window):
    clock = pygame.time.Clock()
    bg, bg_img = get_bg("Green.png")
    run = True
    player = Player(100, 200, 50, 50)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
        movement(player)
        draw(window, bg, bg_img, player)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)