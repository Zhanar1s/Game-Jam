import pygame
from typing import Tuple

pygame.init()


class Button():
    '''
    Button class
    Used to create interactive buttons
    Has a class var buttons where all of the instances are stored
    Requires center position, width and height of the btton, the displayed text, its color and font's size
    '''
    main_buttons = []
    settings_buttons = []
    def __init__(self, center : Tuple[int,int], image):
        self.center = center
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = self.center)
    
    def add_to_main_buttons(self):
        Button.main_buttons.append(self)
        Button.main_buttons = Button.main_buttons[-3:]
    def add_to_settings_buttons(self):
        Button.settings_buttons.append(self)
        Button.settings_buttons = Button.settings_buttons[-1:]

    def show(self, screen):
        '''
        Blitting the text on the button on the given pygame surface
        '''
        screen.blit(self.image, self.rect)

    def on_hover(self, screen, pos):
        '''
        Slightly dimming the button's color when the mouse is hover on it
        '''
        black_surface = pygame.Surface((self.rect.width, self.rect.height))
        black_surface.fill((0,0,0))
        if self.rect.collidepoint(pos):
            black_surface.set_alpha(100)
        else:
            black_surface.set_alpha(0)
        screen.blit(black_surface, self.rect.topleft)

class Slider():
    positions = {"bgm" : 0.5, "sfx" : 0.5}
    '''
    Slider class.
    Used to create slider to regulate volume values
    Class variable positions contains the positions at which the sliders were left off
    Initialized with the following params: center position, size (width, height), and initial value
    '''
    def __init__(self, pos : Tuple[int,int], size : Tuple[int,int], init_val : float):
        self.pos = pos
        self.size = size

        self.slider_left = self.pos[0] - (size[0]//2)
        self.slider_right = self.pos[0] + (size[0]//2)
        self.slider_top = self.pos[1] - (size[1]//2)
        
        self.min = 0.0
        self.max = 1.0
        self.init_val = (self.slider_right - self.slider_left)*init_val

        self.slider_rect = pygame.Rect(self.slider_left, self.slider_top, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left + self.init_val - 5, self.slider_top, 10, self.size[1])

    def move(self, mouse_pos):
        '''
        Moving the slider's button part to the mouse position
        '''
        self.button_rect.centerx = mouse_pos[0]

    def render(self, screen):
        '''
        Drawing the slider on the surface
        '''
        pygame.draw.rect(screen, (169,169,169), self.slider_rect)
        pygame.draw.rect(screen, (0,0,155), self.button_rect)
    
    def get_value(self) -> float:
        '''
        Returing the value of the slider from min to max according to the position of the button part of the slider
        '''
        val_range = self.slider_right - self.slider_left - 1
        button_val = self.button_rect.centerx - self.slider_left

        return (button_val/val_range)*(self.max - self.min) + self.min

