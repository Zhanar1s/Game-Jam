
import pygame
pygame.init()

class Interactable(pygame.sprite.Sprite):
    def __init__(self, text_speed):
        self.text_speed = text_speed
        self.text_clock = 0
        self.text = [""]
        self.text_index = 0
        self.message = self.text[self.text_index]

        self.font = pygame.font.Font("superlegendboy.ttf", 23)
        self.snip = self.font.render("", True, (255,255,255))

        self.done = False
        self.enable = False

    def interaction(self, player, screen, pressed):
        if self.enable and player.rect.colliderect(self.rect):
        #if self.enable and player.rect.colliderect(self.rect):
            if self.done and self.text_index < len(self.text) - 1 and pressed[pygame.K_z]:
                self.text_index += 1
                self.done = False
                self.text_clock = 0
            self.print_out(screen)
        else:
            self.enable = False
            self.text_clock = 0





    def print_out(self, screen):
        '''
        Function that prints out text in a type writer style
        '''
        self.message = self.text[self.text_index]
        pygame.draw.rect(screen, (0,0,0), [0, 400, screen.get_width(), screen.get_height() - 400])
        pygame.draw.rect(screen, (255,255,255), [0,400, screen.get_width(), screen.get_height()], 5)

        if self.text_clock < self.text_speed * len(self.message):
            self.text_clock += 1
        elif self.text_clock >= self.text_speed * len(self.message):
            self.done = True

        self.snip = self.font.render(self.message[0:self.text_clock // self.text_speed], True, (255,255,255))
        screen.blit(self.snip, (10, 410))




class Object(Interactable):
    def __init__(self, text_speed, rect, rect_color):
        super().__init__(text_speed)
        self.rect_color = rect_color
        self.rect = pygame.Rect(rect)
        self.text = ["An old notebook on a table", "It has some calc notes...", "But most of the pages are torn out", "As if the owner wanted to write somethign else"]
        self.message = self.text[self.text_index]
    
    def blit(self, screen):
        pygame.draw.rect(screen, self.rect_color, self.rect)






        


