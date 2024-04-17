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
    def __init__(self, center : Tuple[int,int], rect_width : int, rect_height : int, text : str, text_color : Tuple[int,int,int], size : int):
        self.rect = pygame.Rect(center[0]-rect_width/2, center[1] - rect_height/2, rect_width, rect_height)
        self.rect_color = (150,150,150) 
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center = self.rect.center)
    
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
        pygame.draw.rect(screen, self.rect_color, self.rect)
        screen.blit(self.text, self.text_rect)

    def on_hover(self, pos):
        '''
        Slightly dimming the button's color when the mouse is hover on it
        '''
        if self.rect.collidepoint(pos):
            self.rect_color = (50,50,50)
        else:
            self.rect_color = (100,100,100)

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


def show_title(screen, title_text):
    '''
    Simply blits the title on the screen
    Also used to display Paused when the game is paused
    '''
    title_font = pygame.font.Font(None, 100)
    title_rect = pygame.Rect(250,150, 700,100)
    title = title_font.render(title_text, True, (255,255,255))
    screen.blit(title, title.get_rect(center = title_rect.center))

def settings(screen, bgm_channel, sfx_channel):
    '''
    A function that opens up a settings menu
    Inside of it, one can change the volume, view the stats and change the color of the player
    By default, returns the player's color (if not selected, just the white color)
    '''
    back = False
    #font
    settings_font = pygame.font.Font(None, 40)
    settings_font_s = pygame.font.Font(None, 24)
    #back button
    back_rect = pygame.Rect(85, 30, 100 ,40)
    back_text = settings_font.render("Back", True, (255,255,255))

    #audio settings 
    audio_rect = pygame.Rect(60, 100, 100, 60)
    audio_text = settings_font.render("Audio settings", True, (255,255,255))
    sfx_rect = pygame.Rect(60, 150, 100, 30)
    sfx_text = settings_font_s.render("SFX volume", True, (255,255,255))
    sfx_slider = Slider((150, 200), (180, 40), Slider.positions["sfx"])
    bgm_rect = pygame.Rect(60, 260, 100, 30)
    bgm_text = settings_font_s.render("BGM volume", True, (255,255,255))
    bgm_slider = Slider((150,310), (180,40), Slider.positions["bgm"])




    #settings loop
    while not back:
        for event in pygame.event.get():
            #if we want to quit or return, we do not use quit or exit because we still need to write the stats to the json file
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and (back_trio.collidepoint(event.pos) or back_rect.collidepoint(event.pos)):
                back = True
        screen.fill((0,0,0))
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        
        #interations with sliders
        if sfx_slider.slider_rect.collidepoint(mouse_pos) and pressed[0]:
            sfx_slider.move(mouse_pos)
            Slider.positions["sfx"] = sfx_slider.get_value()
            sfx_channel.set_volume(sfx_slider.get_value())

        elif bgm_slider.slider_rect.collidepoint(mouse_pos) and pressed[0]:
            bgm_slider.move(mouse_pos)
            Slider.positions["bgm"] = bgm_slider.get_value()
            bgm_channel.set_volume(bgm_slider.get_value())


        
        
        sfx_slider.render(screen)
        bgm_slider.render(screen)
        #back function text and button
        screen.blit(back_text, back_rect)
        back_trio = pygame.draw.polygon(screen, (255,255,255), [(30,40),(80,60),(80,20)])
        #audio settings text
        screen.blit(audio_text, audio_rect)
        screen.blit(sfx_text, sfx_rect)
        screen.blit(bgm_text, bgm_rect)
        #displaying stats




        
        pygame.display.flip()


def game_menu(bgm_channel : pygame.mixer.Channel, sfx_channel : pygame.mixer.Channel, menu_type : str):
    '''
    The function that creates either a main or pause menu
    To create a main menu: specify menu_type = "main", to create a pause menu: menu_type = "pause"
    Requires stats_dict (a dictionary of stats extracted from the json file), bgm and sfx channels (audio channels)

    '''
    loop = True
    to_main_menu = False
    screen = pygame.display.set_mode((1200,675))
    clock = pygame.time.Clock()

    if menu_type == "main":
        play_text = "play"
        title_text = "Game"
    elif menu_type == "pause":
        play_text = "resume"
        title_text = "Paused"

    #creating the buttons
    play_button = Button((600,400), 700, 80, play_text, (255,255,255), 62)
    settings_button = Button((600,500), 700, 80, "settings", (255,255,255), 62)
    exit_button = Button((600,600), 700, 80, "exit", (255,255,255), 62)

    for button in (play_button, settings_button, exit_button):
        button.add_to_main_buttons()


    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.rect.collidepoint(event.pos):
                    exit()
                if play_button.rect.collidepoint(event.pos):
                    loop = False
                    
        screen.fill((0,0,0))
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        
        if pressed[0] and settings_button.rect.collidepoint(pos):
            settings(screen, bgm_channel, sfx_channel)


        show_title(screen, title_text)
        for button in Button.main_buttons:
            button.show(screen)
            button.on_hover(pos)
        clock.tick(60)
        pygame.display.flip()
    
    if to_main_menu:
        game_menu(bgm_channel, sfx_channel, "main")
    
