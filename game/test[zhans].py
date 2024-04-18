import pygame
import time
pygame.init()
win = pygame.display.set_mode((1200, 600))

walkRight = [
	pygame.transform.scale(pygame.image.load('images/sprites/Boy/right/1.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/right/2.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/right/3.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/right/4.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/right/5.png'), (170, 201)),

]

walkUp = [
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/back/1.png'),(125,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/back/2.png'),(125,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/back/3.png'),(125, 201))
]

walkLeft = [
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/left/1.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/left/2.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/left/3.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/left/4.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/left/5.png'), (170, 201)),

]

walkDown = [
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/face/1.png'),(125,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/face/2.png'),(125,201)),
    pygame.transform.scale(pygame.image.load('images/sprites/Boy/face/3.png'),(125, 201))
]



bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 600))
bg1 = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 600))
playerStand = pygame.transform.scale(pygame.image.load('images/sprites/Boy/face/1.png'), (125, 201))

door = pygame.transform.scale(pygame.image.load('images/door/door (1).png'), (220, 285))
win.blit(door, (500, 500))
door_open = pygame.transform.scale(pygame.image.load('images/door/door (2).png'), (220, 285))

in_door_open = False


clock = pygame.time.Clock()


x = 50
y = 380
width = 125
height = 201
speed = 5

left = False
right = False
up = False
down = False
animCount = 0

def drawWindow():
    global in_door_open
    global animCount


    if in_door_open:

        win.blit(bg1, (0, 0))
        #win.blit(door_open, (900, 100))


    else:
        win.blit(bg, (0, 0))
        win.blit(door, (900, 100))

    if animCount + 1 >= 30:
        animCount = 0

    if left:
        win.blit(walkLeft[animCount // 6], (x, y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 6], (x, y))
        animCount += 1
    elif up:
        win.blit(walkUp[animCount // 10], (x, y))
        animCount += 1
    elif down:
        win.blit(walkDown[animCount // 10], (x, y))
        animCount += 1




    else:
        win.blit(playerStand, (x, y))

    pygame.display.update()



run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and (x > 900) and (y < 151):
                win.blit(door_open, (900, 100))
                pygame.display.update()
                time.sleep(1)
                in_door_open = not in_door_open
                if in_door_open:
                    x, y = 50, 380


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        up = False
        down = False
    elif keys[pygame.K_RIGHT] and x < 1200 - width - 5:
        x += speed
        left = False
        right = True
        up = False
        down = False
    elif keys[pygame.K_UP] and y > 150:
        y -= speed
        left = False
        right = False
        up = True
        down = False
    elif keys[pygame.K_DOWN] and y < 600 - height - 5:
        y += speed
        left = False
        right = False
        up = False
        down = True

    else:
        left = False
        right = False
        animCount = 0


    drawWindow()
