import pygame
from spriteclasses import Player
from interaction import Interactable
from lighting import Dim
from menu import *

pygame.init()
screen = pygame.display.set_mode((1200, 675))


bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 675))

clock = pygame.time.Clock()

player = Player(screen, (50,300))
notebook = Interactable(1, (195, 280, 200, 120), (255,255,255), room="room1", item="notebook")
puddle = Interactable(1, (800, 280, 200, 200), (255,255,255), room="room1", item="puddle")
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            notebook.enable = not notebook.enable
            puddle.enable = not puddle.enable

            

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.blit()
    dim.darken(150)

    pygame.draw.circle(screen, (255,255,255), (player.rect.x + 97, player.rect.y + 152), 5)
    notebook.interaction(player, screen, keys)
    puddle.interaction(player, screen, keys)

    pygame.display.update()
