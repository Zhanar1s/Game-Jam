import pygame
pygame.init()
win = pygame.display.set_mode((1200, 600))

walkRight = [
	pygame.transform.scale(pygame.image.load('images/boy_right.png'),(125,156)),
    pygame.transform.scale(pygame.image.load('images/boy_right_1.png'),(125,156)),
    pygame.transform.scale(pygame.image.load('images/boy_right_2.png'),(125, 156)),
    pygame.transform.scale(pygame.image.load('images/boy_left.png'),(125, 156)),pygame.transform.scale(pygame.image.load('images/boy_left_1.png'),(125, 156)),
    pygame.transform.scale(pygame.image.load('images/boy_left_2.png'), (125, 156)),

]

walkLeft = [
    pygame.transform.scale(pygame.image.load('images/boy_right.png'),(125,156)),
    pygame.transform.scale(pygame.image.load('images/boy_right_1.png'),(125,156)),
    pygame.transform.scale(pygame.image.load('images/boy_right_2.png'),(125, 156)),
    pygame.transform.scale(pygame.image.load('images/boy_left.png'),(125, 156)),pygame.transform.scale(pygame.image.load('images/boy_left_1.png'),(125, 156)),
    pygame.transform.scale(pygame.image.load('images/boy_left_2.png'), (125, 156)),

]

bg = pygame.image.load('images/backround.jpg')
playerStand = pygame.transform.scale(pygame.image.load('images/boy.png'), (125, 156))

clock = pygame.time.Clock()


x = 50
y = 425
width = 125
height = 156
speed = 5

isJump = False
jumpCount = 5

left = False
right = False
animCount = 0

def drawWindow():
    global animCount
    win.blit(bg, (0, 0))

    if animCount + 1 >= 30:
        animCount = 0

    if left:
        win.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x, y))
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
    elif keys[pygame.K_RIGHT] and x < 1200 - width - 5:
        x += speed
        left = False
        right = True
    else:
        left = False
        right = False
        animCount = 0

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -5:
            if jumpCount < 0:
                y += (jumpCount**2)/2
            else:
                y -= (jumpCount**2)/2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 5
    drawWindow()
