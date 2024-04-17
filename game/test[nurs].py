import pygame
from spriteclasses import Player
from interaction import Interactable, Object
pygame.init()
screen = pygame.display.set_mode((1200, 675))



bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 675))

clock = pygame.time.Clock()

player = Player(screen, (50,300))
notebook = Object(1, (195, 280, 200, 120), (255,255,255))





run = True
while run:
    screen.blit(bg, (0,0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            notebook.enable = not notebook.enable

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.blit()
    notebook.interaction(player, screen, keys)
    screen.blit()


    pygame.display.update()
