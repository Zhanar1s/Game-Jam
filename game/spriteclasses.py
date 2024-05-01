
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
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))
        for wall in wall_hit_list:
            if (self.rect.x - self.old_x) > 0:
                self.rect.right = wall.rect.left
            elif (self.rect.x - self.old_x) < 0:
                self.rect.left = wall.rect.right

        self.rect.y += (self.rect.y - self.old_y)
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))

        for wall in wall_hit_list:
            if (self.rect.y - self.old_y) > 0:
                self.rect.bottom = wall.rect.top
            elif (self.rect.y - self.old_y) < 0:
                self.rect.top = wall.rect.bottom


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
        #placing the jumpsace slightly to the left of the player
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        self.rect.center = (screen_center_x, screen_center_y)
        self.screen.blit(self.image, self.rect)
        self.channel.play(self.sfx) #playing the sound effect of the screamer
        pygame.display.flip()
        pygame.time.delay(1000) #delaying the screen for 1 second
        self.screen.blit(self.scream_image, (0,0)) #blitting the close-up of the screamer
        pygame.display.flip()
        pygame.time.delay((2000))   #delaying the screen for 2 second
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
        pass
        #for wall in Wall.walls[room]:
            #pygame.draw.rect(screen, (255,255,255), wall.rect, 4)

    @classmethod
    def delete_all(cls, room):
        cls.walls[room] = []

class Monster(pygame.sprite.Sprite):
    image = pygame.image.load('images/sprites/monster/monster0.png')
    '''
    The Monster class makes a monster that can move towards and follow the player in the game. It helps make the game more exciting by adding a moving challenge.
    '''
    def __init__(self, screen, pos):
        super().__init__()
        self.screen = screen
        self.rect = self.image.get_rect(center = pos)
        self.speed = 2
        self.laughter_channel = pygame.mixer.Channel(1)

    def update(self, player_pos):
        # Calculate direction to the player

        player_x, player_y = player_pos
        monster_x, monster_y = self.rect.center

        delta_x = player_x - monster_x
        delta_y = player_y - monster_y
        ranges = (delta_x**2 + delta_y**2)**0.5

        if self.speed > 0:
            if not self.laughter_channel.get_busy():
                self.laughter_channel.play(sfx["laughter"], -1)
        else:
            self.laughter_channel.stop()


        if ranges > 0 and self.speed >0: # Make sure the monster only moves when there is distance available
            vector_delta_x = delta_x / ranges
            vector_delta_y = delta_y / ranges
            self.rect.x += vector_delta_x * self.speed
            self.rect.y += vector_delta_y * self.speed

class Timer:
    def __init__(self, screen, font_path, font_size, duration):
        self.screen = screen
        self.font = pygame.font.Font(font_path, font_size)
        self.duration = duration * 1000
        self.start_time = None
        self.finished = False
        self.active = False
        self.used = False
        self.timer_channel = pygame.mixer.Channel(2)

    def start(self):
        if not self.active:
            self.start_time = pygame.time.get_ticks()
            self.finished = False
            self.active = True
            self.timer_channel.play(sfx["timer"],-1)

    def update(self):

        if self.start_time is not None and not self.finished:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.finished = True
                self.active = False
                self.used = True
                self.timer_channel.stop()

    def draw(self):
        """
        Draw the remaining time on the screen if the timer is running.
        """
        if self.start_time is not None and not self.finished:
            remaining_time = max(0, self.duration - (pygame.time.get_ticks() - self.start_time))
            seconds = remaining_time // 1000
            time_text = self.font.render(f'{seconds} seconds left', True, (255, 0, 0))
            self.screen.blit(time_text, (50, 50))  # Adjust position as needed

    def is_finished(self):
        """
        Check if the timer has finished.
        """
        return self.finished

    def reset(self):
        if not self.used:
            """
            Reset the timer to allow it to be started again.
            """
            self.start_time = None
            self.finished = False
            self.active = False
    def stop(self):
        """Stop the timer and its associated sound."""
        self.active = False
        self.timer_channel.stop()
