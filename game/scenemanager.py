import pygame

screen_width = 1280
screen_height = 720

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.scene_manager = Scene_manager("scene1")
        self.menu = Menu(self.screen, self.scene_manager)
        self.scene1 = Scene1(self.screen, self.scene_manager)
             
        self.scenes = {
            "menu" : self.menu,
            "scene1" : self.scene1
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

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
    def __init__(self, display, scene_manager):
        self.display = display
        self.scene_manager = scene_manager

    def run(self):
        self.display.fill((255,0,0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.scene_manager.set_scene("scene1")


class Scene1():
    def __init__(self, display, scene_manager):
        self.display = display
        self.scene_manager = scene_manager

    def run(self):
        self.display.fill((0,0,255))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.scene_manager.set_scene("menu")

if __name__ == "__main__":
    game = Game()
    game.run()