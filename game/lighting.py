import pygame
import os
pygame.init()

class Light():
    def __init__(self, screen, color, radius, pos):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.pos = pos

    def blit(self, glow_color, size):
        
        surf = pygame.Surface((self.radius*size*2, self.radius*size*2))
        pygame.draw.circle(surf, glow_color, (self.radius*size, self.radius*size), self.radius * size)
        surf.set_colorkey((0,0,0))

        self.screen.blit(surf, (self.pos[0] - self.radius * size, self.pos[1] - self.radius * size), special_flags = pygame.BLEND_RGB_ADD)

class Dim():
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.to_fade = False

    def darken(self, alpha):
        self.black_surface = pygame.Surface((self.width, self.height))
        self.black_surface.fill((0,0,0))
        self.black_surface.set_alpha(alpha)
        self.screen.blit(self.black_surface, (0,0))

    def fade(self):
        if self.to_fade:
            fade = pygame.Surface((self.width, self.height))
            fade.fill((0,0,0))

            for alpha in range(0,300,2):
                fade.set_alpha(alpha)
                self.screen.blit(fade, (0,0))
                pygame.display.update()
                pygame.time.delay(5)
            self.to_fade = False
