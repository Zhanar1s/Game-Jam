import pygame
from spriteclasses import Player
from interaction import Interactable, Object
pygame.init()
screen = pygame.display.set_mode((1200, 675))



bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 675))

clock = pygame.time.Clock()

player = Player(screen, (50,300))
notebook = Object(1, (195, 280, 200, 120), (255,255,255))



#isJump = False
#jumpCount = 5


# animCount = 0

# def drawWindow():
#     global animCount, notebook
#     win.blit(bg, (0, 0))

#     if animCount + 1 >= 30:
#         animCount = 0

#     if left:
#         win.blit(walkLeft[animCount // 5], (x, y))
#         animCount += 1
#     elif right:
#         win.blit(walkRight[animCount // 5], (x, y))
#         animCount += 1
#     else:
#         win.blit(playerStand, (x, y))


    # notebook.interaction(playerStand.get_rect(), win, keys)
    # pygame.display.update()



run = True
while run:
    screen.blit(bg, (0,0))
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            notebook.enable = not notebook.enable

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.blit()
    notebook.interaction(player, screen, keys)

    #if not(isJump):
        #if keys[pygame.K_SPACE]:
            #isJump = True
    #else:
        #if jumpCount >= -5:
            #if jumpCount < 0:
               # y += (jumpCount**2)/2
           # else:
               # y -= (jumpCount**2)/2
            #jumpCount -= 1
        #else:
            #isJump = False
           # jumpCount = 5
    pygame.display.update()
