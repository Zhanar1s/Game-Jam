import pygame
pygame.init()

sfx = {
    "dooropen" : pygame.mixer.Sound("sfx/dooropen.wav"),
    "doorclose" : pygame.mixer.Sound("sfx/doorclose.wav"),
    "ambience" : pygame.mixer.Sound("sfx/ambience.wav"),
    "jumpscare" : pygame.mixer.Sound("sfx/jumpscare.ogg"),
    "metaldoorshut" : pygame.mixer.Sound("sfx/metaldoorshut.wav"),
    "steps" : pygame.mixer.Sound("sfx/steps.wav"),
    "twinkle" : pygame.mixer.Sound("sfx/twinkle.mp3"),
    "laughter" : pygame.mixer.Sound("sfx/laughter.mp3"),
    "timer" : pygame.mixer.Sound("sfx/timer.mp3")

}

music = {
    "menusong" : pygame.mixer.Sound("music/menusong.mp3"),
    "limbotheme" : pygame.mixer.Sound("music/limbotheme.mp3")
}
