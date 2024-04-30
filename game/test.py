import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
import pygame.locals as pl

pygame.init()

# No arguments needed to get started
textinput = TextInputVisualizer()

# But more customization possible: Pass your own font object
font = pygame.font.SysFont("Consolas", 55)
# Create own manager with custom input validator
manager = TextInputManager(validator = lambda input: len(input) <= 5)
# Pass these to constructor
textinput_custom = TextInputVisualizer(manager=manager, font_object=font)
# Customize much more
textinput_custom.cursor_width = 4
textinput_custom.cursor_blink_interval = 400 # blinking interval in ms
textinput_custom.antialias = False
textinput_custom.font_color = (0, 85, 170)

screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)
flag = False

while True:
    screen.fill((225, 225, 225))
    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)
    textinput_custom.update(events)

    # Get its surface to blit onto the screen
    if pygame.mouse.get_pressed()[0]:
        flag = True
    
    if flag:
        screen.blit(textinput.surface, (500, 400))

    # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
    textinput_custom.font_color = [(c+10)%255 for c in textinput_custom.font_color]

    # Check if user is exiting or pressed return
    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(f"User pressed enter! Input so far: {textinput.value}")

    pygame.display.update()
    clock.tick(30)