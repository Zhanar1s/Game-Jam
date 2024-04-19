import pygame
from typing import Tuple

pygame.init()

class Button():
    '''
    Button class
    Used to create interactive buttons
    Has a class var buttons where all of the instances are stored
    Requires center position, width and height of the button, and the image path
    '''
    main_buttons = []
    settings_buttons = []
    def __init__(self, center: Tuple[int,int], rect_width: int, rect_height: int, image_path: str):
        self.rect = pygame.Rect(center[0]-rect_width/2, center[1]-rect_height/2, rect_width, rect_height)
        self.image = pygame.image.load(image_path)
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def add_to_main_buttons(self):
        Button.main_buttons.append(self)
        Button.main_buttons = Button.main_buttons[-3:]

    def add_to_settings_buttons(self):
        Button.settings_buttons.append(self)
        Button.settings_buttons = Button.settings_buttons[-1:]

    def show(self, screen):
        '''
        Blitting the image of the button on the given pygame surface
        '''
        screen.blit(self.image, self.image_rect)

    def on_hover(self, pos):
        '''
        Implement hover effect here if needed
        '''
        pass

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
        Returning the value of the slider from min to max according to the position of the button part of the slider
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
    title = title_font.render(title_text, True, (255,0,0))
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

    # Load button images
    back_button_img = pygame.image.load('images/buttons/back_button.png')

    # Back button
    back_button = Button((85, 30), 100, 40, 'images/buttons/back_button.png')

    # Audio settings
    audio_img = pygame.image.load('images/buttons/audio_button.png')

    # Slider images
    sfx_slider_img = pygame.image.load('images/buttons/slider_button.png')
    bgm_slider_img = pygame.image.load('images/buttons/slider_button.png')

    sfx_slider = Slider((150, 200), (180, 40), Slider.positions["sfx"])
    bgm_slider = Slider((150,310), (180,40), Slider.positions["bgm"])

    # Settings loop
    while not back:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.rect.collidepoint(event.pos):
                back = True
        screen.fill((0,0,0))
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        # Interactions with sliders
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

        # Back button
        screen.blit(back_button_img, back_button.rect)

        pygame.display.flip()

def game_menu(bgm_channel : pygame.mixer.Channel, sfx_channel : pygame.mixer.Channel, menu_type : str):
    '''
    The function that creates either a main or pause menu
    To create a main menu: specify menu_type = "main", to create a pause menu: menu_type = "pause"
    '''
    loop = True
    to_main_menu = False
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()

    if menu_type == "main":
        title_text = "5 DAY"
    elif menu_type == "pause":
        title_text = "Paused"

    # Create buttons with images
    play_button = Button((600, 400), 200, 50, 'images/buttons/play.png')
    settings_button = Button((600, 500), 200, 50, 'images/buttons/settings.png')
    exit_button = Button((600, 600), 200, 50, 'images/buttons/quit.png')

    for button in (play_button, settings_button, exit_button):
        button.add_to_main_buttons()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.rect.collidepoint(event.pos):
                    exit()
                if settings_button.rect.collidepoint(event.pos):
                    settings(screen, bgm_channel, sfx_channel)
                if play_button.rect.collidepoint(event.pos):
                    loop = False

        screen.fill((0,0,0))
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()

        show_title(screen, title_text)
        for button in Button.main_buttons:
            button.show(screen)
            button.on_hover(pos)
        clock.tick(60)
        pygame.display.flip()

    if to_main_menu:
        game_menu(bgm_channel, sfx_channel, "main")
