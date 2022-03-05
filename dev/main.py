
import pygame
import pygame_gui
from toolbar import Toolbar

SCREEN_DIMENSIONS = (800, 600)

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)

background = pygame.Surface(SCREEN_DIMENSIONS)
background.fill(pygame.Color('#FFFFFF'))

# set 
ui_manager = pygame_gui.UIManager(SCREEN_DIMENSIONS, "theme.json")


hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=ui_manager)



# initialize the toolbar
tb = Toolbar(ui_manager, 100, SCREEN_DIMENSIONS)


clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0 # time since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    ui_manager.draw_ui(window_surface)

    pygame.display.update()