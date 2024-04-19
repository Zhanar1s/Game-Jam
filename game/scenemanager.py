import pygame

from soundbar import sfx, music

from menu import Settings, Menu
from scenes import Scene1, Scene2, Scene3

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



