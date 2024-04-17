import pygame
import os
pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self, screen, pos):
        
        super().__init__()
        self.screen = screen


        self.walk_left_images = [
            pygame.image.load('images/sprites/Boy/left/' + x) for x in os.listdir('images/sprites/Boy/left')
        ]

        self.walk_right_images = [
            pygame.image.load('images/sprites/Boy/right/' + x) for x in os.listdir('images/sprites/Boy/right')
        ]
        
        self.walk_face_images = [
            pygame.image.load('images/sprites/Boy/face/' + x) for x in os.listdir('images/sprites/Boy/face')
        ]        
        
        self.walk_back_images = [
            pygame.image.load('images/sprites/Boy/back/' +x) for x in os.listdir('images/sprites/Boy/back')
        ]

        self.cur_image = self.walk_face_images[0]
        self.rect = self.cur_image.get_rect(center = pos)

        self.speed = 5

        self.moving = True
        self.left = True
        self.right = False
        self.walk_count = 0
        #self.up
        #self.down


    def move(self, pressed):
        if not self.moving:
            return
        if pressed[pygame.K_UP]:
            self.rect.y = max(self.rect.y - 5, 0 + 150)
            self.cur_image = self.walk_face_images[self.walk_count]
        elif pressed[pygame.K_DOWN]:
            self.rect.y = min(self.rect.y + 5, self.screen.get_height()-self.rect.height)
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= 5
        elif pressed[pygame.K_RIGHT]:
            self.rect.x += 5


    def blit(self):
        self.screen.blit(self.cur_image, self.rect)


class Wall:
    def __init__(self, topleft, size, color):
        self.color = color
        self.x = topleft[0]
        self.y = topleft[1]
        self.width = size[0]
        self.height = size[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def place(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


            

