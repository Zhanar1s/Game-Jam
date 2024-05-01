import pygame
pygame.init()
from spriteclasses import Player, Wall, Door, Witch, Monster, Timer
from interaction import Interactable, Note, Friend, Passcode
from lighting import Light, Dim
from soundbar import sfx, music

class Intro():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.channel = pygame.mixer.Channel(1)
        self.player = Player(self.screen, (400,600))
        self.intro_monologue = Interactable(1, (0,0,1280,720), "intro", "intro monologue")


    def run(self):
        self.intro_monologue.enable = True
        self.player.blit()
        self.screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "intro")

        if self.intro_monologue.finished:
            self.channel.play(sfx["metaldoorshut"])
            self.scene_manager.set_scene("scene1")

        keys = pygame.key.get_pressed()
        self.intro_monologue.interaction(self.player, self.screen, keys)


class Scene1():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room1.png'), (1280, 720))
        self.player = Player(self.screen, (50,600))

        self.wall1 = Wall((0,0), (1280,200), "room1")
        self.table_border = Wall((240,280),(250,80), "room1")
        self.door = Door(self.screen, (600,60))


        self.notebook = Interactable(1, (195, 280, 250, 120), room="room1", item="notebook")
        self.puddle = Interactable(1, (1050, 280, 200, 200), room="room1", item="puddle")

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
                    self.scene_manager.set_scene("menu", "scene1")

        if self.player.rect.colliderect(self.door) and self.door.opened:
            Wall.delete_all("room1")
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

        self.player.wall_collision(Wall.walls["room1"])
        self.wall1.show_test(self.screen, "room1")



class Scene2():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room2.png'), (1280, 720))
        self.monster = Monster(self.screen, (-60,-60))
        self.player = Player(self.screen, (100,600))
        self.witch = Witch(self.screen)
        self.paper = Note(1, (400, 500, 64, 64), room="room2", item="papernote1")
        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)
        self.timer = Timer(screen, 'superlegendboy.ttf', 24, 30) #20 sec timer



        self.wall1 = Wall((0,0), (1280,200), "room2")
        self.border = Interactable(1, (0,0,5,720), "allrooms", "border")
        #self.bgm_channel = pygame.mixer.Channel(0)
        #self.sfx_channel = pygame.mixer.Channel(1)


    def run(self):
        self.screen.blit(self.bg, (0,0))

        self.timer.update()
        self.timer.draw()
        if self.timer.is_finished():
            self.monster.update(self.player.rect.center)
            #print("Timer Finished!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "scene2")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect) and not self.timer.active and not self.timer.used:
                        self.paper.enable = True
                        self.timer.start()

        keys = pygame.key.get_pressed()

        if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
            self.timer.stop()
            self.monster.laughter_channel.stop()
            self.dim.darken(0)
            Wall.delete_all("room2")
            self.scene_manager.set_scene("scene3")



        if self.monster.rect.colliderect(self.player.rect):
            self.witch.scare(self.player)
            exit()


        self.paper.blit(self.screen)
        self.player.move(keys, self.lantern)
        self.player.blit()
        self.screen.blit(self.monster.image, self.monster.rect)
        self.dim.darken(100)
        self.lantern.blit((100,100,100), size=5)
        self.paper.interaction(self.player, self.screen, keys)
        self.border.interaction(self.player, self.screen, keys)
        self.player.wall_collision(Wall.walls["room2"])




class Scene3():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room3.png'), (1280, 720))
        self.paper = Note(2, (200, 400, 64, 64), room="room3", item="papernote2")
        self.player = Player(self.screen, (50,600))
        self.witch = Witch(self.screen)

        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.wall1 = Wall((0,0), (1280,200), "room3")
        self.wall2 = Wall((20,200), (100,200), "room3")
        self.wall3 = Wall((750,200), (100,200), "room3")
        self.wall4 = Wall((1030,200), (80,200), "room3")

        self.border1 = Interactable(1, (0,0,5,720), "allrooms", "border")
        self.border2 = Interactable(1, (1270,0,5,720), "allrooms", "locked")
        self.painting = Interactable(1, (500, 200, 100,200), "room3", "painting")
        self.skull = pygame.image.load("images/items/skull.png")
        self.skull_rect = self.skull.get_rect(center = (1050,400))
        self.skull_activate_rect = pygame.Rect((980, 400, 100, 100))

        self.locked = True

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "scene3")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect):
                        self.paper.enable = True
                    elif self.border1.rect.colliderect(self.player.rect):
                        self.border1.enable = True
                    elif self.border2.rect.colliderect(self.player.rect):
                        self.border2.enable = True
                    elif self.painting.rect.colliderect(self.player.rect):
                        self.painting.enable = True
                        self.locked = False

                    elif self.skull_activate_rect.colliderect(self.player.rect):
                        self.witch.scare_trigger = True


        if not self.locked:
            if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
                self.dim.darken(0)
                Wall.delete_all("room3")
                self.scene_manager.set_scene("scene4")


        keys = pygame.key.get_pressed()

        self.screen.blit(self.skull, self.skull_rect)
        self.paper.blit(self.screen)
        self.player.move(keys, self.lantern)
        self.player.blit()

        self.dim.darken(150)
        self.lantern.blit((100,100,100), size=5)

        self.paper.interaction(self.player, self.screen, keys)
        self.border1.interaction(self.player, self.screen, keys)
        self.border2.interaction(self.player, self.screen, keys)
        self.painting.interaction(self.player, self.screen, keys)


        self.player.wall_collision(Wall.walls["room3"])

        if self.witch.scare_trigger:
            self.witch.scare(self.player)
            exit()

class Scene4():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room4.png'), (1280, 720))
        self.paper = Note(1, (800, 600, 64, 64), room="room4", item="papernote3")
        self.locker = pygame.image.load("images/items/locker1.png")
        self.locker_rect = self.locker.get_rect(topleft = (500,300))
        self.locker_closed = pygame.image.load("images/items/locker.png")

        self.player = Player(self.screen, (50,600))
        self.hidden = False

        self.witch = Witch(self.screen)
        self.timer = 0

        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.wall1 = Wall((0,0), (1280,200), "room4")
        self.wall2 = Wall((20,200), (400,200), "room4")
        self.wall3 = Wall((750,200), (180,200), "room4")
        self.wall4 = Wall((1100,200), (100,200), "room4")
        self.wall5 = Wall((500,300), (130, 80), "room4")

        self.border1 = Interactable(1, (0,0,5,720), "allrooms", "border")
        self.border2 = Interactable(1, (1270,0,5,720), "allrooms", "locked")
        self.locked = True

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        self.played = False

    def run(self):

        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.hidden:
                    self.scene_manager.set_scene("menu", "scene4")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect):
                        self.paper.enable = True
                    elif self.border1.rect.colliderect(self.player.rect):
                        self.border.enable = True
                    elif self.locker_rect.colliderect(self.player.rect):
                        self.locker = self.locker_closed
                        self.hidden = True

        if self.timer > 240 and not self.played:
            self.sfx_channel.play(sfx["steps"])
            self.played = True

        if not self.locked:
            if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
                self.dim.darken(0)
                Wall.delete_all("room4")
                self.scene_manager.set_scene("scene5")


        keys = pygame.key.get_pressed()
        self.screen.blit(self.locker, self.locker_rect)

        self.paper.blit(self.screen)

        if not self.hidden:
            self.player.move(keys, self.lantern)
            self.player.blit()
            self.dim.darken(150)
            self.lantern.blit((100,100,100), size=5)
        else:
            self.dim.darken(220)

        if keys[pygame.K_z] and self.hidden and self.timer > 240:
            if self.timer < 500:
                self.witch.scare(self.player)
                exit()
            else:
                self.hidden = False
                self.locked = False

        self.paper.interaction(self.player, self.screen, keys)
        self.border1.interaction(self.player, self.screen, keys)


        self.player.wall_collision(Wall.walls["room4"])
        self.timer += 1

class Scene5():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room5.png'), (1280, 720))
        self.paper = Note(1, (750, 420, 64, 64), room="room5", item="papernote4")
        self.passcode = Passcode(self.screen, (1000,350,100,40))
        self.player = Player(self.screen, (50,600))

        self.paper = Note(1, (700, 600, 64, 64), room="room5", item="papernote4")
        self.cabinet = Interactable(1, (240,280,380,80), room="room5", item="cabinet")
        self.passcode = Passcode(self.screen, (800,260,100,40))
        self.door = Door(self.screen, (800,80))
        
        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)
        self.timer = Timer(screen, 'superlegendboy.ttf', 24, 80) #20 sec timer

        self.wall1 = Wall((0,0), (1280,200), "room5")
        self.wall2 = Wall((250,280),(370,70), "room5")
        self.border1 = Interactable(1, (0,0,5,720), "allrooms", "border")
        self.border2 = Interactable(1, (1270,0,5,720), "allrooms", "wall")
        
        self.locked = True

        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))

        self.timer.update()
        self.timer.draw()
        if self.timer.is_finished():
            self.monster.update(self.player.rect.center)
            #print("Timer Finished!")
        events = pygame.event.get()
        self.passcode.input_visualizer.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "scene5")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect) and not self.timer.active and not self.timer.used:
                        self.paper.enable = True
                        self.timer.start()
                        self.sfx_channel.play(sfx["twinkle"])
                    elif self.cabinet.rect.colliderect(self.player.rect):
                        self.cabinet.enable = True
                    elif self.border1.rect.colliderect(self.player.rect):
                        self.border1.enable = True
                    elif self.border2.rect.colliderect(self.player.rect):
                        self.border2.enable = True

        keys = pygame.key.get_pressed()

        if self.passcode.unlock():
            if self.player.rect.colliderect(self.door.rect) and keys[pygame.K_z]:
                self.door.open_door()
                self.timer.stop()
                self.monster.laughter_channel.stop()
                self.dim.darken(0)
                Wall.delete_all("room5")
                self.scene_manager.set_scene("scene6")


        if self.monster.rect.colliderect(self.player.rect):
            self.witch.scare(self.player)
            exit()

        if self.monster.rect.colliderect(self.player.rect):
            self.witch.scare(self.player)
            exit()

        self.paper.blit(self.screen)
        self.passcode.interaction(self.player)

        self.player.move(keys, self.lantern)
        self.door.blit()
        self.player.blit()
        self.screen.blit(self.monster.image, self.monster.rect)

        self.dim.darken(150)
        self.lantern.blit((100,100,100), size=5)

        self.paper.interaction(self.player, self.screen, keys)
        self.cabinet.interaction(self.player, self.screen, keys)
        self.border1.interaction(self.player, self.screen, keys)
        self.border2.interaction(self.player, self.screen, keys)
        
        self.player.wall_collision(Wall.walls["room5"])


class Scene6():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room6.png'), (1280, 720))
        self.paper = Note(1, (700, 500, 64, 64), room="room6", item="papernote5")
        self.player = Player(self.screen, (150,600))


        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.wall1 = Wall((0,0), (1280,200), "room6")
        self.border = Interactable(1, (0,0,5,720), "allrooms", "border")
        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "scene6")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect):
                        self.paper.enable = True
                    elif self.border.rect.colliderect(self.player.rect):
                        self.border.enable = True

        if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
            self.dim.darken(0)
            Wall.delete_all("room6")
            self.scene_manager.set_scene("scene7")

        keys = pygame.key.get_pressed()

        self.paper.blit(self.screen)
        self.player.move(keys, self.lantern)
        self.player.blit()

        self.dim.darken(90)
        self.lantern.blit((100,100,100), size=5)

        self.paper.interaction(self.player, self.screen, keys)
        self.border.interaction(self.player, self.screen, keys)
        self.player.wall_collision(Wall.walls["room6"])

class Scene7():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load('images/room/room7.png'), (1280, 720))
        self.paper = Note(1, (300, 600, 64, 64), room="room7", item="papernote6")
        self.player = Player(self.screen, (50,600))
        self.witch = Witch(self.screen)

        self.lantern = Light(self.screen, (220,220,220), 25, (self.player.rect.x + 97, self.player.rect.y + 152))
        self.dim = Dim(self.screen)

        self.wall1 = Wall((0,0), (1280,200), "room7")
        self.wall2 = Wall((240,280),(700,80), "room7")
        self.border = Interactable(1, (0,0,5,720), "allrooms", "border")
        self.bgm_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)

    def run(self):
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "scene7")
                if event.key == pygame.K_z:
                    if self.paper.rect.colliderect(self.player.rect):
                        self.paper.enable = True
                    elif self.border.rect.colliderect(self.player.rect):
                        self.border.enable = True

        keys = pygame.key.get_pressed()
        if self.player.rect.x >= self.screen.get_width() - self.player.rect.width - 10:
            self.witch.scare(self.player)
            Wall.delete_all("room7")
            self.scene_manager.set_scene("limbo")

        self.paper.blit(self.screen)
        self.player.move(keys, self.lantern)
        self.player.blit()

        self.dim.darken(90)
        self.lantern.blit((100,100,100), size=5)

        self.paper.interaction(self.player, self.screen, keys)
        self.border.interaction(self.player, self.screen, keys)
        self.player.wall_collision(Wall.walls["room7"])

class Limbo():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.image.load("images/room/room00.jpg")
        self.bg_rect = self.bg.get_rect(center = (640, 360))


        self.player = Player(self.screen, (400,600))
        self.limbo_monologue = Interactable(1, (0,0,1280,720), "limbo", "limbo monologue")

    def run(self):

        self.limbo_monologue.enable = True
        self.player.blit()
        self.screen.blit(self.bg, self.bg_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "limbo")


        if self.limbo_monologue.finished:
            self.scene_manager.set_scene("university")

        keys = pygame.key.get_pressed()
        self.limbo_monologue.interaction(self.player, self.screen, keys)


class University():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.friend = Friend(1)
        self.player = Player(self.screen, (300,300))
        self.bg = pygame.transform.scale(pygame.image.load("images/room/classroom.png"), (1280, 720))



    def run(self):
        self.friend.enable = True
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "university")

        if self.friend.finished:
            self.scene_manager.set_scene("finale")

        keys = pygame.key.get_pressed()
        self.friend.interaction(self.player, self.screen, keys)


class Finale():
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager

        self.bg = pygame.transform.scale(pygame.image.load("images/room/end.png"), (1280,720))
        self.channel = pygame.mixer.Channel(1)
        self.player = Player(self.screen, (400,600))
        self.finale_monologue = Interactable(1, (0,0,1280,720), "finale", "finale monologue")


    def run(self):
        self.finale_monologue.enable = True
        self.player.blit()
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.set_scene("menu", "finale")



        keys = pygame.key.get_pressed()
        self.finale_monologue.interaction(self.player, self.screen, keys)
