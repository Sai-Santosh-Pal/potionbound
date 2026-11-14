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
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.jump_intensity = 10
        self.hit = False 
        self.hit_count = 0

    def is_hit(self):
        self.hit = True
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * self.jump_intensity
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
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
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit =  False
            self.hit = 0
        self.fall_count += 1
        self.animate()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self, window, offset_x, offset_y):
        # print(self.SPRITES)
        # self.sprite = self.SPRITES["idle_" + self.direction][0]
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
    
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def animate(self):
        spritesheet = "idle"
        if self.hit:
            spritesheet = "hit"
        if self.y_vel < 0:
            if self.jump_count == 1:
                spritesheet = "jump"
            elif self.jump_count == 2:
                spritesheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            spritesheet = "fall"
        elif self.x_vel != 0:
            spritesheet = "run"
        name = spritesheet + "_" + self.direction
        sprites = self.SPRITES[name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window, offset_x, offset_y):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

def get_block(size):
    path = join("assets", "Terrain", "Green Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(272, 64, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprites("Green Traps", "Fire", width, height)
        print(self.fire)
        self.image = self.fire["off"][0]
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"
    
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

def draw(window, bg_list, img, player, objects, offset_x, offset_y):
    for tile in bg_list:
        window.blit(img, tuple(tile))
    for obj in objects:
        obj.draw(window, offset_x, offset_y)
    player.draw(window, offset_x, offset_y)
    pygame.display.update()

def collision_vertical(player, objects, dy):
    collided = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided.append(obj)
    return collided

def check_collision(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided

def movement(player, objects):
    key = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = check_collision(player, objects, -player_vel )
    collide_right = check_collision(player, objects, player_vel)
    if key[pygame.K_LEFT] and not collide_left:
        player.move_left(player_vel)
    if key[pygame.K_RIGHT] and not collide_right:
        player.move_right(player_vel)
    collide_vertical = collision_vertical(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *collide_vertical]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.is_hit()

def main(window):
    clock = pygame.time.Clock()
    bg, bg_img = get_bg("Green.png")
    run = True
    player = Player(100, 200, 50, 50)
    block_size = 96
    floor_dimension = HEIGHT + 30
    fire = Fire(100, floor_dimension - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i*block_size, floor_dimension - block_size, block_size) for i in range(-WIDTH//block_size, (WIDTH*2)//block_size)]
    floor_layer2 = [Block(i*block_size, floor_dimension - block_size*2, block_size) for i in range(-WIDTH//block_size, (WIDTH*2)//block_size)]
    # blocks = [Block(0,HEIGHT - block_size, block_size)]
    offset_x = 0
    offset_y = 0
    objects = [*floor, Block(0, floor_dimension - block_size*2, block_size), Block(block_size*3, floor_dimension - block_size*4, block_size), Block(block_size*3, floor_dimension - block_size*5, block_size), Block(block_size*2, floor_dimension - block_size*7, block_size), fire]
    scroll_area_w = 200
    scroll_area_h = 120
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        player.loop(FPS)
        fire.loop()
        movement(player, objects)
        # collision_vertical(player, floor, 1)
        draw(window, bg, bg_img, player, objects, offset_x, offset_y)
        if (player.rect.right - offset_x >= WIDTH - scroll_area_w and player.x_vel > 0) or (player.rect.left - offset_x <= scroll_area_w and player.x_vel < 0):
            offset_x += player.x_vel
        if (player.rect.top - offset_y >= HEIGHT - scroll_area_h and player.y_vel > 0) or (player.rect.bottom - offset_y <= scroll_area_h and player.y_vel < 0):
            offset_y += player.y_vel
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)