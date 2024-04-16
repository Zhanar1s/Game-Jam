import pygame
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
playerStand = pygame.transform.scale(pygame.image.load('images/sprites/Boy/face/1.png'), (125, 201))


clock = pygame.time.Clock()


x = 50
y = 380
width = 170
height = 201
speed = 5

left = False
right = False
up = False
down = False
animCount = 0

def drawWindow():
    global animCount
    win.blit(bg, (0, 0))

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
    elif keys[pygame.K_UP] and y > 5:
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
