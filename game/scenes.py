import pygame
pygame.init()
from spriteclasses import Player, Wall, Door
from interaction import Interactable, Note
from lighting import Light, Dim


class Scene1():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room1.png'), (1280, 720))
        self.player = Player(self.screen, (50,600))

        self.wall1 = Wall((0,0), (1280,200))
        self.table_border = Wall((240,280),(250,80))
        self.door = Door(self.screen, (600,60))


        self.notebook = Interactable(1, (195, 280, 250, 120), room="room1", item="notebook")
        self.puddle = Interactable(1, (950, 280, 200, 200), room="room1", item="puddle")

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
        self.paper = Note(1, (400, 500, 64, 64), room="room2", item="papernote1")
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
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect):
                        self.paper.enable = True

        if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
            self.dim.darken(0)
            Wall.delete_all()
            print("scene3")
            self.scene_manager.set_scene("scene3")

        keys = pygame.key.get_pressed()
        
        self.paper.blit(self.screen)

        self.player.move(keys, self.lantern)
        self.player.blit()

        self.dim.darken(100)
        self.lantern.blit((100,100,100), size=5)

        self.paper.interaction(self.player, self.screen, keys)

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

        self.dim.darken(70)

        self.lantern.blit((100,100,100), size=5)

        self.player.wall_collision(Wall.walls)