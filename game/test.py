import pygame
pygame.init()
win = pygame.display.set_mode((1200, 600))

walkRight = [
	pygame.transform.scale(pygame.image.load('images/boy_right/boy_right.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/boy_right/boy_right_1.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/boy_right/boy_right_2.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/boy_right/boy_right_3.png'),(170, 201)),pygame.transform.scale(pygame.image.load('images/boy_right/boy_right_4.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/boy_right/boy_right_5.png'), (170, 201)),

]

walkLeft = [
    pygame.transform.scale(pygame.image.load('images/boy_left/boy_left.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/boy_left/boy_left_1.png'),(170,201)),
    pygame.transform.scale(pygame.image.load('images/boy_left/boy_left_2.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/boy_left/boy_left_3.png'),(170, 201)),pygame.transform.scale(pygame.image.load('images/boy_left/boy_left_4.png'),(170, 201)),
    pygame.transform.scale(pygame.image.load('images/boy_left/boy_left_5.png'), (170, 201)),

]

bg = pygame.transform.scale(pygame.image.load('images/background.png'), (1200, 600))
playerStand = pygame.transform.scale(pygame.image.load('images/boy.png'), (170, 201))

clock = pygame.time.Clock()


x = 50
y = 380
width = 170
height = 201
speed = 5

#isJump = False
#jumpCount = 5

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
    drawWindow()
