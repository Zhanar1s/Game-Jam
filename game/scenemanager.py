
import pygame
from menu import Button, Slider

from spriteclasses import Player, Wall, Door
from interaction import Interactable
from lighting import Light, Dim


screen_width = 1280
screen_height = 720

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.scene_manager = Scene_manager("menu")
        self.menu = Menu(self.screen, self.scene_manager)
        self.settings = Settings(self.screen, self.scene_manager)
        self.scene1 = Scene1(self.screen, self.scene_manager)

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
             
        self.scenes = {
            "menu" : self.menu,
            "settings" : self.settings,
            "scene1" : self.scene1
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.scenes[self.scene_manager.get_scene()].run()

            pygame.display.update()
            self.clock.tick(60)

        

class Scene_manager():
    def __init__(self, current_scene):
        self.current_scene = current_scene

    def get_scene(self):
        return self.current_scene
    
    def set_scene(self, scene):
        self.current_scene = scene

class Menu():
    def __init__(self, screen, scene_manager : Scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager


        self.play_button = Button((640,400), 700, 80, "play", (255,255,255), 62)
        self.settings_button = Button((640,500), 700, 80, "settings", (255,255,255), 62)
        self.exit_button = Button((640,600), 700, 80, "exit", (255,255,255), 62)

        self.title_font = pygame.font.Font(None, 100)
        self.title_rect = pygame.Rect(250,150, 700,100)
        self.title = self.title_font.render("GONE", True, (255,255,255))

        for button in (self.play_button, self.exit_button, self.settings_button):
            button.add_to_main_buttons()


    def run(self):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.screen.fill((0,0,0))

        if pressed[0]:
            if self.settings_button.rect.collidepoint(mouse_pos):
                self.scene_manager.set_scene("settings")
            elif self.exit_button.rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()
            elif self.play_button.rect.collidepoint(mouse_pos):
                self.scene_manager.set_scene("scene1")

        self.screen.blit(self.title, self.title.get_rect(center = self.title_rect.center))

        for button in Button.main_buttons:
            button.show(self.screen)
            button.on_hover(mouse_pos)
        

class Settings():
    def __init__(self, screen, scene_manager : Scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

        #font
        self.settings_font = pygame.font.Font(None, 40)
        self.settings_font_s = pygame.font.Font(None, 24)
        #back button
        self.back_rect = pygame.Rect(85, 30, 100 ,40)
        self.back_text = self.settings_font.render("Back", True, (255,255,255))

        #audio settings 
        self.audio_rect = pygame.Rect(60, 100, 100, 60)
        self.audio_text = self.settings_font.render("Audio settings", True, (255,255,255))
        self.sfx_rect = pygame.Rect(60, 150, 100, 30)
        self.sfx_text = self.settings_font_s.render("SFX volume", True, (255,255,255))
        self.sfx_slider = Slider((150, 200), (180, 40), Slider.positions["sfx"])
        self.bgm_rect = pygame.Rect(60, 260, 100, 30)
        self.bgm_text = self.settings_font_s.render("BGM volume", True, (255,255,255))
        self.bgm_slider = Slider((150,310), (180,40), Slider.positions["bgm"])

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
        self.screen.blit(self.back_text, self.back_rect)
        back_trio = pygame.draw.polygon(self.screen, (255,255,255), [(30,40),(80,60),(80,20)])
        #audio settings text
        self.screen.blit(self.audio_text, self.audio_rect)
        self.screen.blit(self.sfx_text, self.sfx_rect)
        self.screen.blit(self.bgm_text, self.bgm_rect)

        if pressed[0] and self.back_rect.collidepoint(mouse_pos):
            self.scene_manager.set_scene("menu")


class Scene1():
    def __init__(self, screen, scene_manager : Scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room1.png'), (1280, 720))
        self.player = Player(self.screen, (50,600))

        self.wall1 = Wall((0,0), (1280,200))
        self.table_border = Wall((240,280),(250,80))
        self.door = Door(self.screen, (600,60))


        self.notebook = Interactable(1, (195, 280, 250, 120), (255,255,255), room="room1", item="notebook")
        self.puddle = Interactable(1, (950, 280, 200, 200), (255,255,255), room="room1", item="puddle")

        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.notebook.rect.colliderect(self.player.rect):
                        self.notebook.enable = True
                    if self.puddle.rect.colliderect(self.player.rect):
                        self.puddle.enable = True
                    if self.door.rect.colliderect(self.player.rect):
                        self.door.open_door()
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu")


        keys = pygame.key.get_pressed()

        self.player.move(keys, self.lantern)

        self.door.blit()
        self.player.blit()

        self.dim.darken(200)

        self.lantern.blit((100,100,100), size=5)

        self.notebook.interaction(self.player, self.screen, keys)
        self.puddle.interaction(self.player, self.screen, keys)

        self.player.wall_collision(Wall.walls)



