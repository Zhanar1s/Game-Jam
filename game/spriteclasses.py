
import pygame
import os
from soundbar import sfx
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

        self.default_image = self.walk_face_images[0]
        self.rect = self.default_image.get_rect(center = pos)
        self.old_x = 0
        self.old_y = 0

        self.speed = 8

        self.moving = {
                "left" : False,
                "right" : False,
                "face" : False,
                "back" : False
        }

        self.walk_count = 0
        #self.up
        #self.down


    def move(self, pressed, lantern):
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        if pressed[pygame.K_UP]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["back"] = True
            self.rect.y = max(self.rect.y - self.speed, 0)
            lantern.pos = (self.rect.x+97, self.rect.y+152)

        elif pressed[pygame.K_DOWN]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["face"] = True
            self.rect.y = min(self.rect.y + self.speed, self.screen.get_height()-self.rect.height)
            lantern.pos = (self.rect.x + 97, self.rect.y + 152)

        elif pressed[pygame.K_LEFT]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["left"] = True
            self.rect.x = max(0, self.rect.x - self.speed)
            lantern.pos = (self.rect.x + 15, self.rect.y + 182)

        elif pressed[pygame.K_RIGHT]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["right"] = True
            self.rect.x = min(self.screen.get_width() - self.rect.width, self.rect.x + self.speed)
            lantern.pos = (self.rect.x + self.rect.width + 30, self.rect.y + 182)
        else:
            self.moving["right"] = False
            self.moving["left"] = False
            self.walk_count = 0
            lantern.pos = (self.rect.x + 97, self.rect.y + 152)


    def blit(self):
        if self.walk_count + 1 >= 60:
            self.walk_count = 0

        if self.moving["left"]:
            self.screen.blit(self.walk_left_images[self.walk_count // 12], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["right"]:
            self.screen.blit(self.walk_right_images[self.walk_count // 12], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["face"]:
            self.screen.blit(self.walk_face_images[self.walk_count // 20], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["back"]:
            self.screen.blit(self.walk_back_images[self.walk_count // 20], (self.rect.x, self.rect.y))
            self.walk_count += 1
        else:
            self.screen.blit(self.default_image, (self.rect.x, self.rect.y))

    def wall_collision(self, walls):
        self.rect.x += (self.rect.x-self.old_x)
<<<<<<< HEAD
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
=======
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))
>>>>>>> original
        for wall in wall_hit_list:
            if (self.rect.x - self.old_x) > 0:
                self.rect.right = wall.rect.left
            elif (self.rect.x - self.old_x) < 0:
                self.rect.left = wall.rect.right

        self.rect.y += (self.rect.y - self.old_y)
<<<<<<< HEAD
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
=======
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))
>>>>>>> original
        for wall in wall_hit_list:
            if (self.rect.y - self.old_y) > 0:
                self.rect.bottom = wall.rect.top
            elif (self.rect.y - self.old_y) < 0:
                self.rect.top = wall.rect.bottom


<<<<<<< HEAD
class Wall(pygame.sprite.Sprite):
    walls = pygame.sprite.Group()
    def __init__(self, topleft, size):
        super().__init__()
        self.x = topleft[0]
        self.y = topleft[1]
        self.width = size[0]
        self.height = size[1]
        self.show = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        Wall.walls.add(self)

    def show_test(self, screen):
        for wall in Wall.walls:
            pygame.draw.rect(screen, (255,255,255), wall.rect, 4)

    @classmethod
    def delete_all(cls):
        cls.walls.empty()

=======
>>>>>>> original
class Witch(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.scare_trigger = False
        self.image =pygame.image.load("images/sprites/monster/monster_big.png")
        self.scream_image = pygame.transform.scale(pygame.image.load("images/sprites/monster/scream.png"), (1280,720))
        self.rect = self.image.get_rect()
        self.sfx = sfx["jumpscare"]

        self.channel = pygame.mixer.Channel(1)

    def scare(self, player):
        self.rect.center = (player.rect.center[0] - 400, player.rect.center[1])
        self.screen.blit(self.image, self.rect)
        self.channel.play(self.sfx)
        pygame.display.flip()
<<<<<<< HEAD
        pygame.time.delay(1000)
=======
        pygame.time.delay((400))
>>>>>>> original
        self.screen.blit(self.scream_image, (0,0))
        pygame.display.flip()
        pygame.time.delay((2000))
        self.scare_trigger = False
        


class Door():
    def __init__(self, screen, pos):
        self.screen = screen

        self.closed_image = pygame.image.load("images/door/door (1).png")
        self.open_image = pygame.image.load("images/door/door (2).png")
        self.opened = False
        self.current_image = self.closed_image

        self.pos = pos
        self.rect = self.current_image.get_rect(topleft=pos)

        self.audio_channel = pygame.mixer.Channel(2)

    def blit(self):
        self.screen.blit(self.current_image, self.rect)

    def open_door(self):
        if not self.opened:
            self.audio_channel.play(sfx["dooropen"])
            self.current_image = self.open_image
            self.opened = True

    def close_door(self):
        if self.opened:
            self.audio_channel.play(sfx["doorclose"])
            self.current_image = self.closed_image
            self.opened = False
<<<<<<< HEAD
=======



class Wall(pygame.sprite.Sprite):
    #walls = pygame.sprite.Group()

    walls = {
        "room1" : [],
        "room2" : [],
        "room3" : [],
        "room4" : [],
        "room5" : [],
        "room6" : [],
        "room7" : [],
    }
    def __init__(self, topleft, size, room):
        super().__init__()
        self.x = topleft[0]
        self.y = topleft[1]
        self.width = size[0]
        self.height = size[1]
        self.show = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        Wall.walls[room].append(self)

    def show_test(self, screen, room):
        for wall in Wall.walls[room]:
            pygame.draw.rect(screen, (255,255,255), wall.rect, 4)

    @classmethod
    def delete_all(cls, room):
        cls.walls[room] = []
>>>>>>> original
