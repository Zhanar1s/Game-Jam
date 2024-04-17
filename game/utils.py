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


