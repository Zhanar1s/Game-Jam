import pygame
from utils import Button, Slider

class Menu():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load("images/buttons/menu_back.png"), (1280,720))

        self.play_button = Button((640,400), "images/buttons/play.png")
        self.settings_button = Button((640,500), "images/buttons/settings.png")
        self.exit_button = Button((640,600), "images/buttons/quit.png")

        self.title = pygame.image.load("images/buttons/gone.png")
        self.title_rect = self.title.get_rect(center = (640, 240))
        self.prev_scene = "intro"

        for button in (self.play_button, self.exit_button, self.settings_button):
            button.add_to_main_buttons()


    def run(self):

        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.screen.fill((0,0,0))
        self.screen.blit(self.bg, (0,0))

        if pressed[0]:
            if self.settings_button.rect.collidepoint(mouse_pos):
                self.scene_manager.set_scene("settings")
            elif self.exit_button.rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()
            elif self.play_button.rect.collidepoint(mouse_pos):
                # self.scene_manager.set_scene("finale")
                self.scene_manager.set_scene(self.scene_manager.prev_scene)

        self.screen.blit(self.title, self.title.get_rect(center = self.title_rect.center))

        for button in Button.main_buttons:
            button.show(self.screen)
            button.on_hover(self.screen, mouse_pos)
        

class Settings():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

        #font
        self.settings_font = pygame.font.SysFont("superlegendboy", 50)
        self.settings_font_s = pygame.font.SysFont("superlegendboy", 30)
        #back button
        self.back = pygame.image.load("images/buttons/back.png")
        self.back_rect = self.back.get_rect(center = (100,40))

        #audio settings 
        self.audio_rect = pygame.Rect(390, 100, 100, 60)
        self.audio_text = self.settings_font.render("Audio settings", True, (150,0,0))
        self.sfx_rect = pygame.Rect(520, 150, 100, 30)
        self.sfx_text = self.settings_font_s.render("SFX volume", True, (150,0,0))
        self.sfx_slider = Slider((640, 200), (180, 40), Slider.positions["sfx"])
        self.bgm_rect = pygame.Rect(520, 260, 100, 30)
        self.bgm_text = self.settings_font_s.render("BGM volume", True, (150,0,0))
        self.bgm_slider = Slider((640,310), (180,40), Slider.positions["bgm"])

        self.credits_rect = pygame.Rect(500, 450, 100, 60)
        self.credits = self.settings_font.render("Credits", True, (150,0,0))

        

    def run(self):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.screen.fill((0,0,0))
        
        #interations with sliders
        if self.sfx_slider.slider_rect.collidepoint(mouse_pos) and pressed[0]:
            self.sfx_slider.move(mouse_pos)
            Slider.positions["sfx"] = self.sfx_slider.get_value()
            self.sfx_channel.set_volume(self.sfx_slider.get_value())

        elif self.bgm_slider.slider_rect.collidepoint(mouse_pos) and pressed[0]:
            self.bgm_slider.move(mouse_pos)
            Slider.positions["bgm"] = self.bgm_slider.get_value()
            self.bgm_channel.set_volume(self.bgm_slider.get_value())


        self.sfx_slider.render(self.screen)
        self.bgm_slider.render(self.screen)
        #back function text and button
        self.screen.blit(self.back, self.back_rect)
        #audio settings text
        self.screen.blit(self.audio_text, self.audio_rect)
        self.screen.blit(self.sfx_text, self.sfx_rect)
        self.screen.blit(self.bgm_text, self.bgm_rect)

        self.screen.blit(self.credits, self.credits_rect)

        if pressed[0] and self.back_rect.collidepoint(mouse_pos):
            self.scene_manager.set_scene("menu")
