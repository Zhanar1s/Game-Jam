
import pygame
import json
import re
pygame.init()

with open("text/dialogs.json", "r") as json_data:
    dialog_data = json.load(json_data)

class Interactable(pygame.sprite.Sprite):

    '''
    Class for object interaction
    '''
    all_object_rects = []
    def __init__(self, text_speed, rect, room, item):
        self.text_speed = text_speed
        self.text_clock = 0
        self.text_index = 0
        self.text = dialog_data[room][item]
        self.message = self.text[self.text_index]

        self.rect = pygame.Rect(rect)

        self.font = pygame.font.SysFont("superlegendboy", 23)
        self.snip = self.font.render("", True, (255,255,255))

        self.done = False
        self.enable = False
        self.finished = False

        Interactable.all_object_rects.append(self.rect)

    def interaction(self, player, screen, pressed):
        '''
        Identifying if player interacted with an object and calls a rpint_out function to display correpsonding text
        '''
        if self.text_index == len(self.text) - 1:
            self.finished = True


        if player.rect.colliderect(self.rect):

            if self.enable:
                if self.done and self.text_index < len(self.text) - 1 and pressed[pygame.K_z]:
                    self.text_index += 1
                    self.done = False
                    self.text_clock = 0
                self.print_out(screen)

        else:
            self.text_clock = 0
            self.enable = False


    def print_out(self, screen):
        '''
        Function that prints out text in a type writer style
        '''
        self.message = self.text[self.text_index]
        pygame.draw.rect(screen, (0,0,0), [0, 500, screen.get_width(), screen.get_height() - 500])
        pygame.draw.rect(screen, (255,255,255), [0,500, screen.get_width(), screen.get_height()-500], 5)

        if self.text_clock < self.text_speed * len(self.message):
            self.text_clock += 1
        elif self.text_clock >= self.text_speed * len(self.message):
            self.done = True

        self.snip = self.font.render(self.message[0:self.text_clock // self.text_speed], True, (255,255,255))

        screen.blit(self.snip, (10, 510))


    def blit(self, screen):
        pygame.draw.rect(screen, self.rect_color, self.rect)



class Note(Interactable):
    '''
    Child class of Interactable. Used to display paper notes
    '''
    def __init__(self, text_speed, rect, room, item):
        super().__init__(text_speed, rect, room, item)
        self.image = pygame.image.load("images/items/paper.png")
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

#spoiler alert! this part spoils the entire plot. keep that in mind        

class Friend(Interactable):
    def __init__(self, text_speed):
        self.images = [pygame.image.load("images/sprites/friend/friendread.png"),
                       pygame.image.load("images/sprites/friend/friendneutral.png"),
                       pygame.image.load("images/sprites/friend/friendmad.png"),
                       pygame.image.load("images/sprites/friend/friendsmile.png")]
        self.image = self.images[1]
        self.rect = self.image.get_rect(center = (1000, 600))
        super().__init__(text_speed, (0,0,1280,720), "university", "friend")

    

    def print_out(self, screen):
        '''
        Function that prints out text in a type writer style
        '''
        self.message = self.text[self.text_index]
        if self.text_index > 3 and self.text_index not in (5,8,11,16) and self.text_index < 26:
            if self.text_index == 6:
                self.image = self.images[2]
            if self.text_index == 10:
                self.image = self.images[1]
            if self.text_index == 23:
                self.image = self.images[3]
            screen.blit(self.image, self.rect)

            pygame.draw.rect(screen, (0,0,0), (1100, 460, 180, 40))
            pygame.draw.rect(screen, (255,255,255), (1100, 460, 180, 40), 3)
            screen.blit(self.font.render("Asem", True, (255,255,255)), (1110, 470))
        pygame.draw.rect(screen, (0,0,0), [0, 500, 1280, 720 - 500])
        pygame.draw.rect(screen, (255,255,255), [0,500, 1280, 720-500], 5)

        if self.text_clock < self.text_speed * len(self.message):
            self.text_clock += 1
        elif self.text_clock >= self.text_speed * len(self.message):
            self.done = True

        self.snip = self.font.render(self.message[0:self.text_clock // self.text_speed], True, (255,255,255))

        screen.blit(self.snip, (10, 510))