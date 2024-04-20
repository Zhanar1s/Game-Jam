import pygame
from typing import Optional

from soundbar import sfx, music

from menu import Settings, Menu
from scenes import Scene1, Scene2, Scene3, Scene4, Scene5, Scene6, Scene7, Intro, Limbo

screen_width = 1280
screen_height = 720

class Game():
    '''
    Main game class. 
    '''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("GONE")

        self.clock = pygame.time.Clock()

        '''
        Here we init every single Scene
        '''

        self.scene_manager = Scene_manager("menu")
        self.menu = Menu(self.screen, self.scene_manager)
        self.settings = Settings(self.screen, self.scene_manager)
        self.intro = Intro(self.screen, self.scene_manager)
        self.scene1 = Scene1(self.screen, self.scene_manager)
        self.scene2 = Scene2(self.screen, self.scene_manager)
        self.scene3 = Scene3(self.screen, self.scene_manager)
        self.scene4 = Scene4(self.screen, self.scene_manager)
        self.scene5 = Scene5(self.screen, self.scene_manager)
        self.scene6 = Scene6(self.screen, self.scene_manager)
        self.scene7 = Scene7(self.screen, self.scene_manager)
        self.limbo = Limbo(self.screen, self.scene_manager)



        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

        '''
        Store scenes in a dict parameter
        '''
        self.scenes = {
            "menu" : self.menu,
            "settings" : self.settings,
            "intro" : self.intro,
            "scene1" : self.scene1,
            "scene2" : self.scene2,
            "scene3" : self.scene3,
            "scene4" : self.scene4,
            "scene5" : self.scene5,
            "scene6" : self.scene6,
            "scene7" : self.scene7,
            "limbo" : self.limbo
        }

    def run(self):
        self.bgm_channel.play(music["menusong"], -1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            '''
            The main element of the entire game.
            Here we call the get_scene function of scene manager and according to the returned value, we play this scene
            '''
            self.scenes[self.scene_manager.get_scene()].run()
            
            pygame.display.update()
            self.clock.tick(60)



class Scene_manager():
    '''
    A class that manages the current scene. Used to switch and return the current scene
    '''
    def __init__(self, current_scene):
        self.current_scene = current_scene
        self.prev_scene = "intro"

    def get_scene(self):
        return self.current_scene

    def set_scene(self, scene, prev_scene = None):
        if prev_scene:
            self.prev_scene = prev_scene
        self.current_scene = scene
