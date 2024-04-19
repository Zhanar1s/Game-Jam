
import pygame
from utils import Button, Slider

from spriteclasses import Player, Wall, Door
from interaction import Interactable
from lighting import Light, Dim
from soundbar import sfx, music

screen_width = 1280
screen_height = 720

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("GONE")

        self.clock = pygame.time.Clock()

        self.scene_manager = Scene_manager("menu")
        self.menu = Menu(self.screen, self.scene_manager)
        self.settings = Settings(self.screen, self.scene_manager)
        self.scene1 = Scene1(self.screen, self.scene_manager)
        self.scene2 = Scene2(self.screen, self.scene_manager)
        self.scene3 = Scene3(self.screen, self.scene_manager)

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
             
        self.scenes = {
            "menu" : self.menu,
            "settings" : self.settings,
            "scene1" : self.scene1,
            "scene2" : self.scene2,
            "scene3" : self.scene3
        }

    def run(self):
        self.bgm_channel.play(music["menusong"], -1)
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

        self.bg = pygame.transform.scale(pygame.image.load("images/menu_back.png"), (1280,720))

        self.play_button = Button((640,400), "images/buttons/play.png")
        self.settings_button = Button((640,500), "images/buttons/settings.png")
        self.exit_button = Button((640,600), "images/buttons/quit.png")

        self.title = pygame.image.load("images/gone.png")
        self.title_rect = self.title.get_rect(center = (640, 240))

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
                self.scene_manager.set_scene("scene1")

        self.screen.blit(self.title, self.title.get_rect(center = self.title_rect.center))

        for button in Button.main_buttons:
            button.show(self.screen)
            button.on_hover(self.screen, mouse_pos)
        

class Settings():
    def __init__(self, screen, scene_manager : Scene_manager):
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
            if event.type == pygame.QUIT:
                exit()
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

        if self.player.rect.colliderect(self.door) and self.door.opened:
            Wall.delete_all()
            self.dim.darken(0)
            self.scene_manager.set_scene("scene2")

        keys = pygame.key.get_pressed()

        self.player.move(keys, self.lantern)

        self.door.blit()
        self.player.blit()

        self.dim.darken(150)

        self.lantern.blit((100,100,100), size=5)

        self.notebook.interaction(self.player, self.screen, keys)
        self.puddle.interaction(self.player, self.screen, keys)

        self.player.wall_collision(Wall.walls)



class Scene2():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room2.png'), (1280, 720))
        self.player = Player(self.screen, (50,600))


        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.wall1 = Wall((0,0), (1280,200))
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu")

        if self.player.rect.right == self.screen.get_width() - 10:
            self.dim.darken(0)
            Wall.delete_all()
            self.scene_manager.set_scene("scene3")

        keys = pygame.key.get_pressed()
        


        self.player.move(keys, self.lantern)

        self.player.blit()

        self.dim.darken(150)

        self.lantern.blit((100,100,100), size=5)

        self.player.wall_collision(Wall.walls)


class Scene3():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room3.png'), (1280, 720))
        self.player = Player(self.screen, (50,600))

        self.wall1 = Wall((0,0), (1280,200))

        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu")


        keys = pygame.key.get_pressed()

        self.player.move(keys, self.lantern)

        self.player.blit()

        self.dim.darken(150)

        self.lantern.blit((100,100,100), size=5)

        self.player.wall_collision(Wall.walls)