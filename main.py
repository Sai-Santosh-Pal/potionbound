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

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprites(dir1, dir2, w, h, d=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]
    # print(images)
    all_sprites = {}
    for img in images:
        spritesheet = pygame.image.load(join(path, img)).convert_alpha()
        sprites = []
        for i in range(spritesheet.get_width()//w):
            surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * w, 0,w, h)
            surface.blit(spritesheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if d:
            all_sprites[img.replace(".png", "") + "_right"] = sprites
            all_sprites[img.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[img.replace(".png", "")] = sprites
    return all_sprites

load_sprites('MainCharacters', 'MaskDude', 10, 10)

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprites("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 1

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

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
        # if self.rect.y > 700:
        #     self.y_vel = 0
        # else:
        #     self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        self.y_vel += min(1, (self.fall_count/fps)*self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.animate()
        

    def draw(self, window):
        # print(self.SPRITES)
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        window.blit(self.sprite, (self.rect.x, self.rect.y))

    def animate(self):
        spritesheet = "idle"
        if self.x_vel != 0:
            spritesheet = "run"
        name = spritesheet + "_" + self.direction
        sprites = self.SPRITES[name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

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