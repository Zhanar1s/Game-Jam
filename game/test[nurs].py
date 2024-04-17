import pygame
from spriteclasses import Player, Door
from interaction import Interactable
from lighting import Dim
from menu import *

pygame.init()
screen = pygame.display.set_mode((1200, 675))


bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 675))

clock = pygame.time.Clock()

player = Player(screen, (50,300))
notebook = Interactable(1, (195, 280, 250, 120), (255,255,255), room="room1", item="notebook")
puddle = Interactable(1, (950, 280, 200, 200), (255,255,255), room="room1", item="puddle")
door = Door(screen, (600,60))
dim = Dim(screen)


bgm_channel = pygame.mixer.Channel(0)
sfx_channel = pygame.mixer.Channel(1)

run = True

game_menu(bgm_channel, sfx_channel, "main")

while run:
    screen.blit(bg, (0,0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if notebook.rect.colliderect(player.rect):
                    notebook.enable = True
                if puddle.rect.colliderect(player.rect):
                    puddle.enable = True
                if door.rect.colliderect(player.rect):
                    door.open_door(player)
            if event.key == pygame.K_ESCAPE:
                game_menu(bgm_channel, sfx_channel, "pause")
            

            

    keys = pygame.key.get_pressed()
    player.move(keys, Interactable.all_object_rects)

    door.blit()
    player.blit()

    dim.darken(150)

    pygame.draw.circle(screen, (255,255,255), (player.rect.x + 97, player.rect.y + 152), 5)
    notebook.interaction(player, screen, keys)
    puddle.interaction(player, screen, keys)

    pygame.display.update()
