import pygame
import os
pygame.init()

class Light():
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
        self.glow_radius = radius * 2
        
    def draw_source(self, pos, alpha):
        self.pos = pos
        source_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(source_surf, self.color + (alpha,), pos, self.radius)
        return source_surf

    def gen_glow_surf(self, color):
        surf = pygame.Surface((self.glow_radius*2, self.glow_radius*2))
        pygame.draw.circle(surf, color, (self.glow_radius, self.glow_radius), self.glow_radius)
        surf.set_colorkey((0,0,0))
        return surf

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
